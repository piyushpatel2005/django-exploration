from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_clicking():
    """Demonstrate clicking elements."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
            page = browser.new_page()
            page.goto(get_file_url(), wait_until="load")
            
            # Prevent form submission to avoid navigation
            page.evaluate("document.getElementById('test-form').addEventListener('submit', e => e.preventDefault())")
            
            # Click a button
            button = page.locator("button[type='submit']")
            button.wait_for(state="visible")
            button.first.click()
            print("✓ Clicked button")
        finally:
            browser.close()
            time.sleep(0.1)  # Ensure browser is fully closed

def test_typing():
    """Demonstrate typing text."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
            page = browser.new_page()
            page.goto(get_file_url(), wait_until="domcontentloaded")
            
            # Wait for the specific input to be ready
            name_input = page.locator("input[name='name']")
            name_input.wait_for(state="visible", timeout=10000)
            
            # Click on the input first to ensure it's focused and ready
            name_input.first.click()
            time.sleep(0.1)
            
            # Now fill it
            name_input.first.fill("Playwright Test")
            print("✓ Filled name input")
        finally:
            browser.close()
            time.sleep(0.1)  # Ensure browser is fully closed

def test_keyboard():
    """Demonstrate keyboard actions."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
            page = browser.new_page()
            page.goto(get_file_url(), wait_until="domcontentloaded")
            
            # Wait for the specific input to be ready
            email_input = page.locator("input[name='email']")
            email_input.wait_for(state="visible", timeout=10000)
            
            # Click on the input first to ensure it's focused and ready
            email_input.first.click()
            time.sleep(0.1)
            
            # Now use keyboard to type
            page.keyboard.type("test@example.com")
            print("✓ Typed email using keyboard")
        finally:
            browser.close()
            time.sleep(0.1)  # Ensure browser is fully closed

def test_mouse_hover():
    """Demonstrate mouse hover."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
            page = browser.new_page()
            page.goto(get_file_url(), wait_until="load")
            
            # Hover over button
            hover_btn = page.locator("#hover-btn")
            hover_btn.wait_for(state="visible")
            hover_btn.first.hover()
            print("✓ Hovered over button")
        finally:
            browser.close()
            time.sleep(0.1)  # Ensure browser is fully closed

def test_scroll():
    """Demonstrate scrolling."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
            page = browser.new_page()
            page.goto(get_file_url(), wait_until="load")
            
            # Scroll element into view
            target = page.locator("#target")
            target.wait_for(state="attached")
            target.first.scroll_into_view_if_needed()
            print("✓ Scrolled element into view")
        finally:
            browser.close()
            time.sleep(0.1)  # Ensure browser is fully closed

if __name__ == "__main__":
    # Run each test with its own browser instance
    # This is more reliable on macOS where browser instances can have resource issues
    tests = [
        ("Testing clicking...", test_clicking),
        ("Testing typing...", test_typing),
        ("Testing keyboard...", test_keyboard),
        ("Testing mouse hover...", test_mouse_hover),
        ("Testing scroll...", test_scroll),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(test_name)
            test_func()
            passed += 1
            time.sleep(0.3)  # Delay between tests to ensure browser is fully closed
        except Exception as e:
            print(f"✗ {test_name} failed: {e}")
            failed += 1
            import traceback
            traceback.print_exc()
            time.sleep(0.3)  # Delay even on failure
    
    print(f"\nAll tests completed! Passed: {passed}, Failed: {failed}")

