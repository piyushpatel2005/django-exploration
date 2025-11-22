from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_spa_waiting():
    """Demonstrate testing SPAs."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Wait for network to be idle (SPA loaded)
        page.wait_for_load_state("networkidle")
        
        # Click button to load dynamic content
        page.click("button:has-text('Load Content Dynamically')")
        page.wait_for_selector("#content", state="visible")
        print("✓ SPA dynamic content loaded")
        
        browser.close()

def test_geolocation():
    """Demonstrate geolocation testing."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        context = browser.new_context(
            geolocation={"latitude": 40.7128, "longitude": -74.0060},
            permissions=["geolocation"]
        )
        page = context.new_page()
        page.goto(get_file_url())
        
        # Click button to get location
        page.click("button:has-text('Get Location')")
        page.wait_for_timeout(1000)
        print("✓ Geolocation configured and tested")
        
        browser.close()

if __name__ == "__main__":
    print("Testing SPA waiting...")
    test_spa_waiting()
    print("\nTesting geolocation...")
    test_geolocation()
    print("\nAll tests completed!")

