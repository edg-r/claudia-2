import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    url = "https://canvas.ucsd.edu"
    print(f"Navigating to dashboard: {url}")
    driver.get(url)
    time.sleep(5)
    
    # List all links that look like courses
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(links)} links on Dashboard:")
    for link in links:
        try:
            text = link.text or ""
            href = link.get_attribute("href") or ""
            if href and "courses/" in href:
                print(f" - '{text.strip()}' -> {href}")
        except Exception:
            continue

if __name__ == "__main__":
    main()
