# Interacting with Elements

Once you've located elements, the next step is interacting with them. This tutorial covers clicking, typing, selecting, and other interactions with web elements.

## Overview

Playwright provides methods for various user interactions:
- Clicking elements
- Typing text
- Filling forms
- Selecting dropdowns and checkboxes
- Keyboard shortcuts
- Mouse actions (hover, drag, etc.)

## Clicking Elements

The most common interaction is clicking:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_clicking():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url(), wait_until="load")
        
            # Prevent form submission to avoid navigation
            page.evaluate("document.getElementById('test-form').addEventListener('submit', e => e.preventDefault())")
        
            # Click a button
            button = page.locator("button[type='submit']")
            button.wait_for(state="visible")
            button.first.click()
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_clicking()
```

### Click Options

You can specify various click options:

```python
# Click with modifiers
page.locator("button").click(modifiers=["Shift"])

# Double click
page.locator("button").dblclick()

# Right click
page.locator("button").click(button="right")

# Click at specific position
page.locator("button").click(position={"x": 10, "y": 20})

# Force click (even if element is not visible)
page.locator("button").click(force=True)
```

## Typing Text

Type text into input fields:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_typing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url(), wait_until="domcontentloaded")
        
            # Wait for the specific input to be ready
            name_input = page.locator("input[name='name']")
            name_input.wait_for(state="visible", timeout=10000)
        
            # Click on the input first to ensure it's focused and ready
            name_input.first.click()
        time.sleep(0.1)
        
            # Now fill it
            name_input.first.fill("Playwright Test")
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_typing()
```

### Fill vs Type

- **`fill()`**: Clears the field and types text quickly (recommended)
- **`type()`**: Simulates individual key presses (slower, more realistic)

```python
# Fill - clears and types quickly
input_field.fill("Hello World")

# Type - simulates typing character by character
input_field.type("Hello World", delay=50)  # 50ms delay between keys
```

## Filling Forms

Fill multiple form fields:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_filling_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url(), wait_until="domcontentloaded")
            
            # Prevent form submission to avoid navigation
            page.evaluate("document.getElementById('test-form').addEventListener('submit', e => e.preventDefault())")
        
        # Fill text inputs
            page.get_by_label("Name:").fill("John Doe")
            page.get_by_label("Email:").fill("john@example.com")
        
        # Select dropdown
            page.select_option("select#country", "us")
        
        # Check checkbox
            page.get_by_label("Subscribe to newsletter").check()
        
        # Select radio button
        page.get_by_label("Option 1").check()
        
        # Submit form
        page.locator("button[type='submit']").click()
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_filling_form()
```

## Selecting Dropdowns

Select options from dropdown menus:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_select_dropdown():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url())
        
        # Select by value
        page.select_option("select#country", value="us")
        
        # Select by label
        page.select_option("select#country", label="United States")
        
        # Select by index
            page.select_option("select#country", index=1)  # Skip first empty option
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_select_dropdown()
```

## Checkboxes and Radio Buttons

Handle checkboxes and radio buttons:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_checkboxes_radio():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url())
        
        # Check a checkbox
        page.get_by_label("Subscribe to newsletter").check()
        
        # Uncheck a checkbox
        page.get_by_label("Subscribe to newsletter").uncheck()
        
        # Check if checked
            is_checked = page.get_by_label("Subscribe to newsletter").is_checked()
        
        # Select radio button
        page.get_by_label("Option 1").check()
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_checkboxes_radio()
```

## Keyboard Actions

Simulate keyboard actions:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_keyboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url(), wait_until="domcontentloaded")
        
            # Wait for the specific input to be ready
            email_input = page.locator("input[name='email']")
            email_input.wait_for(state="visible", timeout=10000)
        
            # Click on the input first to ensure it's focused and ready
            email_input.first.click()
        time.sleep(0.1)
        
            # Now use keyboard to type
            page.keyboard.type("test@example.com")
        
        # Keyboard shortcuts
        page.keyboard.press("Control+A")  # Select all
        page.keyboard.press("Control+C")  # Copy
        page.keyboard.press("Control+V")  # Paste
        
        # On Mac, use "Meta" instead of "Control"
        page.keyboard.press("Meta+A")
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_keyboard()
```

## Mouse Actions

Perform mouse actions:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_mouse_actions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url(), wait_until="load")
        
        # Hover over an element
            hover_btn = page.locator("#hover-btn")
            hover_btn.wait_for(state="visible")
            hover_btn.first.hover()
        
        # Drag and drop
        source = page.locator("#source")
        target = page.locator("#target")
        source.wait_for(state="visible")
        target.wait_for(state="visible")
            source.first.drag_to(target.first)
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_mouse_actions()
```

## Uploading Files

Handle file uploads (see the file-downloads tutorial for a complete example):

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_file_upload():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url())
        
            # Upload a file (if file input exists on page)
        file_input = page.locator("input[type='file']")
            if file_input.count() > 0:
        file_input.set_input_files("path/to/file.pdf")
        
        # Upload multiple files
        file_input.set_input_files([
            "path/to/file1.pdf",
            "path/to/file2.pdf"
        ])
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_file_upload()
```

## Clearing Input Fields

Clear input fields:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_clear_input():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url())
        
        # Clear an input field
            input_field = page.locator("input[name='name']")
        input_field.fill("")  # Method 1: Fill with empty string
        input_field.clear()   # Method 2: Use clear method
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_clear_input()
```

## Focus and Blur

Control focus on elements:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_focus_blur():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url(), wait_until="domcontentloaded")
        
        # Wait for input to be ready
            input_field = page.locator("input[name='name']")
        input_field.wait_for(state="visible")
        
        # Focus on an element (clicking first helps ensure it's ready)
        input_field.first.click()
        time.sleep(0.1)
        input_field.focus()
        
        # Blur (remove focus)
        input_field.blur()
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_focus_blur()
```

## Scroll Actions

Scroll elements into view:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_scroll():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        try:
        page = browser.new_page()
            page.goto(get_file_url(), wait_until="load")
        
        # Scroll element into view
            target = page.locator("#target")
            target.wait_for(state="attached")
            target.first.scroll_into_view_if_needed()
        
        # Scroll page
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        finally:
        browser.close()
            time.sleep(0.1)

if __name__ == "__main__":
    test_scroll()
```

## HTML Page for Testing

Here's the HTML page (`index.html`) used in the examples above:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interacting with Elements</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        form {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
        }
        input, select, textarea {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            margin: 10px 5px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #2980b9;
        }
        .draggable {
            width: 100px;
            height: 100px;
            background-color: #e74c3c;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: move;
        }
        #target {
            width: 200px;
            height: 200px;
            border: 2px dashed #3498db;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Interacting with Elements</h1>
    
    <form id="test-form">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" placeholder="Enter your name">
        
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" placeholder="Enter your email">
        
        <label for="country">Country:</label>
        <select id="country" name="country">
            <option value="">Select a country</option>
            <option value="us">United States</option>
            <option value="uk">United Kingdom</option>
            <option value="ca">Canada</option>
        </select>
        
        <label>
            <input type="checkbox" id="subscribe" name="subscribe">
            Subscribe to newsletter
        </label>
        
        <label>
            <input type="radio" name="option" value="option1" checked>
            Option 1
        </label>
        <label>
            <input type="radio" name="option" value="option2">
            Option 2
        </label>
        
        <button type="submit">Submit Form</button>
        <button type="button" id="clear-btn">Clear</button>
    </form>
    
    <div>
        <button id="hover-btn">Hover over me</button>
    </div>
    
    <div class="draggable" id="source">Drag me</div>
    <div id="target">Drop here</div>
    
    <script>
        document.getElementById('hover-btn').addEventListener('mouseenter', function() {
            this.textContent = 'Hovered!';
        });
    </script>
</body>
</html>
```

## Best Practices

1. **Use `fill()` for text inputs**: It's faster and more reliable than `type()`
2. **Use role-based locators**: More stable and accessible
3. **Wait for elements**: Playwright auto-waits, but be explicit when needed - use `wait_for(state="visible")` before interacting
4. **Click before fill/focus**: For input fields, clicking first before filling or focusing helps ensure the element is ready and stable
5. **Use proper wait strategies**: For local files (`file://` URLs), use `wait_until="domcontentloaded"` for faster loading
6. **Prevent unwanted navigation**: If clicking submit buttons, prevent form submission to avoid page navigation
7. **Close browsers properly**: Always close browsers in a `finally` block to ensure cleanup even if errors occur
8. **Add small delays**: Small delays (0.1-0.2s) after clicking or focusing can help ensure stability, especially on macOS
9. **Add delays between tests**: When running multiple tests sequentially, add delays between them to ensure browsers are fully closed

### Running Multiple Tests

When running multiple tests, you can either:

**Option 1: Separate browser instances (more reliable on macOS)**
```python
def test_one():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            # ... test code ...
        finally:
            browser.close()
            time.sleep(0.1)  # Small delay to ensure browser is fully closed

def test_two():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            # ... test code ...
        finally:
            browser.close()
            time.sleep(0.1)

# Run tests with delays between them
test_one()
time.sleep(0.3)
test_two()
```

**Option 2: Single browser instance (more efficient)**
```python
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    try:
        # Test 1
        page = browser.new_page()
        page.goto(url)
        # ... test code ...
        page.close()
        
        # Test 2
        page = browser.new_page()
        page.goto(url)
        # ... test code ...
        page.close()
    finally:
        browser.close()
```

## Next Steps

Now that you can interact with elements, learn about:
- Waiting strategies for elements
- Assertions and expectations
- Handling dynamic content

