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

def test_basic_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Assert element is visible
        heading = page.locator("h1")
        expect(heading).to_be_visible()
        
        # Assert text content
        expect(heading).to_have_text("Example Domain")
        
        # Assert text contains
        expect(heading).to_contain_text("Example")
        
        browser.close()

if __name__ == "__main__":
    test_basic_assertions()
```

## Element Assertions

### Visibility Assertions

```python
from playwright.sync_api import sync_playwright, expect

def test_visibility():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        heading = page.locator("h1")
        
        # Exact text match
        expect(heading).to_have_text("Example Domain")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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

def test_url_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Check URL
        expect(page).to_have_url("https://example.com/")
        
        # Check URL contains
        expect(page).to_have_url(r".*example.*")
        
        # Check title
        expect(page).to_have_title("Example Domain")
        
        browser.close()

if __name__ == "__main__":
    test_url_assertions()
```

## Count Assertions

```python
from playwright.sync_api import sync_playwright, expect

def test_count_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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

# Page has URL
expect(page).to_have_url("https://example.com")

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

## Next Steps

Now that you understand assertions, learn about:
- Handling alerts and dialogs
- Working with frames
- Navigation and URLs

