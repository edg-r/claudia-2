import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    url = "https://canvas.ucsd.edu/courses/74851/assignments"
    print(f"Navigating to assignments: {url}")
    driver.get(url)
    print("Waiting 5 seconds for assignments to load...")
    time.sleep(5)
    
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(links)} links on the page:")
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
