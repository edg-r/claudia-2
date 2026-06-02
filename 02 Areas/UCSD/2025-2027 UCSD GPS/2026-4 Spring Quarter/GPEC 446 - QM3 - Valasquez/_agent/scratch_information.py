import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    url = "https://canvas.ucsd.edu/courses/74851/pages/information"
    print(f"Navigating to information page: {url}")
    driver.get(url)
    time.sleep(5)
    
    # Print the title and content
    print(f"Page Title: {driver.title}")
    
    try:
        content = driver.find_element(By.CLASS_NAME, "show-content")
        print("\nPage Content:")
        print(content.text)
    except Exception as e:
        try:
            content = driver.find_element(By.ID, "wiki_page_show")
            print("\nPage Content (wiki_page_show):")
            print(content.text)
        except Exception as e2:
            print(f"Could not read content: {e2}")
            
    # List links
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"\nFound {len(links)} links:")
    for link in links:
        try:
            text = link.text or ""
            href = link.get_attribute("href") or ""
            if href and text.strip():
                print(f" - '{text.strip()}' -> {href}")
        except Exception:
            continue

if __name__ == "__main__":
    main()
