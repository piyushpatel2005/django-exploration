from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_css_selectors():
    """Demonstrate CSS selector locators."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # By tag name
        heading = page.locator("h1")
        print(f"✓ Found heading by tag: {heading.text_content()}")
        
        # By tag with CSS selector
        paragraph = page.locator("p")
        print(f"✓ Found paragraph: {paragraph.first.text_content()}")
        
        browser.close()

def test_text_locators():
    """Demonstrate text-based locators."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Locate by exact text
        heading = page.get_by_text("Locating Elements Test Page")
        print(f"✓ Found by exact text: {heading.text_content()}")
        
        # Locate by partial text
        link = page.get_by_text("More information", exact=False)
        if link.count() > 0:
            print(f"✓ Found link by partial text: {link.first.text_content()}")
        
        browser.close()

def test_role_locators():
    """Demonstrate role-based locators."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Locate by role
        heading = page.get_by_role("heading")
        if heading.count() > 0:
            print(f"✓ Found heading by role: {heading.first.text_content()}")
        
        # Find links by role
        links = page.get_by_role("link")
        print(f"✓ Found {links.count()} links by role")
        
        browser.close()

def test_chaining_locators():
    """Demonstrate chaining locators."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Chain locators
        body = page.locator("body")
        heading = body.locator("h1")
        print(f"✓ Chained locator found: {heading.text_content()}")
        
        # Get first/last
        paragraphs = page.locator("p")
        if paragraphs.count() > 0:
            print(f"✓ First paragraph: {paragraphs.first.text_content()}")
            print(f"✓ Last paragraph: {paragraphs.last.text_content()}")
        
        browser.close()

def test_multiple_elements():
    """Demonstrate working with multiple elements."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Get count of matching elements
        links = page.locator("a")
        count = links.count()
        print(f"✓ Found {count} links")
        
        # Get all text contents
        if count > 0:
            all_texts = links.all_text_contents()
            print(f"✓ All link texts: {all_texts}")
        
        browser.close()

if __name__ == "__main__":
    print("Testing CSS selectors...")
    test_css_selectors()
    print("\nTesting text locators...")
    test_text_locators()
    print("\nTesting role locators...")
    test_role_locators()
    print("\nTesting chaining locators...")
    test_chaining_locators()
    print("\nTesting multiple elements...")
    test_multiple_elements()
    print("\nAll tests completed!")

