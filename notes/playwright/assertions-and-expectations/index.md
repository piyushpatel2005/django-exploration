# Assertions and Expectations

Assertions are crucial for verifying that your tests are working correctly. Playwright provides a powerful `expect()` API for making assertions about page state, elements, and values.

## Overview

Playwright's `expect()` API provides:
- Rich assertion messages
- Auto-waiting for conditions
- Multiple assertion types
- Custom error messages

## Basic Assertions

### Using `expect()` with Locators

```python
from playwright.sync_api import sync_playwright, expect
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_basic_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Assert element is visible
        heading = page.locator("h1")
        expect(heading).to_be_visible()
        print("✓ Element is visible")
        
        # Assert text content
        expect(heading).to_have_text("Assertions and Expectations Test Page")
        print("✓ Text matches")
        
        browser.close()

if __name__ == "__main__":
    test_basic_assertions()
```

## Element Assertions

### Visibility Assertions

```python
from playwright.sync_api import sync_playwright, expect
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_visibility():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        element = page.locator("h1")
        
        # Element is visible
        expect(element).to_be_visible()
        
        # Element is hidden
        expect(element).not_to_be_visible()  # This would fail in this case
        
        # Element is attached to DOM
        expect(element).to_be_attached()
        
        browser.close()

if __name__ == "__main__":
    test_visibility()
```

### Text Assertions

```python
from playwright.sync_api import sync_playwright, expect

def test_text_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        heading = page.locator("h1")
        
        # Exact text match
        expect(heading).to_have_text("Assertions and Expectations Test Page")
        
        # Contains text
        expect(heading).to_contain_text("Example")
        
        # Regex match
        expect(heading).to_have_text(r"Example.*")
        
        browser.close()

if __name__ == "__main__":
    test_text_assertions()
```

### Attribute Assertions

```python
from playwright.sync_api import sync_playwright, expect

def test_attribute_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        link = page.locator("a").first
        
        # Check attribute value
        expect(link).to_have_attribute("href", "https://www.iana.org/domains/example")
        
        # Check attribute exists
        expect(link).to_have_attribute("href")
        
        browser.close()

if __name__ == "__main__":
    test_attribute_assertions()
```

### State Assertions

```python
from playwright.sync_api import sync_playwright, expect

def test_state_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        checkbox = page.locator("input[type='checkbox']")
        
        # Check if checked
        expect(checkbox).to_be_checked()
        
        # Check if enabled
        expect(checkbox).to_be_enabled()
        
        # Check if editable
        input_field = page.locator("input[type='text']")
        expect(input_field).to_be_editable()
        
        browser.close()

if __name__ == "__main__":
    test_state_assertions()
```

## Page Assertions

### URL Assertions

```python
from playwright.sync_api import sync_playwright, expect
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_url_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        file_url = get_file_url()
        page.goto(file_url)
        
        # Check URL contains file path
        expect(page).to_have_url(r".*index\.html.*")
        
        # Check title
        expect(page).to_have_title("Assertions and Expectations")
        
        browser.close()

if __name__ == "__main__":
    test_url_assertions()
```

## Count Assertions

```python
from playwright.sync_api import sync_playwright, expect

def test_count_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        links = page.locator("a")
        
        # Check count
        expect(links).to_have_count(2)
        
        # Check count is greater than
        expect(links).to_have_count(lambda count: count > 0)
        
        browser.close()

if __name__ == "__main__":
    test_count_assertions()
```

## Value Assertions

```python
from playwright.sync_api import sync_playwright, expect

def test_value_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # For input fields
        input_field = page.locator("input")
        input_field.fill("test")
        expect(input_field).to_have_value("test")
        
        browser.close()

if __name__ == "__main__":
    test_value_assertions()
```

## Custom Error Messages

Add custom error messages to assertions:

```python
from playwright.sync_api import sync_playwright, expect

def test_custom_messages():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        heading = page.locator("h1")
        expect(heading).to_have_text(
            "Wrong Text",
            message="Heading should display 'Example Domain'"
        )
        
        browser.close()

if __name__ == "__main__":
    test_custom_messages()
```

## Soft Assertions

Soft assertions don't stop test execution on failure:

```python
from playwright.sync_api import sync_playwright, expect

def test_soft_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Use soft assertions
        expect.soft(page.locator("h1")).to_have_text("Wrong")
        expect.soft(page.locator("p")).to_have_text("Wrong")
        
        # Test continues even if assertions fail
        print("Test completed")
        
        browser.close()

if __name__ == "__main__":
    test_soft_assertions()
```

## Negating Assertions

Use `.not` to negate assertions:

```python
from playwright.sync_api import sync_playwright, expect

def test_negated_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        hidden_element = page.locator(".hidden")
        
        # Element should not be visible
        expect(hidden_element).not_to_be_visible()
        
        # Element should not have text
        expect(hidden_element).not_to_have_text("Visible")
        
        browser.close()

if __name__ == "__main__":
    test_negated_assertions()
```

## Common Assertion Patterns

```python
# Element is visible
expect(element).to_be_visible()

# Element has text
expect(element).to_have_text("Expected Text")

# Element contains text
expect(element).to_contain_text("Partial")

# Element has attribute
expect(element).to_have_attribute("href", "value")

# Element is checked
expect(checkbox).to_be_checked()

# Page has URL (for file URLs, check for file path)
expect(page).to_have_url(r".*index\.html.*")

# Page has title
expect(page).to_have_title("Page Title")

# Multiple elements
expect(locator).to_have_count(5)
```

## Best Practices

1. **Use `expect()` API**: More reliable than manual assertions
2. **Let Playwright auto-wait**: Assertions automatically wait for conditions
3. **Use descriptive assertions**: Clear what you're checking
4. **Combine assertions**: Check multiple conditions when needed
5. **Use soft assertions**: When you want to check multiple things without stopping

## HTML Page for Testing

Here's the HTML page (`index.html`) used in the examples above:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assertions and Expectations</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        .box {
            padding: 20px;
            margin: 10px 0;
            border: 2px solid #3498db;
        }
        .hidden {
            display: none;
        }
        input {
            padding: 8px;
            margin: 10px 0;
            width: 200px;
        }
        button {
            padding: 10px 20px;
            background-color: #27ae60;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Assertions and Expectations Test Page</h1>
    
    <div class="box" id="visible-box">
        <h2>Visible Element</h2>
        <p>This element is visible.</p>
    </div>
    
    <div class="box hidden" id="hidden-box">
        <h2>Hidden Element</h2>
        <p>This element is hidden.</p>
    </div>
    
    <div>
        <input type="text" id="test-input" value="Test Value">
    </div>
    
    <div>
        <button id="test-btn">Test Button</button>
    </div>
    
    <div>
        <a href="#section1" id="test-link">Test Link</a>
    </div>
    
    <div id="section1">
        <h2>Section 1</h2>
        <p>Content for assertions.</p>
    </div>
</body>
</html>
```

## Next Steps

Now that you understand assertions, learn about:
- Handling alerts and dialogs
- Working with frames
- Navigation and URLs

