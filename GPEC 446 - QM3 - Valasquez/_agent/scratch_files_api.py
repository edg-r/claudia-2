import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("Connected to Chrome!")
    
    # Copy cookies
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])
        
    print("Fetching folders via Canvas REST API...")
    folders_url = "https://canvas.ucsd.edu/api/v1/courses/74851/folders"
    try:
        r = session.get(folders_url)
        print(f"Folders response status: {r.status_code}")
        folders = r.json()
        print(f"Found {len(folders)} folders:")
        for f in folders:
            print(f" - Folder ID: {f.get('id')} | Name: '{f.get('name')}' | Path: '{f.get('full_name')}'")
    except Exception as e:
        print(f"Failed to fetch folders: {e}")
        
    print("\nFetching root files via Canvas REST API...")
    files_url = "https://canvas.ucsd.edu/api/v1/courses/74851/files"
    try:
        r = session.get(files_url)
        print(f"Files response status: {r.status_code}")
        files = r.json()
        print(f"Found {len(files)} files in course:")
        for f in files:
            print(f" - File ID: {f.get('id')} | Name: '{f.get('display_name')}' | URL: {f.get('url')}")
    except Exception as e:
        print(f"Failed to fetch files: {e}")

if __name__ == "__main__":
    main()
