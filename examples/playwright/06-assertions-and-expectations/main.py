from playwright.sync_api import sync_playwright, expect
from pathlib import Path
import re

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_basic_assertions():
    """Demonstrate basic assertions."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Assert element is visible
        heading = page.locator("h1")
        expect(heading).to_be_visible()
        print("✓ Element is visible")
        
        # Assert text content
        expect(heading).to_have_text("Assertions and Expectations Test Page")
        print("✓ Text matches")
        
        browser.close()

def test_text_assertions():
    """Demonstrate text assertions."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        heading = page.locator("h1")
        
        # Contains text
        expect(heading).to_contain_text("Assertions")
        print("✓ Contains text 'Assertions'")
        
        browser.close()

def test_url_assertions():
    """Demonstrate URL assertions."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        file_url = get_file_url()
        page.goto(file_url)
        
        # Check URL contains file path using regex
        expect(page).to_have_url(re.compile(r".*index\.html.*"))
        print("✓ URL matches")
        
        # Check title
        expect(page).to_have_title("Assertions and Expectations")
        print("✓ Title matches")
        
        browser.close()

def test_count_assertions():
    """Demonstrate count assertions."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        links = page.locator("a")
        
        # Check count is greater than 0
        # Note: to_have_count can accept a callable, but for simplicity, we check the actual count
        link_count = links.count()
        assert link_count > 0, f"Expected at least 1 link, but found {link_count}"
        print(f"✓ Found {link_count} links")
        
        browser.close()

def test_negated_assertions():
    """Demonstrate negated assertions."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Check that hidden element is not visible
        hidden_element = page.locator("#hidden-box")
        expect(hidden_element).not_to_be_visible()
        print("✓ Hidden element is not visible")
        
        browser.close()

if __name__ == "__main__":
    print("Testing basic assertions...")
    test_basic_assertions()
    print("\nTesting text assertions...")
    test_text_assertions()
    print("\nTesting URL assertions...")
    test_url_assertions()
    print("\nTesting count assertions...")
    test_count_assertions()
    print("\nTesting negated assertions...")
    test_negated_assertions()
    print("\nAll tests completed!")

