import sqlite3

def main():
    conn = sqlite3.connect('_claudia/claudia.db')
    cursor = conn.cursor()
    
    # We will define a helper function to insert a grade
    def insert_grade(course_id, assignment_id, score, notes):
        # Check if already exists
        cursor.execute("SELECT id FROM grades WHERE course_id = ? AND assignment_id = ?", (course_id, assignment_id))
        g_row = cursor.fetchone()
        if g_row:
            cursor.execute("UPDATE grades SET score = ?, notes = ?, date_recorded = date('now') WHERE id = ?", (score, notes, g_row[0]))
            print(f"  Updated grade for Course {course_id}, Assignment {assignment_id} to {score}")
        else:
            cursor.execute("INSERT INTO grades (course_id, assignment_id, score, weight, notes, date_recorded) VALUES (?, ?, ?, ?, ?, date('now'))", (course_id, assignment_id, score, None, notes))
            print(f"  Inserted new grade for Course {course_id}, Assignment {assignment_id} -> {score}")

    print("Syncing verified grades to claudia.db...")

    # 1. GPCO 403 — International Economics (course_id=1)
    insert_grade(1, 1, "14.1/17.0", "Mean: 16.17. High: 17.0. Low: 14.0.") # CC1
    insert_grade(1, 2, "4.5/5.0", "Mean: 4.68. High: 5.0. Low: 1.5.")    # DB1
    insert_grade(1, 3, "10.0/12.0", "Mean: 11.79. High: 12.0. Low: 10.0.") # CC2
    insert_grade(1, 4, "10.0/10.0", "Mean: 9.49. High: 10.0. Low: 7.0.")   # CC3
    insert_grade(1, 6, "10.0/10.0", "Mean: 9.79. High: 10.0. Low: 8.0.")   # CC4
    insert_grade(1, 5, "95.0%", "Reported by Edgar. Standard weight: 30%.") # Midterm

    # 2. GPCO 410 — International Politics & Security (course_id=2)
    insert_grade(2, 14, "90.0/100.0", "Memo Second Gulf War. Mean: 90.81. High: 96.0. Low: 86.0.") # Memo BLUE
    insert_grade(2, 15, "86.0/100.0", "Memo Myanmar Coup. Mean: 90.94. High: 100.0. Low: 76.0.")    # Memo ORANGE
    insert_grade(2, 18, "100.0/100.0", "Reported by Edgar. Standard weight: 30%.") # Midterm Exam

    # 3. GPEC 446 — Quantitative Methods 3 (course_id=3)
    insert_grade(3, 10, "20.5/25.0", "Homework I: Opportunity Atlas. Mean: 22.46. High: 25.0. Low: 13.5.") # HW1

    # 4. GPPS 463 — Politics of Southeast Asia (course_id=5)
    insert_grade(5, 22, "14.0/20.0", "Midterm Exam 1 (Apr 20). Mean: 15.91. High: 19.0. Low: 8.5.") # Midterm 1
    insert_grade(5, 23, "16.25/22.0", "Midterm Exam 2 (May 11). Mean: 17.54. High: 22.0. Low: 11.5.") # Midterm 2

    conn.commit()
    conn.close()
    print("Database sync completed successfully!")

if __name__ == "__main__":
    main()
