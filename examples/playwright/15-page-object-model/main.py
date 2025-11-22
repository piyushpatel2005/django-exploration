from playwright.sync_api import sync_playwright
from pages.home_page import HomePage

def test_home_page():
    """Test using Page Object Model."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Use page object
        home_page = HomePage(page)
        home_page.goto()
        
        heading_text = home_page.get_heading_text()
        print(f"✓ Heading: {heading_text}")
        
        paragraph_count = home_page.get_paragraph_count()
        print(f"✓ Paragraphs: {paragraph_count}")
        
        browser.close()

if __name__ == "__main__":
    test_home_page()

