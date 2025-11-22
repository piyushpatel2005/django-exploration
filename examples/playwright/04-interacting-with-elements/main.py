from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_clicking():
    """Demonstrate clicking elements."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Click a button
        button = page.locator("button[type='submit']")
        if button.count() > 0:
            button.first.click()
            print("✓ Clicked button")
        
        browser.close()

def test_typing():
    """Demonstrate typing text."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Find input field and type
        name_input = page.locator("input[name='name']")
        if name_input.count() > 0:
            name_input.first.fill("Playwright Test")
            print("✓ Filled name input")
            page.wait_for_timeout(1000)
        
        browser.close()

def test_keyboard():
    """Demonstrate keyboard actions."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Focus on input and type
        email_input = page.locator("input[name='email']")
        if email_input.count() > 0:
            email_input.first.focus()
            page.keyboard.type("test@example.com")
            print("✓ Typed email using keyboard")
        
        browser.close()

def test_mouse_hover():
    """Demonstrate mouse hover."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Hover over button
        hover_btn = page.locator("#hover-btn")
        if hover_btn.count() > 0:
            hover_btn.first.hover()
            print("✓ Hovered over button")
            page.wait_for_timeout(1000)  # Wait to see hover effect
        
        browser.close()

def test_scroll():
    """Demonstrate scrolling."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Scroll element into view
        target = page.locator("#target")
        if target.count() > 0:
            target.first.scroll_into_view_if_needed()
            print("✓ Scrolled element into view")
        
        browser.close()

if __name__ == "__main__":
    print("Testing clicking...")
    test_clicking()
    print("\nTesting typing...")
    test_typing()
    print("\nTesting keyboard...")
    test_keyboard()
    print("\nTesting mouse hover...")
    test_mouse_hover()
    print("\nTesting scroll...")
    test_scroll()
    print("\nAll tests completed!")

