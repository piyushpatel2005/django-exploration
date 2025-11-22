from playwright.sync_api import sync_playwright, expect
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_descriptive_name():
    """Example of a test with a descriptive name."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Clear, focused assertion
        expect(page).to_have_title("Best Practices")
        print("✓ Test with descriptive name passed")
        
        browser.close()

def test_explicit_wait():
    """Example of using explicit waits instead of fixed timeouts."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Explicit wait for element
        heading = page.locator("h1")
        heading.wait_for(state="visible")
        
        # Then interact
        expect(heading).to_be_visible()
        print("✓ Explicit wait used")
        
        browser.close()

def test_focused_test():
    """Example of a focused test doing one thing."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Single focused assertion
        assert "Best Practices" in page.title()
        print("✓ Focused test passed")
        
        browser.close()

if __name__ == "__main__":
    print("Testing best practices...")
    test_descriptive_name()
    print("\nTesting explicit waits...")
    test_explicit_wait()
    print("\nTesting focused tests...")
    test_focused_test()
    print("\nAll best practice examples completed!")

