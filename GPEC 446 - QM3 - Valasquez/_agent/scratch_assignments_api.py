import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])
        
    url = "https://canvas.ucsd.edu/api/v1/courses/74851/assignments"
    print(f"Querying Canvas Assignments API: {url}")
    try:
        r = session.get(url)
        print(f"Status: {r.status_code}")
        assignments = r.json()
        if isinstance(assignments, list):
            print(f"Found {len(assignments)} assignments:")
            for a in assignments:
                print(f" - ID: {a.get('id')} | Title: '{a.get('name')}' | Due: {a.get('due_at')} | Published: {a.get('published')}")
        else:
            print(f"Response is not a list: {assignments}")
    except Exception as e:
        print(f"Failed to fetch assignments: {e}")

if __name__ == "__main__":
    main()
