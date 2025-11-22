# Handling Alerts and Dialogs

Web applications often use alerts, confirmations, and prompts to interact with users. This tutorial covers how to handle these dialogs in Playwright tests.

## Overview

Playwright can handle:
- **Alert dialogs**: Simple OK dialogs
- **Confirm dialogs**: OK/Cancel dialogs
- **Prompt dialogs**: Input dialogs
- **File upload dialogs**: File selection dialogs

## Alert Dialogs

Handle simple alert dialogs:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_alert():
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

if __name__ == "__main__":
    test_alert()
```

## Confirm Dialogs

Handle confirm dialogs (OK/Cancel):

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_confirm():
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
                dialog.accept()  # Or use dialog.dismiss() to cancel
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

if __name__ == "__main__":
    test_confirm()
```

## Prompt Dialogs

Handle prompt dialogs with input:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_prompt():
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
                dialog.accept("John Doe")  # Provide input value
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

if __name__ == "__main__":
    test_prompt()
```

## Important: Handler Setup Order

**Always set up the dialog handler BEFORE triggering the dialog.** This ensures the handler is ready when the dialog appears:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_handler_order():
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
            
            # Step 1: Set up handler FIRST
            def handle_dialog(dialog):
                print(f"Dialog message: {dialog.message}")
                print(f"Dialog type: {dialog.type}")
                dialog.accept()
            
            page.on("dialog", handle_dialog)
            
            # Step 2: THEN trigger the dialog
            page.click("button:has-text('Show Alert')")
            page.wait_for_timeout(200)
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_handler_order()
```

## Dialog Information

Get information from dialogs:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_dialog_info():
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
    test_dialog_info()
```

## macOS Compatibility Note

**Important for macOS users**: Chromium on macOS has known issues with dialog handling, especially after handling multiple dialogs. If you encounter crashes:

1. **Use Firefox or WebKit** for dialog tests:
   ```python
   browser = p.firefox.launch(headless=True)  # More stable on macOS
   # or
   browser = p.webkit.launch(headless=True)
   ```

2. **Add delays between tests** when running multiple dialog tests:
   ```python
   import time
   test_alert()
   time.sleep(0.5)  # Delay between tests
   test_confirm()
   ```

3. **Use try/finally blocks** to ensure proper cleanup:
   ```python
   try:
       # test code
   finally:
       browser.close()
   ```

## File Upload Dialogs

Handle file upload dialogs (covered in more detail in File Downloads tutorial):

```python
from playwright.sync_api import sync_playwright

def test_file_upload_dialog():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Set files before clicking upload button
        file_input = page.locator("input[type='file']")
        file_input.set_input_files("path/to/file.pdf")
        
        # Or handle file chooser
        with page.expect_file_chooser() as fc_info:
            page.click("button#upload")
        file_chooser = fc_info.value
        file_chooser.set_files("path/to/file.pdf")
        
        browser.close()

if __name__ == "__main__":
    test_file_upload_dialog()
```

## Best Practices

1. **Set up handlers before actions**: Register dialog handlers BEFORE clicking buttons that trigger dialogs
2. **Use try/finally blocks**: Ensure browser cleanup even if errors occur
3. **Handle all dialog types**: Alert, confirm, and prompt
4. **Verify dialog messages**: Check that the correct dialog appeared
5. **Add small delays**: Use `wait_for_timeout(200)` after triggering dialogs to ensure they're handled
6. **macOS compatibility**: Use Firefox or WebKit for dialog tests on macOS to avoid Chromium crashes
7. **Add delays between tests**: When running multiple dialog tests, add delays between them

## Common Patterns

```python
# Pattern 1: Simple accept with handler
def handle_dialog(dialog):
    print(f"Dialog: {dialog.message}")
    dialog.accept()

page.on("dialog", handle_dialog)
page.click("button")

# Pattern 2: Accept with message check
def handle_dialog(dialog):
    if "confirm" in dialog.message.lower():
        dialog.accept()
    else:
        dialog.dismiss()

page.on("dialog", handle_dialog)
page.click("button")

# Pattern 3: Capture dialog information
dialog_info = {}
def handle_dialog(dialog):
    dialog_info["message"] = dialog.message
    dialog_info["type"] = dialog.type
    dialog.accept()

page.on("dialog", handle_dialog)
page.click("button")
page.wait_for_timeout(200)
print(f"Dialog info: {dialog_info}")
```

## HTML Page for Testing

Here's the HTML page (`index.html`) used in the examples above:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Handling Alerts and Dialogs</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        button {
            padding: 10px 20px;
            margin: 10px 5px;
            background-color: #3498db;
            color: white;
            border: none;
            cursor: pointer;
        }
        .button-group {
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>Handling Alerts and Dialogs</h1>
    
    <div class="button-group">
        <button onclick="showAlert()">Show Alert</button>
        <button onclick="showConfirm()">Show Confirm</button>
        <button onclick="showPrompt()">Show Prompt</button>
    </div>
    
    <div id="result"></div>
    
    <script>
        function showAlert() {
            alert('Hello! This is an alert dialog.');
        }
        
        function showConfirm() {
            const result = confirm('Are you sure?');
            document.getElementById('result').textContent = 'Confirm result: ' + result;
        }
        
        function showPrompt() {
            const result = prompt('What is your name?', 'John Doe');
            document.getElementById('result').textContent = 'Prompt result: ' + (result || 'Cancelled');
        }
    </script>
</body>
</html>
```

## Next Steps

Now that you can handle dialogs, learn about:
- Working with frames and iframes
- Navigation and URL handling
- Cookies and storage management

