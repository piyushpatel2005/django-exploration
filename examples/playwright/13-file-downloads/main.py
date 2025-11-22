from playwright.sync_api import sync_playwright
from pathlib import Path
import os

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_file_upload():
    """Demonstrate file upload using file chooser."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Create a test file
        test_file = "test_upload.txt"
        with open(test_file, "w") as f:
            f.write("Test content")
        
        # Handle file chooser
        with page.expect_file_chooser() as fc_info:
            page.click("button")
        
        file_chooser = fc_info.value
        file_chooser.set_files(test_file)
        
        print("✓ File upload handled")
        
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        
        browser.close()

def test_download_info():
    """Demonstrate getting download information."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Wait for download
        with page.expect_download() as download_info:
            page.click("a[href*='test-file.txt']")
        
        download = download_info.value
        
        filename = download.suggested_filename()
        print(f"✓ Download filename: {filename}")
        print(f"✓ Download URL: {download.url}")
        
        # Save download
        download.save_as("downloaded_file.txt")
        
        if os.path.exists("downloaded_file.txt"):
            print("✓ File downloaded successfully")
            os.remove("downloaded_file.txt")
        
        browser.close()

if __name__ == "__main__":
    print("Testing file upload...")
    test_file_upload()
    print("\nTesting download info...")
    test_download_info()
    print("\nAll tests completed!")

