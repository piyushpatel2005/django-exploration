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

def test_alert():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Listen for alert dialog
        page.on("dialog", lambda dialog: dialog.accept())
        
        # Trigger alert (example)
        page.evaluate("alert('Hello!')")
        
        browser.close()

if __name__ == "__main__":
    test_alert()
```

## Confirm Dialogs

Handle confirm dialogs (OK/Cancel):

```python
from playwright.sync_api import sync_playwright

def test_confirm():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Accept confirm dialog
        page.on("dialog", lambda dialog: dialog.accept())
        page.evaluate("confirm('Are you sure?')")
        
        # Or dismiss
        page.on("dialog", lambda dialog: dialog.dismiss())
        page.evaluate("confirm('Are you sure?')")
        
        browser.close()

if __name__ == "__main__":
    test_confirm()
```

## Prompt Dialogs

Handle prompt dialogs with input:

```python
from playwright.sync_api import sync_playwright

def test_prompt():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Handle prompt with input
        page.on("dialog", lambda dialog: dialog.accept("John Doe"))
        result = page.evaluate("prompt('What is your name?')")
        print(f"Result: {result}")
        
        browser.close()

if __name__ == "__main__":
    test_prompt()
```

## Using `page.wait_for_event()`

A better approach is to wait for the dialog event:

```python
from playwright.sync_api import sync_playwright

def test_dialog_wait():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Wait for dialog and handle it
        def handle_dialog(dialog):
            print(f"Dialog message: {dialog.message}")
            print(f"Dialog type: {dialog.type}")
            dialog.accept()
        
        page.on("dialog", handle_dialog)
        
        # Trigger dialog
        page.evaluate("alert('Test alert')")
        
        browser.close()

if __name__ == "__main__":
    test_dialog_wait()
```

## Dialog Information

Get information from dialogs:

```python
from playwright.sync_api import sync_playwright

def test_dialog_info():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        dialog_messages = []
        
        def handle_dialog(dialog):
            dialog_messages.append({
                "message": dialog.message,
                "type": dialog.type,
                "default_value": dialog.default_value
            })
            dialog.accept()
        
        page.on("dialog", handle_dialog)
        page.evaluate("alert('Hello World')")
        
        print(f"Dialog info: {dialog_messages}")
        
        browser.close()

if __name__ == "__main__":
    test_dialog_info()
```

## Before Dialog Handler

Handle dialogs before they appear:

```python
from playwright.sync_api import sync_playwright

def test_before_dialog():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Set up dialog handler before navigation
        page.on("dialog", lambda dialog: dialog.accept())
        
        page.goto("https://example.com")
        
        browser.close()

if __name__ == "__main__":
    test_before_dialog()
```

## File Upload Dialogs

Handle file upload dialogs (covered in more detail in File Downloads tutorial):

```python
from playwright.sync_api import sync_playwright

def test_file_upload_dialog():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/upload")
        
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

1. **Set up handlers before actions**: Register dialog handlers before triggering dialogs
2. **Use `wait_for_event()`**: For more control over dialog handling
3. **Handle all dialog types**: Alert, confirm, and prompt
4. **Verify dialog messages**: Check that the correct dialog appeared
5. **Clean up handlers**: Remove handlers when done to avoid interference

## Common Patterns

```python
# Pattern 1: Simple accept
page.on("dialog", lambda dialog: dialog.accept())

# Pattern 2: Accept with message check
page.on("dialog", lambda dialog: 
    dialog.accept() if "confirm" in dialog.message.lower() else dialog.dismiss()
)

# Pattern 3: Wait for specific dialog
with page.expect_dialog() as dialog_info:
    page.click("button")
dialog = dialog_info.value
dialog.accept()
```

## Next Steps

Now that you can handle dialogs, learn about:
- Working with frames and iframes
- Navigation and URL handling
- Cookies and storage management

