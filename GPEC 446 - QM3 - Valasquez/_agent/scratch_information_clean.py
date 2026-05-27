import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("Connected to Chrome!")
    except Exception as e:
        print(f"Error connecting: {e}")
        return
    
    url = "https://canvas.ucsd.edu/courses/74851/pages/information"
    print(f"Navigating to: {url}")
    driver.get(url)
    time.sleep(5)
    
    print(f"Current URL: {driver.current_url}")
    print(f"Page Title: {driver.title}")
    
    # Try different selectors to print page content
    for selector in ["show-content", "wiki_page_show", "content"]:
        try:
            el = driver.find_element(By.CLASS_NAME, selector)
            print(f"\nContent by class '{selector}':")
            print(el.text)
            break
        except Exception:
            try:
                el = driver.find_element(By.ID, selector)
                print(f"\nContent by ID '{selector}':")
                print(el.text)
                break
            except Exception:
                continue
    else:
        print("\nCould not find content elements. Dumping body text:")
        try:
            print(driver.find_element(By.TAG_NAME, "body").text[:2000])
        except Exception as e:
            print(f"Failed to dump body: {e}")
            
    # Print links
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
