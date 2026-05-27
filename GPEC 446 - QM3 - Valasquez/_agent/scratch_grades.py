import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    url = "https://canvas.ucsd.edu/courses/74851/grades"
    print(f"Navigating to grades page: {url}")
    driver.get(url)
    time.sleep(5)
    
    # Locate assignments in the grades table
    # Canvas grades table rows typically contain class 'student_assignment'
    rows = driver.find_elements(By.CLASS_NAME, "student_assignment")
    print(f"Found {len(rows)} assignment rows:")
    for row in rows:
        try:
            # The assignment title is usually inside an anchor tag or th
            title_el = row.find_element(By.TAG_NAME, "a")
            title = title_el.text.strip()
            href = title_el.get_attribute("href") or ""
            print(f" - '{title}' -> {href}")
        except Exception:
            try:
                th = row.find_element(By.TAG_NAME, "th")
                print(f" - (No Link) '{th.text.strip()}'")
            except Exception:
                continue

if __name__ == "__main__":
    main()
