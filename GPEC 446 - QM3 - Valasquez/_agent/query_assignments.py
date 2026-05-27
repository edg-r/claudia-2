import sqlite3

def main():
    conn = sqlite3.connect('/Users/edgar/Documents/01 Projects/Claudia/_claudia/claudia.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, due_date, status, weight FROM assignments WHERE course_id = 3")
    print("ASSIGNMENTS:")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()

if __name__ == "__main__":
    main()
