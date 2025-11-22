from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import sys

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_alert():
    """Demonstrate handling alert dialogs."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes with dialogs
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Set up dialog handler BEFORE clicking
            dialog_handled = False
            def handle_dialog(dialog):
                nonlocal dialog_handled
                print(f"✓ Alert dialog: {dialog.message}")
                dialog.accept()
                dialog_handled = True
            
            # Register handler before triggering
            page.on("dialog", handle_dialog)
            
            # Now trigger the alert
            page.click("button:has-text('Show Alert')")
            
            # Small wait to ensure dialog is handled
            page.wait_for_timeout(200)
            
            if dialog_handled:
                print("✓ Alert handled successfully")
        finally:
            if browser:
                browser.close()

def test_confirm():
    """Demonstrate handling confirm dialogs."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes with dialogs
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Set up dialog handler before triggering
            dialog_handled = False
            def handle_dialog(dialog):
                nonlocal dialog_handled
                print(f"✓ Confirm dialog: {dialog.message}")
                dialog.accept()
                dialog_handled = True
            
            # Register handler before triggering
            page.on("dialog", handle_dialog)
            page.click("button:has-text('Show Confirm')")
            page.wait_for_timeout(200)
            
            if dialog_handled:
                print("✓ Confirm handled successfully")
        finally:
            if browser:
                browser.close()

def test_prompt():
    """Demonstrate handling prompt dialogs."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes with dialogs
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Set up dialog handler before triggering
            dialog_handled = False
            def handle_dialog(dialog):
                nonlocal dialog_handled
                print(f"✓ Prompt dialog: {dialog.message}")
                dialog.accept("John Doe")
                dialog_handled = True
            
            # Register handler before triggering
            page.on("dialog", handle_dialog)
            page.click("button:has-text('Show Prompt')")
            page.wait_for_timeout(200)
            
            if dialog_handled:
                print("✓ Prompt handled successfully")
        finally:
            if browser:
                browser.close()

def test_dialog_info():
    """Demonstrate getting dialog information."""
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes with dialogs
            # Chromium on macOS has known issues with dialog handling after multiple dialogs
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Set up dialog handler to capture information
            dialog_info = {}
            def handle_dialog(dialog):
                dialog_info["type"] = dialog.type
                dialog_info["message"] = dialog.message
                dialog.accept()
            
            # Register handler before triggering
            page.on("dialog", handle_dialog)
            page.click("button:has-text('Show Alert')")
            page.wait_for_timeout(200)
            
            if dialog_info:
                print(f"✓ Dialog type: {dialog_info.get('type')}")
                print(f"✓ Dialog message: {dialog_info.get('message')}")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    print("Testing alert dialogs...")
    test_alert()
    time.sleep(0.5)  # Small delay between tests to ensure browser cleanup
    
    print("\nTesting confirm dialogs...")
    test_confirm()
    time.sleep(0.5)
    
    print("\nTesting prompt dialogs...")
    test_prompt()
    time.sleep(0.5)
    
    print("\nTesting dialog information...")
    test_dialog_info()
    print("\nAll tests completed!")

