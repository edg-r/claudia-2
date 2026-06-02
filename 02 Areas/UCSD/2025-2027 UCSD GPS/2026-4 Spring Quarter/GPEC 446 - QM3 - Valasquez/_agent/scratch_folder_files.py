import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])
        
    for folder_id in [2591564, 2683482]:
        print(f"\nFetching files in Folder {folder_id}...")
        url = f"https://canvas.ucsd.edu/api/v1/folders/{folder_id}/files"
        try:
            r = session.get(url)
            print(f"Status: {r.status_code}")
            res = r.json()
            if isinstance(res, list):
                print(f"Found {len(res)} files:")
                for f in res:
                    print(f" - ID: {f.get('id')} | Name: '{f.get('display_name')}' | Size: {f.get('size')} | Created: {f.get('created_at')}")
            else:
                print(f"Response is not a list: {res}")
        except Exception as e:
            print(f"Failed to fetch files for folder {folder_id}: {e}")

if __name__ == "__main__":
    main()
