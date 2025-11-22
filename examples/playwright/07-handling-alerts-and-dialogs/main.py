from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_alert():
    """Demonstrate handling alert dialogs."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Listen for alert dialog
        dialog_handled = False
        def handle_dialog(dialog):
            nonlocal dialog_handled
            print(f"✓ Alert dialog: {dialog.message}")
            dialog.accept()
            dialog_handled = True
        
        page.on("dialog", handle_dialog)
        
        # Trigger alert
        page.click("button:has-text('Show Alert')")
        page.wait_for_timeout(500)
        
        if dialog_handled:
            print("✓ Alert handled successfully")
        
        browser.close()

def test_confirm():
    """Demonstrate handling confirm dialogs."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Accept confirm dialog
        def handle_dialog(dialog):
            print(f"✓ Confirm dialog: {dialog.message}")
            dialog.accept()
        
        page.on("dialog", handle_dialog)
        page.click("button:has-text('Show Confirm')")
        page.wait_for_timeout(500)
        
        browser.close()

def test_prompt():
    """Demonstrate handling prompt dialogs."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Handle prompt with input
        def handle_dialog(dialog):
            print(f"✓ Prompt dialog: {dialog.message}")
            dialog.accept("John Doe")
        
        page.on("dialog", handle_dialog)
        page.click("button:has-text('Show Prompt')")
        page.wait_for_timeout(500)
        
        browser.close()

def test_dialog_info():
    """Demonstrate getting dialog information."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        dialog_info = {}
        
        def handle_dialog(dialog):
            dialog_info["message"] = dialog.message
            dialog_info["type"] = dialog.type
            dialog.accept()
        
        page.on("dialog", handle_dialog)
        page.click("button:has-text('Show Alert')")
        page.wait_for_timeout(500)
        
        print(f"✓ Dialog type: {dialog_info.get('type')}")
        print(f"✓ Dialog message: {dialog_info.get('message')}")
        
        browser.close()

if __name__ == "__main__":
    print("Testing alert dialogs...")
    test_alert()
    print("\nTesting confirm dialogs...")
    test_confirm()
    print("\nTesting prompt dialogs...")
    test_prompt()
    print("\nTesting dialog information...")
    test_dialog_info()
    print("\nAll tests completed!")

