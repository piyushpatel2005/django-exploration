from playwright.sync_api import sync_playwright
from pathlib import Path
import os

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_ci_mode():
    """Demonstrate CI mode configuration."""
    # Detect CI environment
    is_ci = os.getenv("CI") == "true"
    
    with sync_playwright() as p:
        # Run headless by default (True) for stability
        # In CI, always use headless=True. Set headless=False locally if you want to see the browser window
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(get_file_url())
        
        print(f"✓ Running in {'CI' if is_ci else 'local'} mode")
        print(f"✓ Headless: {is_ci}")
        print(f"✓ Page title: {page.title()}")
        
        browser.close()

if __name__ == "__main__":
    test_ci_mode()

