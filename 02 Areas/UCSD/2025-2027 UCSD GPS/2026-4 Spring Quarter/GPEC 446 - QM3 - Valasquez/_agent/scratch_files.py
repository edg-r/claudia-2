import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    files_url = "https://canvas.ucsd.edu/courses/74851/files"
    print(f"Navigating to files page: {files_url}")
    driver.get(files_url)
    time.sleep(5) # Give it plenty of time to load the files tree
    
    # Let's find elements that might contain filenames or text
    elements = driver.find_elements(By.CLASS_NAME, "ef-name-col")
    print(f"Found {len(elements)} items in the files tree:")
    for el in elements:
        try:
            print(f" - {el.text.strip()}")
        except Exception:
            continue
            
    # Also find all a tags that might be file downloads
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(links)} links on the files page:")
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
