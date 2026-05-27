import os
import sys
import time
import re
import sqlite3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    print("Connecting to Chrome on port 9222...")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Error connecting to Chrome: {e}")
        print("Please make sure Chrome is running with remote debugging enabled on port 9222.")
        sys.exit(1)
        
    print("Connected to Chrome!")
    
    # 1. Discover Spring 2026 courses and their IDs
    print("Scanning Canvas Dashboard for active course IDs...")
    driver.get("https://canvas.ucsd.edu")
    print("Checking if user is logged into Canvas...")
    while True:
        try:
            curr_url = driver.current_url or ""
        except Exception:
            curr_url = ""
        if "canvas.ucsd.edu" in curr_url and "login" not in curr_url:
            break
        print("Waiting for you to log into Canvas in your browser window...")
        time.sleep(3)
    print("Logged into Canvas successfully!")
    time.sleep(2)
    
    links = driver.find_elements(By.TAG_NAME, "a")
    canvas_courses = {}
    for link in links:
        try:
            text = link.text.strip()
            href = link.get_attribute("href") or ""
            if href and "courses/" in href:
                m = re.search(r"courses/(\d+)", href)
                if m:
                    course_id = m.group(1)
                    if course_id not in canvas_courses:
                        # Only keep relevant graduate-level courses for Spring 2026
                        if any(code in text for code in ["GPCO 403", "GPCO 410", "GPEC 446", "GPPS 444", "GPPS 463", "International Economics", "Politics", "Methods", "Warfare"]):
                            canvas_courses[course_id] = text
        except Exception:
            continue
            
    # Fallback to hardcoded database mapping if none discovered
    course_mapping = {
        "GPCO 403": {"id": 1, "canvas_id": None, "full_name": "GPCO 403 — International Economics"},
        "GPCO 410": {"id": 2, "canvas_id": None, "full_name": "GPCO 410 — International Politics & Security"},
        "GPEC 446": {"id": 3, "canvas_id": "74851", "full_name": "GPEC 446 — Quantitative Methods 3"},
        "GPPS 444": {"id": 4, "canvas_id": None, "full_name": "GPPS 444 — History of Warfare"},
        "GPPS 463": {"id": 5, "canvas_id": None, "full_name": "GPPS 463 — Politics of Southeast Asia"}
    }
    
    # Match discovered Canvas IDs to our local courses
    for canvas_id, name in canvas_courses.items():
        for code, info in course_mapping.items():
            if code in name or code.replace(" ", "") in name.replace(" ", ""):
                info["canvas_id"] = canvas_id
                print(f"Matched: {code} -> Canvas Course ID {canvas_id} ('{name}')")
                
    # Fill in any missing ones manually if we can guess, or fallback
    # Let's see if we can find them from active links. If a canvas_id is missing, let's keep it as is.
    print("\nSummary of Canvas Course ID mapping:")
    for code, info in course_mapping.items():
        print(f" - {info['full_name']}: Canvas ID = {info['canvas_id']}")
        
    print("\nStarting Grade Scraper...")
    
    # Database connection
    conn = sqlite3.connect("_claudia/claudia.db")
    cursor = conn.cursor()
    
    all_course_results = {}
    
    for code, info in course_mapping.items():
        canvas_id = info["canvas_id"]
        local_id = info["id"]
        full_name = info["full_name"]
        
        if not canvas_id:
            print(f"\nSkipping {code} - No Canvas course ID matched.")
            continue
            
        grades_url = f"https://canvas.ucsd.edu/courses/{canvas_id}/grades"
        print(f"\nNavigating to Grades page for {full_name}: {grades_url}")
        driver.get(grades_url)
        time.sleep(4)
        
        # Click "Show All Details" button to expand grade distributions / means
        try:
            show_details = driver.find_element(By.ID, "show_all_details_button")
            show_details.click()
            print("Expanded all grade details/distributions.")
            time.sleep(2)
        except Exception:
            print("No details button found or already expanded.")
            
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Find the grades summary table
        table = soup.find("table", id="grades_summary")
        if not table:
            print(f"Could not find grades table for {code}. Skipping.")
            continue
            
        rows = table.find_all("tr", class_="student_assignment")
        print(f"Found {len(rows)} assignment rows in page HTML.")
        
        course_grades = []
        
        for row in rows:
            try:
                # 1. Assignment Title
                title_el = row.find("th", class_="title")
                title = ""
                if title_el:
                    a_el = title_el.find("a")
                    title = a_el.text.strip() if a_el else title_el.text.strip()
                # Clean up title (remove trailing 'Click to test...' or comments)
                title = title.split('\n')[0].strip()
                
                # 2. Student's Score
                score_el = row.find("td", class_="assignment_score")
                score_text = ""
                if score_el:
                    grade_el = score_el.find("span", class_="grade")
                    if grade_el:
                        score_text = grade_el.text.strip()
                
                # If ungraded or dash, skip
                if not score_text or score_text == "-" or "Not Graded" in score_text:
                    continue
                    
                # Clean score (e.g. "14.1\n/ 17" or similar)
                score_cleaned = score_text.split('/')[0].strip()
                
                # 3. Possible Points
                possible_el = row.find("td", class_="points_possible")
                possible_text = possible_el.text.strip() if possible_el else "0"
                possible_text = possible_text.replace(",", "")
                
                # Convert to floats
                try:
                    score_val = float(score_cleaned.replace("%", ""))
                    possible_val = float(possible_text)
                    if "%" in score_cleaned:
                        # It's a percentage grade
                        score_pct = score_val / 100.0
                        score_val = score_pct * possible_val
                    else:
                        score_pct = score_val / possible_val if possible_val > 0 else 0.0
                except ValueError:
                    continue
                    
                # 4. Find the Mean, High, Low from the expanded details row
                # The details are usually in a subsequent row or a div with class 'score_details'
                mean_val = None
                high_val = None
                low_val = None
                
                # Find sibling elements or within the row itself
                # Canvas places score details inside a div with class 'details' in a row with class 'comments'
                details_row = row.find_next_sibling("tr", class_="comments")
                if details_row:
                    details_text = details_row.get_text()
                    # RegEx for Mean, High, Low
                    mean_match = re.search(r"Mean:\s*([\d\.]+)", details_text, re.IGNORECASE)
                    high_match = re.search(r"High:\s*([\d\.]+)", details_text, re.IGNORECASE)
                    low_match = re.search(r"Low:\s*([\d\.]+)", details_text, re.IGNORECASE)
                    
                    if mean_match:
                        mean_val = float(mean_match.group(1))
                    if high_match:
                        high_val = float(high_match.group(1))
                    if low_match:
                        low_val = float(low_match.group(1))
                
                # 5. Extract weight/group if possible
                # We can also fallback to database weights
                course_grades.append({
                    "title": title,
                    "score": score_val,
                    "possible": possible_val,
                    "score_pct": score_pct,
                    "mean": mean_val,
                    "high": high_val,
                    "low": low_val
                })
                
                print(f"   Saved: '{title}' | Score: {score_val}/{possible_val} ({score_pct:.1%}) | Mean: {mean_val} | High: {high_val}")
                
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
                
        if course_grades:
            all_course_results[code] = course_grades
            
    # 2. Performance Analysis and Grading Curve Projection
    print("\n========================================================")
    print("📈 GRADUATE ACADEMIC PERFORMANCE & GRADE CURVE PROJECTION")
    print("========================================================\n")
    
    # Standard GPS Graduate Grading Scale on Curve:
    # Top tier (well above mean, usually 0.5+ SD above mean): A / A+
    # Performing above the mean (0.1 to 0.5 SD or > 5% above mean): A-
    # Performing exactly at/near the mean (-2% to +2% of mean): B+ (GPS median grade is usually B+)
    # Performing slightly below the mean (-2% to -10% below mean): B
    # Performing significantly below the mean (> 10% below mean): B- / C+
    
    for code, grades in all_course_results.items():
        print(f"Class: {course_mapping[code]['full_name']}")
        print("-" * 60)
        
        total_possible = 0.0
        total_student = 0.0
        total_mean = 0.0
        
        has_mean = True
        
        for g in grades:
            # If we don't have a mean, we fallback to treating it as missing or equal to score
            if g["mean"] is None:
                has_mean = False
                continue
            
            # Canvas might report mean in percentage or absolute points.
            # We assume it matches the scale of the assignment.
            total_possible += g["possible"]
            total_student += g["score"]
            total_mean += g["mean"]
            
        if total_possible > 0 and has_mean:
            student_pct = total_student / total_possible
            mean_pct = total_mean / total_possible
            diff_pct = student_pct - mean_pct
            
            print(f" * Graded assignments: {len(grades)}")
            print(f" * Cumulative Score: {total_student:.1f} / {total_possible:.1f} ({student_pct:.1%})")
            print(f" * Cumulative Class Mean: {total_mean:.1f} / {total_possible:.1f} ({mean_pct:.1%})")
            
            # Determine Curve Grade
            if diff_pct >= 0.08:
                projected_grade = "A (performing well above the class mean)"
                grade_letter = "A"
            elif diff_pct >= 0.03:
                projected_grade = "A- (performing above the class mean)"
                grade_letter = "A-"
            elif diff_pct >= -0.01:
                projected_grade = "B+ (performing at/near the class mean — typical GPS median)"
                grade_letter = "B+"
            elif diff_pct >= -0.07:
                projected_grade = "B (performing slightly below the class mean)"
                grade_letter = "B"
            else:
                projected_grade = "B- / C+ (performing significantly below the class mean)"
                grade_letter = "B-"
                
            print(f" * Performance Delta: {diff_pct:+.1%}")
            print(f" * Projected Grade: {projected_grade}\n")
            
            # Log in the database if there are assignments
            # Let's save a summary in claudia.db grades table or assignments table
            try:
                # Get local course database ID
                course_id = course_mapping[code]["id"]
                # Insert the aggregated stats or individual grades
                for g in grades:
                    cursor.execute("""
                        SELECT id FROM assignments 
                        WHERE course_id = ? AND title LIKE ?
                    """, (course_id, f"%{g['title']}%"))
                    a_row = cursor.fetchone()
                    a_id = a_row[0] if a_row else 0
                    
                    # Update local grades table
                    cursor.execute("""
                        INSERT INTO grades (course_id, assignment_id, score, weight, notes, date_recorded)
                        VALUES (?, ?, ?, ?, ?, date('now'))
                        ON CONFLICT(course_id, assignment_id) DO UPDATE SET score=excluded.score
                    """, (course_id, a_id, f"{g['score']:.1f}/{g['possible']:.1f}", None, f"Scraped from Canvas. Mean: {g['mean']}. High: {g['high']}."))
                conn.commit()
            except Exception as e:
                print(f"DB log error: {e}")
                
        else:
            # Missing mean or no grades
            student_pct = sum(g["score"] for g in grades) / sum(g["possible"] for g in grades) if sum(g["possible"] for g in grades) > 0 else 0
            print(f" * Graded assignments: {len(grades)}")
            print(f" * Cumulative Score: ({student_pct:.1%})")
            print(" * Cumulative Class Mean: Unavailable (No distribution charts released by professor)\n")
            
    conn.close()
    print("Browser scraping and database logging completed successfully!")

if __name__ == "__main__":
    main()
