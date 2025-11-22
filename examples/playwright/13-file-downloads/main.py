from playwright.sync_api import sync_playwright
from pathlib import Path
import os
import sys
import time

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_file_upload():
    """Demonstrate file upload using file chooser."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes with file operations
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Create a test file
            test_file = Path(__file__).parent / "test_upload.txt"
            with open(test_file, "w") as f:
                f.write("Test content")
            
            # Handle file chooser
            with page.expect_file_chooser() as fc_info:
                page.click("button:has-text('Upload File')")
            
            file_chooser = fc_info.value
            file_chooser.set_files(str(test_file))
            
            print("✓ File upload handled")
            
            # Cleanup
            if test_file.exists():
                test_file.unlink()
        finally:
            if browser:
                browser.close()

def test_download_info():
    """Demonstrate getting download information."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes with file operations
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Wait for download
            with page.expect_download() as download_info:
                page.click("a[href*='test-file.txt']")
            
            download = download_info.value
            
            filename = download.suggested_filename
            print(f"✓ Download filename: {filename}")
            print(f"✓ Download URL: {download.url}")
            
            # Save download
            download_path = Path(__file__).parent / "downloaded_file.txt"
            download.save_as(str(download_path))
            
            if download_path.exists():
                print("✓ File downloaded successfully")
                download_path.unlink()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    print("Testing file upload...")
    test_file_upload()
    time.sleep(0.5)  # Allow browser to fully close
    print("\nTesting download info...")
    test_download_info()
    print("\nAll tests completed!")

