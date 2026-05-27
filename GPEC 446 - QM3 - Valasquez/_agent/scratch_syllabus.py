import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    syllabus_url = "https://canvas.ucsd.edu/courses/74851/assignments/syllabus"
    print(f"Navigating to syllabus: {syllabus_url}")
    driver.get(syllabus_url)
    time.sleep(3)
    
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(links)} links on the page:")
    for link in links:
        try:
            text = link.text or ""
            href = link.get_attribute("href") or ""
            if href and text.strip():
                if "project" in text.lower() or "data" in text.lower() or "final" in text.lower():
                    print(f" - '{text.strip()}' -> {href}")
        except Exception:
            continue
            
    # Print the syllabus text or content
    try:
        content = driver.find_element(By.ID, "course_syllabus_body")
        print("\nSyllabus Content Snippet:")
        print(content.text[:1000])
    except Exception as e:
        print(f"Could not read syllabus content: {e}")

if __name__ == "__main__":
    main()
