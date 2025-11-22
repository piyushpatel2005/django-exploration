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

def test_clicking():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Click a link
        link = page.get_by_text("More information")
        link.click()
        
        browser.close()

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

def test_typing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Type into an input field
        search_box = page.locator("input[type='search']")
        search_box.fill("Playwright")
        
        # Or use type (slower, simulates key presses)
        search_box.type("Playwright", delay=100)
        
        browser.close()

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

def test_filling_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/form")
        
        # Fill text inputs
        page.get_by_label("Name").fill("John Doe")
        page.get_by_label("Email").fill("john@example.com")
        
        # Select dropdown
        page.select_option("select#country", "USA")
        
        # Check checkbox
        page.get_by_label("Subscribe").check()
        
        # Select radio button
        page.get_by_label("Option 1").check()
        
        # Submit form
        page.locator("button[type='submit']").click()
        
        browser.close()

if __name__ == "__main__":
    test_filling_form()
```

## Selecting Dropdowns

Select options from dropdown menus:

```python
from playwright.sync_api import sync_playwright

def test_select_dropdown():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Select by value
        page.select_option("select#country", value="us")
        
        # Select by label
        page.select_option("select#country", label="United States")
        
        # Select by index
        page.select_option("select#country", index=0)
        
        # Select multiple options
        page.select_option("select#countries", ["us", "uk", "ca"])
        
        browser.close()

if __name__ == "__main__":
    test_select_dropdown()
```

## Checkboxes and Radio Buttons

Handle checkboxes and radio buttons:

```python
from playwright.sync_api import sync_playwright

def test_checkboxes_radio():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Check a checkbox
        page.get_by_label("Subscribe to newsletter").check()
        
        # Uncheck a checkbox
        page.get_by_label("Subscribe to newsletter").uncheck()
        
        # Check if checked
        is_checked = page.get_by_label("Subscribe").is_checked()
        
        # Select radio button
        page.get_by_label("Option 1").check()
        
        browser.close()

if __name__ == "__main__":
    test_checkboxes_radio()
```

## Keyboard Actions

Simulate keyboard actions:

```python
from playwright.sync_api import sync_playwright

def test_keyboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Press a key
        page.keyboard.press("Enter")
        page.keyboard.press("Escape")
        
        # Type text
        page.keyboard.type("Hello World")
        
        # Keyboard shortcuts
        page.keyboard.press("Control+A")  # Select all
        page.keyboard.press("Control+C")  # Copy
        page.keyboard.press("Control+V")  # Paste
        
        # On Mac, use "Meta" instead of "Control"
        page.keyboard.press("Meta+A")
        
        browser.close()

if __name__ == "__main__":
    test_keyboard()
```

## Mouse Actions

Perform mouse actions:

```python
from playwright.sync_api import sync_playwright

def test_mouse_actions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Hover over an element
        button = page.locator("button")
        button.hover()
        
        # Click and hold
        element = page.locator(".draggable")
        element.click(button="left", delay=1000)  # Hold for 1 second
        
        # Drag and drop
        source = page.locator("#source")
        target = page.locator("#target")
        source.drag_to(target)
        
        browser.close()

if __name__ == "__main__":
    test_mouse_actions()
```

## Uploading Files

Handle file uploads:

```python
from playwright.sync_api import sync_playwright

def test_file_upload():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/upload")
        
        # Upload a file
        file_input = page.locator("input[type='file']")
        file_input.set_input_files("path/to/file.pdf")
        
        # Upload multiple files
        file_input.set_input_files([
            "path/to/file1.pdf",
            "path/to/file2.pdf"
        ])
        
        browser.close()

if __name__ == "__main__":
    test_file_upload()
```

## Clearing Input Fields

Clear input fields:

```python
from playwright.sync_api import sync_playwright

def test_clear_input():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Clear an input field
        input_field = page.locator("input")
        input_field.fill("")  # Method 1: Fill with empty string
        input_field.clear()   # Method 2: Use clear method
        
        browser.close()

if __name__ == "__main__":
    test_clear_input()
```

## Focus and Blur

Control focus on elements:

```python
from playwright.sync_api import sync_playwright

def test_focus_blur():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Focus on an element
        input_field = page.locator("input")
        input_field.focus()
        
        # Blur (remove focus)
        input_field.blur()
        
        browser.close()

if __name__ == "__main__":
    test_focus_blur()
```

## Scroll Actions

Scroll elements into view:

```python
from playwright.sync_api import sync_playwright

def test_scroll():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Scroll element into view
        element = page.locator("#footer")
        element.scroll_into_view_if_needed()
        
        # Scroll page
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        browser.close()

if __name__ == "__main__":
    test_scroll()
```

## Best Practices

1. **Use `fill()` for text inputs**: It's faster and more reliable than `type()`
2. **Use role-based locators**: More stable and accessible
3. **Wait for elements**: Playwright auto-waits, but be explicit when needed
4. **Use `click()` with options**: Specify modifiers, position, etc. when needed
5. **Handle dynamic content**: Wait for elements to be ready before interacting

## Next Steps

Now that you can interact with elements, learn about:
- Waiting strategies for elements
- Assertions and expectations
- Handling dynamic content

