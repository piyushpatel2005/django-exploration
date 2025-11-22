from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_example():
    """Simple test that navigates to local HTML file and verifies the title."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Verify the page title
        assert page.title() == "First Playwright Test"
        print(f"✓ Page title verified: {page.title()}")
        
        browser.close()

def test_multiple_browsers():
    """Test the same page in different browsers."""
    browsers = ['chromium', 'firefox', 'webkit']
    
    with sync_playwright() as p:
        for browser_name in browsers:
            browser_type = getattr(p, browser_name)
            browser = browser_type.launch(headless=True)  # Set headless=False to see browser window
            page = browser.new_page()
            page.goto(get_file_url())
            print(f"✓ {browser_name.capitalize()}: {page.title()}")
            browser.close()

def test_page_content():
    """Test page content and elements."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Verify page loaded
        assert "First Playwright Test" in page.title()
        print(f"✓ Page title: {page.title()}")
        
        # Check for heading
        heading = page.locator("h1").first
        if heading.is_visible():
            print(f"✓ Heading found: {heading.text_content()}")
        
        browser.close()

if __name__ == "__main__":
    print("Running first Playwright test...")
    test_example()
    print("\nTesting multiple browsers...")
    test_multiple_browsers()
    print("\nTesting page content...")
    test_page_content()
    print("\nAll tests completed!")

