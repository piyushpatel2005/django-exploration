from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_browser_options():
    """Demonstrate browser configuration options."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # Set headless=False to see browser window
            slow_mo=500  # Slow down by 500ms
        )
        page = browser.new_page()
        page.goto(get_file_url())
        print("✓ Browser configured with options")
        browser.close()

def test_viewport_config():
    """Demonstrate viewport configuration."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        page.goto(get_file_url())
        
        viewport_size = context.viewport_size
        print(f"✓ Viewport: {viewport_size['width']}x{viewport_size['height']}")
        
        browser.close()

def test_timeout_config():
    """Demonstrate timeout configuration."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Set default timeout
        page.set_default_timeout(10000)
        
        page.goto(get_file_url())
        print("✓ Timeout configured")
        
        browser.close()

if __name__ == "__main__":
    print("Testing browser options...")
    test_browser_options()
    print("\nTesting viewport config...")
    test_viewport_config()
    print("\nTesting timeout config...")
    test_timeout_config()
    print("\nAll tests completed!")

