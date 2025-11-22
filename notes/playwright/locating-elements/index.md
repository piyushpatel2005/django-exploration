# Locating Elements

One of the most important skills in Playwright is locating elements on a web page. This tutorial covers various strategies for finding elements, from simple selectors to advanced locator strategies.

## Overview

Playwright provides multiple ways to locate elements:
- CSS selectors
- XPath selectors
- Text-based locators
- Role-based locators
- Test ID locators

## The `locator()` Method

The primary way to locate elements is using the `locator()` method:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")
    
    # Locate an element
    heading = page.locator("h1")
    
    browser.close()
```

## CSS Selectors

CSS selectors are the most common way to locate elements:

```python
from playwright.sync_api import sync_playwright

def test_css_selectors():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # By tag name
        heading = page.locator("h1")
        
        # By ID
        element = page.locator("#my-id")
        
        # By class
        element = page.locator(".my-class")
        
        # By attribute
        element = page.locator("[data-testid='submit']")
        
        # Combined selectors
        element = page.locator("div.container > button.primary")
        
        print(f"Heading text: {heading.text_content()}")
        browser.close()

if __name__ == "__main__":
    test_css_selectors()
```

## XPath Selectors

XPath provides powerful element location capabilities:

```python
from playwright.sync_api import sync_playwright

def test_xpath_selectors():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Absolute XPath
        element = page.locator("xpath=/html/body/h1")
        
        # Relative XPath
        element = page.locator("xpath=//h1")
        
        # XPath with text
        element = page.locator("xpath=//button[text()='Submit']")
        
        # XPath with contains
        element = page.locator("xpath=//a[contains(@href, 'example')]")
        
        browser.close()

if __name__ == "__main__":
    test_xpath_selectors()
```

## Text-Based Locators

Locate elements by their visible text:

```python
from playwright.sync_api import sync_playwright

def test_text_locators():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Locate by exact text
        heading = page.get_by_text("Example Domain")
        
        # Locate by partial text
        link = page.get_by_text("More information", exact=False)
        
        # Locate by label text
        input_field = page.get_by_label("Email")
        
        # Locate by placeholder
        search_box = page.get_by_placeholder("Search...")
        
        print(f"Heading: {heading.text_content()}")
        browser.close()

if __name__ == "__main__":
    test_text_locators()
```

## Role-Based Locators

Use semantic roles to locate elements (recommended for accessibility):

```python
from playwright.sync_api import sync_playwright

def test_role_locators():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Locate by role
        button = page.get_by_role("button", name="Submit")
        link = page.get_by_role("link", name="Click here")
        heading = page.get_by_role("heading", name="Welcome")
        
        # Common roles: button, link, textbox, checkbox, radio, etc.
        
        browser.close()

if __name__ == "__main__":
    test_role_locators()
```

## Test ID Locators

Using test IDs is a best practice for stable selectors:

```python
from playwright.sync_api import sync_playwright

def test_testid_locators():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Locate by test ID
        element = page.get_by_test_id("submit-button")
        
        # Equivalent to: page.locator("[data-testid='submit-button']")
        
        browser.close()

if __name__ == "__main__":
    test_testid_locators()
```

## Chaining Locators

You can chain locators to find nested elements:

```python
from playwright.sync_api import sync_playwright

def test_chaining_locators():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Chain locators
        container = page.locator(".container")
        button = container.locator("button")
        text = button.locator("span")
        
        # Or use filter
        buttons = page.locator("button").filter(has_text="Submit")
        
        browser.close()

if __name__ == "__main__":
    test_chaining_locators()
```

## Filtering Locators

Filter locators based on conditions:

```python
from playwright.sync_api import sync_playwright

def test_filtering_locators():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Filter by text
        submit_button = page.locator("button").filter(has_text="Submit")
        
        # Filter by another locator
        form = page.locator("form")
        submit_in_form = form.locator("button").filter(has=page.locator("input[type='email']"))
        
        # Get first/last/nth element
        first_button = page.locator("button").first
        last_button = page.locator("button").last
        third_button = page.locator("button").nth(2)  # 0-indexed
        
        browser.close()

if __name__ == "__main__":
    test_filtering_locators()
```

## Multiple Elements

When a locator matches multiple elements, you can work with all of them:

```python
from playwright.sync_api import sync_playwright

def test_multiple_elements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Get count of matching elements
        links = page.locator("a")
        count = links.count()
        print(f"Found {count} links")
        
        # Iterate through all elements
        for i in range(count):
            link = links.nth(i)
            print(f"Link {i}: {link.text_content()}")
        
        # Get all text contents
        all_texts = links.all_text_contents()
        print(f"All link texts: {all_texts}")
        
        browser.close()

if __name__ == "__main__":
    test_multiple_elements()
```

## Best Practices

1. **Prefer role-based locators**: They're more accessible and stable
2. **Use test IDs**: Add `data-testid` attributes for critical elements
3. **Avoid brittle selectors**: Don't rely on CSS classes that might change
4. **Use text locators carefully**: Text can change, use for user-facing content
5. **Chain locators**: Start broad, then narrow down
6. **Avoid XPath when possible**: CSS selectors are usually faster and more readable

## Locator Best Practices Summary

| Method | When to Use | Example |
|--------|-------------|---------|
| `get_by_role()` | Semantic elements | `page.get_by_role("button")` |
| `get_by_test_id()` | Test-specific elements | `page.get_by_test_id("submit")` |
| `get_by_text()` | User-visible text | `page.get_by_text("Click here")` |
| `get_by_label()` | Form inputs | `page.get_by_label("Email")` |
| `locator()` | CSS/XPath selectors | `page.locator(".class")` |

## Next Steps

Now that you can locate elements, you're ready to learn about:
- Clicking and interacting with elements
- Filling forms
- Handling different input types

