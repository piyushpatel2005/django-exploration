from playwright.sync_api import sync_playwright
from pathlib import Path
import sys
import time

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_auto_wait():
    """Demonstrate Playwright's automatic waiting."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Playwright automatically waits for the element
            heading = page.locator("h1")
            print(f"✓ Auto-waited for element: {heading.text_content()}")
        finally:
            if browser:
                browser.close()

def test_wait_for_selector():
    """Demonstrate waiting for a selector."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Wait for element to be visible
            page.wait_for_selector("h1", state="visible")
            print("✓ Element is visible")
        finally:
            if browser:
                browser.close()

def test_wait_for_load_state():
    """Demonstrate waiting for load states."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            
            # Navigate and wait for load
            page.goto(get_file_url(), wait_until="load")
            print("✓ Page loaded")
            
            # Wait for network to be idle
            page.wait_for_load_state("networkidle")
            print("✓ Network idle")
        finally:
            if browser:
                browser.close()

def test_wait_for_timeout():
    """Demonstrate timeout waiting (use sparingly)."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Wait for 1 second
            page.wait_for_timeout(1000)
            print("✓ Waited for timeout")
        finally:
            if browser:
                browser.close()

def test_wait_for_dynamic_content():
    """Demonstrate waiting for dynamic content."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Click button to load dynamic content
            page.click("#load-btn")
            
            # Wait for dynamic content to appear
            page.wait_for_selector("#dynamic-content", state="visible")
            print("✓ Dynamic content loaded")
        finally:
            if browser:
                browser.close()

def test_wait_for_element_state():
    """Demonstrate waiting for element states."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            element = page.locator("h1")
            
            # Wait for element to be visible
            element.wait_for(state="visible")
            print("✓ Element is visible")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    print("Testing auto-wait...")
    test_auto_wait()
    time.sleep(0.5)  # Allow browser to fully close
    print("\nTesting wait for selector...")
    test_wait_for_selector()
    time.sleep(0.5)
    print("\nTesting wait for load state...")
    test_wait_for_load_state()
    time.sleep(0.5)
    print("\nTesting wait for timeout...")
    test_wait_for_timeout()
    time.sleep(0.5)
    print("\nTesting wait for dynamic content...")
    test_wait_for_dynamic_content()
    time.sleep(0.5)
    print("\nTesting wait for element state...")
    test_wait_for_element_state()
    print("\nAll tests completed!")

