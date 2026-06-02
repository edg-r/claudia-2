import sqlite3

def main():
    conn = sqlite3.connect('/Users/edgar/Documents/000 Files/_claudia/claudia.db')
    cursor = conn.cursor()
    
    print("COURSES:")
    cursor.execute("SELECT * FROM courses")
    for row in cursor.fetchall():
        print(row)
        
    print("\nASSIGNMENTS:")
    cursor.execute("SELECT * FROM assignments WHERE course_id = 3")
    for row in cursor.fetchall():
        print(row)
        
    print("\nFILES:")
    cursor.execute("SELECT * FROM files WHERE course_id = 3")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()

if __name__ == "__main__":
    main()
