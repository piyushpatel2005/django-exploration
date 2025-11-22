from playwright.sync_api import sync_playwright
from pathlib import Path
import os

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_full_page_screenshot():
    """Demonstrate taking full page screenshots."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Take full page screenshot
        screenshot_path = "screenshot_full.png"
        page.screenshot(path=screenshot_path, full_page=True)
        
        if os.path.exists(screenshot_path):
            print(f"✓ Screenshot saved: {screenshot_path}")
        
        browser.close()

def test_element_screenshot():
    """Demonstrate taking element screenshots."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Screenshot of specific element
        heading = page.locator("h1")
        if heading.count() > 0:
            screenshot_path = "screenshot_element.png"
            heading.first.screenshot(path=screenshot_path)
            
            if os.path.exists(screenshot_path):
                print(f"✓ Element screenshot saved: {screenshot_path}")
        
        browser.close()

def test_screenshot_options():
    """Demonstrate screenshot options."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Screenshot with options
        screenshot_path = "screenshot_options.png"
        page.screenshot(
            path=screenshot_path,
            full_page=True,
            type="png"
        )
        
        if os.path.exists(screenshot_path):
            print(f"✓ Screenshot with options saved: {screenshot_path}")
        
        browser.close()

def test_pdf_generation():
    """Demonstrate PDF generation."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Generate PDF
        pdf_path = "page.pdf"
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True
        )
        
        if os.path.exists(pdf_path):
            print(f"✓ PDF saved: {pdf_path}")
        
        browser.close()

if __name__ == "__main__":
    print("Testing full page screenshot...")
    test_full_page_screenshot()
    print("\nTesting element screenshot...")
    test_element_screenshot()
    print("\nTesting screenshot options...")
    test_screenshot_options()
    print("\nTesting PDF generation...")
    test_pdf_generation()
    print("\nAll tests completed!")

