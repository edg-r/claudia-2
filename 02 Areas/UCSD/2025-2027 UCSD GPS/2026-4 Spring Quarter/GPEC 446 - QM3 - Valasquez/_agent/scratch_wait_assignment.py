import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    print("Monitoring active tab for 60 seconds. Please navigate to the GPEC 446 Data Project page in your browser...")
    start_time = time.time()
    last_url = ""
    while time.time() - start_time < 60:
        try:
            curr_url = driver.current_url or ""
            title = driver.title or ""
            if curr_url != last_url:
                print(f"URL Changed -> Title: '{title}' | URL: {curr_url}")
                last_url = curr_url
                if "assignments/" in curr_url and any(c.isdigit() for c in curr_url.split('/')[-1]):
                    print(f"SUCCESS: Detected specific assignment page: {curr_url}")
                    break
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(3)

if __name__ == "__main__":
    main()
