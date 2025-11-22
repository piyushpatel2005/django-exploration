from playwright.sync_api import sync_playwright
from pathlib import Path

def main():
    """
    Simple script to verify Playwright installation.
    Opens a browser, navigates to local HTML file, and prints the page title.
    
    Note: Using headless=True by default for stability. 
    Change to headless=False if you want to see the browser window.
    """
    # Get the path to the HTML file in the same directory
    html_file = Path(__file__).parent / "index.html"
    file_url = f"file://{html_file.absolute()}"
    
    with sync_playwright() as p:
        # Launch browser in headless mode (more stable)
        # Change headless=False if you want to see the browser window
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(file_url)
        
        # Get and print the page title
        title = page.title()
        print(f"Page title: {title}")
        print("✓ Playwright is working correctly!")
        
        browser.close()

if __name__ == "__main__":
    main()

