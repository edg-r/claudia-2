import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    url = "https://canvas.ucsd.edu/courses/74851/external_tools/6633"
    print(f"Navigating to Gradescope: {url}")
    driver.get(url)
    print("Waiting 10 seconds for Gradescope LTI iframe to launch...")
    time.sleep(10)
    
    # Check if there is an iframe
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"Found {len(iframes)} iframes on the page:")
    for idx, iframe in enumerate(iframes):
        try:
            print(f" - Iframe {idx}: id={iframe.get_attribute('id')}, name={iframe.get_attribute('name')}, src={iframe.get_attribute('src')}")
        except Exception as e:
            print(f" - Error reading iframe {idx}: {e}")
            
    # Switch to the Gradescope iframe if it exists
    if iframes:
        try:
            driver.switch_to.frame(iframes[0])
            print("Switched to first iframe!")
            time.sleep(2)
        except Exception as e:
            print(f"Failed to switch to iframe: {e}")
            
    # Dump all text and links inside (or outside) the iframe
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(links)} links on the current frame:")
    for link in links:
        try:
            text = link.text or ""
            href = link.get_attribute("href") or ""
            if text.strip() or href:
                print(f" - '{text.strip()}' -> {href}")
        except Exception:
            continue
            
    # Print page text
    try:
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print("\nPage body text (first 1000 chars):")
        print(body_text[:1000])
    except Exception as e:
        print(f"Could not read body text: {e}")

if __name__ == "__main__":
    main()
