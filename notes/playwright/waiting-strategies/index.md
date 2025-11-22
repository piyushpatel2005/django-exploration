# Waiting Strategies

One of Playwright's key features is automatic waiting. This tutorial explains how Playwright handles waits and how to use explicit wait strategies when needed.

## Overview

Playwright automatically waits for elements to be ready before interacting with them. This eliminates most flaky tests. However, sometimes you need explicit waits for specific conditions.

## Auto-Waiting

Playwright automatically waits for elements to be:
- **Attached** to the DOM
- **Visible** (not hidden)
- **Stable** (not animating)
- **Enabled** (not disabled)
- **Editable** (for input fields)

```python
from playwright.sync_api import sync_playwright

def test_auto_wait():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Playwright automatically waits for the element to be ready
        heading = page.locator("h1")
        heading.click()  # Waits automatically if element isn't ready
        
        browser.close()

if __name__ == "__main__":
    test_auto_wait()
```

## Explicit Waits

### `wait_for_selector()`

Wait for a specific selector to appear:

```python
from playwright.sync_api import sync_playwright

def test_wait_for_selector():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Wait for element to appear
        page.wait_for_selector("h1", state="visible")
        
        # Wait for element to be hidden
        page.wait_for_selector(".loading", state="hidden")
        
        browser.close()

if __name__ == "__main__":
    test_wait_for_selector()
```

### `wait_for_load_state()`

Wait for the page to reach a specific load state:

```python
from playwright.sync_api import sync_playwright

def test_wait_for_load_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate and wait for load
        page.goto("https://example.com", wait_until="load")
        
        # Wait for DOM content loaded
        page.wait_for_load_state("domcontentloaded")
        
        # Wait for network to be idle
        page.wait_for_load_state("networkidle")
        
        # Wait for all load states
        page.wait_for_load_state("load")
        
        browser.close()

if __name__ == "__main__":
    test_wait_for_load_state()
```

### `wait_for_timeout()`

Wait for a specific duration (use sparingly):

```python
from playwright.sync_api import sync_playwright

def test_wait_for_timeout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Wait for 2 seconds
        page.wait_for_timeout(2000)
        
        browser.close()

if __name__ == "__main__":
    test_wait_for_timeout()
```

**Note**: Avoid `wait_for_timeout()` when possible. Use condition-based waits instead.

## Waiting for Network Requests

Wait for network requests to complete:

```python
from playwright.sync_api import sync_playwright

def test_wait_for_network():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Wait for navigation
        with page.expect_response("**/api/data") as response_info:
            page.goto("https://example.com")
        response = response_info.value
        print(f"Response status: {response.status}")
        
        browser.close()

if __name__ == "__main__":
    test_wait_for_network()
```

## Waiting for Navigation

Wait for page navigation:

```python
from playwright.sync_api import sync_playwright

def test_wait_for_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Wait for navigation after click
        with page.expect_navigation():
            page.locator("a").click()
        
        browser.close()

if __name__ == "__main__":
    test_wait_for_navigation()
```

## Waiting for Element States

Wait for specific element states:

```python
from playwright.sync_api import sync_playwright

def test_wait_for_element_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        element = page.locator("button")
        
        # Wait for element to be visible
        element.wait_for(state="visible")
        
        # Wait for element to be hidden
        element.wait_for(state="hidden")
        
        # Wait for element to be attached
        element.wait_for(state="attached")
        
        # Wait for element to be detached
        element.wait_for(state="detached")
        
        browser.close()

if __name__ == "__main__":
    test_wait_for_element_state()
```

## Custom Wait Conditions

Create custom wait conditions:

```python
from playwright.sync_api import sync_playwright
import time

def test_custom_wait():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Custom wait function
        def wait_for_custom_condition():
            for _ in range(10):  # Try 10 times
                if page.locator(".custom-element").count() > 0:
                    return True
                time.sleep(0.5)
            return False
        
        wait_for_custom_condition()
        
        browser.close()

if __name__ == "__main__":
    test_custom_wait()
```

## Timeout Configuration

Set timeouts globally or per action:

```python
from playwright.sync_api import sync_playwright

def test_timeout_config():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # Create context with timeout
        context = browser.new_context()
        context.set_default_timeout(30000)  # 30 seconds
        
        page = context.new_page()
        
        # Set timeout for specific action
        page.goto("https://example.com", timeout=60000)
        
        # Set timeout for locator
        element = page.locator("h1")
        element.click(timeout=10000)
        
        browser.close()

if __name__ == "__main__":
    test_timeout_config()
```

## Best Practices

1. **Rely on auto-waiting**: Playwright's auto-wait is usually sufficient
2. **Avoid `wait_for_timeout()`**: Use condition-based waits instead
3. **Use `wait_for_load_state()`**: For page-level waits
4. **Wait for specific conditions**: Instead of fixed timeouts
5. **Set appropriate timeouts**: Balance between speed and reliability

## Common Wait Patterns

```python
# Wait for element to be visible
page.wait_for_selector(".element", state="visible")

# Wait for element to disappear
page.wait_for_selector(".loading", state="hidden")

# Wait for network to be idle
page.wait_for_load_state("networkidle")

# Wait for navigation
with page.expect_navigation():
    page.click("a")

# Wait for response
with page.expect_response("**/api/data"):
    page.click("button")
```

## Next Steps

Now that you understand waiting strategies, learn about:
- Assertions and expectations
- Verifying element states and content
- Error handling

