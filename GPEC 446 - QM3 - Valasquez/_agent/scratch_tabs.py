import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    handles = driver.window_handles
    print(f"Found {len(handles)} window/tab handles:")
    for handle in handles:
        try:
            driver.switch_to.window(handle)
            print(f" - Handle: {handle} | Title: {driver.title} | URL: {driver.current_url}")
        except Exception as e:
            print(f" - Error checking handle {handle}: {e}")

if __name__ == "__main__":
    main()
