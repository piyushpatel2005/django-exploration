from playwright.sync_api import sync_playwright, expect
from pathlib import Path

def get_file_url(filename):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_navigate():
    """Demonstrate basic navigation."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Navigate to a URL
        file_url = get_file_url("page1.html")
        page.goto(file_url)
        
        print(f"✓ Current URL: {page.url[:50]}...")
        print(f"✓ Page title: {page.title()}")
        
        browser.close()

def test_history():
    """Demonstrate browser history navigation."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Navigate to first page
        page.goto(get_file_url("page1.html"))
        print(f"✓ Page 1 title: {page.title()}")
        
        # Navigate to second page
        page.goto(get_file_url("page2.html"))
        print(f"✓ Page 2 title: {page.title()}")
        
        # Go back
        page.go_back()
        print(f"✓ After back - title: {page.title()}")
        
        # Go forward
        page.go_forward()
        print(f"✓ After forward - title: {page.title()}")
        
        browser.close()

def test_reload():
    """Demonstrate reloading a page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url("page1.html"))
        
        initial_title = page.title()
        
        # Reload page
        page.reload()
        
        reloaded_title = page.title()
        print(f"✓ Initial title: {initial_title}")
        print(f"✓ Reloaded title: {reloaded_title}")
        
        browser.close()

def test_url_assertions():
    """Demonstrate URL assertions."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        file_url = get_file_url("page1.html")
        page.goto(file_url)
        
        # Assert URL contains page1.html
        expect(page).to_have_url(lambda url: "page1.html" in url)
        print("✓ URL assertion passed")
        
        # Assert title
        expect(page).to_have_title("Navigation Page 1")
        print("✓ Title assertion passed")
        
        browser.close()

if __name__ == "__main__":
    print("Testing navigation...")
    test_navigate()
    print("\nTesting browser history...")
    test_history()
    print("\nTesting reload...")
    test_reload()
    print("\nTesting URL assertions...")
    test_url_assertions()
    print("\nAll tests completed!")

