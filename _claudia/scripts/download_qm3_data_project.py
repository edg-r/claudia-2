import os
import sys
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        
    try:
        init_url = driver.current_url
    except Exception:
        init_url = "None"
    print(f"Connected to Chrome! Current URL: {init_url}")
    
    # Wait for the user to log in and reach Canvas
    print("Checking if user is logged into Canvas...")
    while True:
        try:
            curr_url = driver.current_url or ""
        except Exception:
            curr_url = ""
        if "canvas.ucsd.edu" in curr_url:
            break
        print("Waiting for you to navigate to canvas.ucsd.edu and log in...")
        time.sleep(3)
        
    print("Successfully connected to Canvas!")
    
    # Let's find GPEC 446 course on the page
    # First, let's go to Dashboard if we aren't there or if we can see the course links
    try:
        curr_url = driver.current_url or ""
    except Exception:
        curr_url = ""
    if "courses" not in curr_url and "dashboard" not in curr_url:
        print("Navigating to Canvas Dashboard...")
        driver.get("https://canvas.ucsd.edu")
        time.sleep(3)
        
    print("Searching for GPEC 446 / QM3 course link...")
    # Find links on the page containing "GPEC 446" or "QM 3" or "QM3"
    course_link = None
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        try:
            text = link.text or ""
            href = link.get_attribute("href") or ""
            if href and ("courses" in href) and ("446" in text or "QM3" in text or "QM 3" in text or "Quantitative Methods" in text):
                course_link = href
                print(f"Found course link: '{text}' -> {href}")
                break
        except Exception:
            continue
            
    if not course_link:
        # Let's try to search by course card on the dashboard
        print("Course link not found on main page. Searching dashboard cards...")
        cards = driver.find_elements(By.CLASS_NAME, "ic-DashboardCard__link")
        for card in cards:
            try:
                href = card.get_attribute("href") or ""
                title = card.get_attribute("title") or ""
                if href and ("446" in title or "QM3" in title or "QM 3" in title or "Quantitative Methods" in title):
                    course_link = href
                    print(f"Found course link in cards: '{title}' -> {href}")
                    break
            except Exception:
                continue

    if not course_link:
        # Prompt the user to navigate to the GPEC 446 course home page themselves
        print("\n[ACTION REQUIRED] Could not automatically find the GPEC 446 course link.")
        print("Please click on GPEC 446 (QM3) in your browser, then wait...")
        while True:
            try:
                curr_url = driver.current_url or ""
            except Exception:
                curr_url = ""
            if "courses/" in curr_url:
                break
            time.sleep(2)
        try:
            course_link = driver.current_url
        except Exception:
            course_link = ""
        print(f"Detected GPEC 446 Course Home Page: {course_link}")

    # Ensure we are on the course home page
    try:
        curr_url = driver.current_url or ""
    except Exception:
        curr_url = ""
    if curr_url != course_link and not curr_url.startswith(course_link):
        print(f"Navigating to course: {course_link}")
        driver.get(course_link)
        time.sleep(3)
        
    # Get course URL base
    try:
        curr_url = driver.current_url or ""
    except Exception:
        curr_url = ""
    course_match = re.search(r"courses/(\d+)", curr_url)
    if not course_match:
        print("Could not parse course ID from URL. Exiting.")
        sys.exit(1)
    course_id = course_match.group(1)
    print(f"Canvas Course ID: {course_id}")
    
    # Navigate directly to assignments list
    assignments_url = f"https://canvas.ucsd.edu/courses/{course_id}/assignments"
    print(f"Navigating to assignments page: {assignments_url}")
    driver.get(assignments_url)
    time.sleep(3)
    
    # Search for "Data Project" or "Independent Data Project" or similar
    print("Searching for Data Project assignment...")
    project_url = None
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        try:
            text = link.text or ""
            href = link.get_attribute("href") or ""
            if href and ("assignments/" in href) and ("data project" in text.lower() or "independent project" in text.lower() or "causal inference project" in text.lower()):
                project_url = href
                print(f"Found Data Project assignment link: '{text}' -> {href}")
                break
        except Exception:
            continue
            
    if not project_url:
        print("\n[ACTION REQUIRED] Could not find the Data Project assignment automatically in the list.")
        print("Please click on the Data Project assignment link in your browser...")
        while True:
            try:
                curr_url = driver.current_url or ""
            except Exception:
                curr_url = ""
            if "assignments/" in curr_url:
                break
            time.sleep(2)
        try:
            project_url = driver.current_url
        except Exception:
            project_url = ""
        print(f"Detected Data Project Page: {project_url}")
        
    # Ensure we are on the project page
    try:
        curr_url = driver.current_url or ""
    except Exception:
        curr_url = ""
    if curr_url != project_url and not curr_url.startswith(project_url):
        print(f"Navigating to: {project_url}")
        driver.get(project_url)
        time.sleep(3)
        
    print("Successfully loaded Data Project page!")
    
    # Create the target directory
    target_dir = "/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Data Project"
    os.makedirs(target_dir, exist_ok=True)
    print(f"Target directory created: {target_dir}")
    
    # Save the instructions text
    print("Extracting instructions...")
    try:
        assignment_description = driver.find_element(By.ID, "assignment_show")
        description_html = assignment_description.get_attribute("outerHTML")
        description_text = assignment_description.text
        
        # Write markdown text instructions
        instructions_txt_path = os.path.join(target_dir, "instructions.txt")
        with open(instructions_txt_path, "w", encoding="utf-8") as f:
            f.write(description_text)
        print(f"Saved plain text instructions to: {instructions_txt_path}")
    except Exception as e:
        print(f"Could not extract description text: {e}")
        
    # Get all download links in the description
    print("Finding all file links on the page...")
    file_links = []
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        try:
            href = link.get_attribute("href") or ""
            text = link.text or ""
            # Canvas file links usually contain /files/ and /download
            if "/files/" in href:
                file_links.append((text, href))
                print(f"Found linked file: '{text}' -> {href}")
        except Exception:
            continue
            
    if not file_links:
        print("No files found directly linked on the assignment page. Checking for modules or files index...")
    else:
        # Copy cookies to requests Session
        print("Extracting session cookies for direct download...")
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
            
        print(f"Downloading {len(file_links)} files...")
        downloaded = []
        for name, url in file_links:
            # Clean filename from url or name
            # e.g. https://canvas.ucsd.edu/courses/12345/files/67890/download?wrap=1
            # We can request the URL head or just fetch it and read headers
            try:
                # Remove query params for cleaner download URL
                clean_url = url.split('?')[0]
                if not clean_url.endswith('/download'):
                    if clean_url.endswith('/'):
                        clean_url = clean_url + 'download'
                    else:
                        clean_url = clean_url + '/download'
                
                print(f"Downloading: {name} from {clean_url} ...")
                response = session.get(clean_url, stream=True, allow_redirects=True)
                
                # Try to get filename from content-disposition header
                filename = ""
                if "content-disposition" in response.headers:
                    cd = response.headers["content-disposition"]
                    filenames = re.findall(r"filename\*=UTF-8''(.+)|filename=\"(.+?)\"|filename=(.+)", cd)
                    if filenames:
                        # Extract first non-empty group
                        filename = next(f for f in filenames[0] if f)
                        # URL decode
                        import urllib.parse
                        filename = urllib.parse.unquote(filename)
                
                if not filename:
                    # Fallback to a name based on the text or URL
                    filename = name.strip().replace(" ", "_")
                    # Remove invalid characters
                    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
                    if not filename:
                        filename = url.split('/')[-2]
                
                filepath = os.path.join(target_dir, filename)
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            
                print(f"Successfully saved to: {filepath}")
                downloaded.append(filename)
            except Exception as e:
                print(f"Failed to download {name}: {e}")
                
        print(f"\nCompleted! Downloaded {len(downloaded)} files to {target_dir}:")
        for f in downloaded:
            print(f" - {f}")
            
    print("\nBrowser task completed! You can return to the CLI.")

if __name__ == "__main__":
    main()
