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
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_auto_wait():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Playwright automatically waits for the element to be ready
            heading = page.locator("h1")
            print(f"✓ Auto-waited for element: {heading.text_content()}")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_auto_wait()
```

## Explicit Waits

### `wait_for_selector()`

Wait for a specific selector to appear:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_wait_for_selector():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Wait for element to appear
            page.wait_for_selector("h1", state="visible")
            print("✓ Element is visible")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_wait_for_selector()
```

### `wait_for_load_state()`

Wait for the page to reach a specific load state:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_wait_for_load_state():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            
            # Navigate and wait for load
            page.goto(get_file_url(), wait_until="load")
            print("✓ Page loaded")
            
            # Wait for network to be idle
            page.wait_for_load_state("networkidle")
            print("✓ Network idle")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_wait_for_load_state()
```

### `wait_for_timeout()`

Wait for a specific duration (use sparingly):

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_wait_for_timeout():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Wait for 1 second
            page.wait_for_timeout(1000)
            print("✓ Waited for timeout")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_wait_for_timeout()
```

**Note**: Avoid `wait_for_timeout()` when possible. Use condition-based waits instead.

## Waiting for Network Requests

Wait for network requests to complete:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_wait_for_network():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            
            # Navigate to page
            page.goto(get_file_url())
            
            # Note: For local file URLs, network requests are minimal
            # This example shows the pattern for web URLs
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_wait_for_network()
```

## Waiting for Navigation

Wait for page navigation:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_wait_for_navigation():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Wait for navigation after click (if link navigates)
            # Note: For local file URLs, navigation may not occur
            # This example shows the pattern for web URLs
            page.locator("h1").click()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_wait_for_navigation()
```

## Waiting for Dynamic Content

Wait for content that loads dynamically:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_wait_for_dynamic_content():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Click button to load dynamic content
            page.click("#load-btn")
            
            # Wait for dynamic content to appear
            page.wait_for_selector("#dynamic-content", state="visible")
            print("✓ Dynamic content loaded")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_wait_for_dynamic_content()
```

## Waiting for Element States

Wait for specific element states:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_wait_for_element_state():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            element = page.locator("h1")
            
            # Wait for element to be visible
            element.wait_for(state="visible")
            print("✓ Element is visible")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_wait_for_element_state()
```

## Custom Wait Conditions

Create custom wait conditions:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys
import time

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_custom_wait():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Custom wait function
            def wait_for_custom_condition():
                for _ in range(10):  # Try 10 times
                    if page.locator("h1").count() > 0:
                        return True
                    time.sleep(0.5)
                return False
            
            wait_for_custom_condition()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_custom_wait()
```

## Timeout Configuration

Set timeouts globally or per action:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_timeout_config():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            # Create context with timeout
            context = browser.new_context()
            context.set_default_timeout(30000)  # 30 seconds
            
            page = context.new_page()
            
            # Set timeout for specific action
            page.goto(get_file_url(), timeout=60000)
            
            # Set timeout for locator
            element = page.locator("h1")
            element.click(timeout=10000)
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_timeout_config()
```

## HTML Page for Testing

Here's the HTML page (`index.html`) used in the examples above:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Waiting Strategies</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        .loading {
            display: none;
            color: #3498db;
        }
        .content {
            margin-top: 20px;
        }
        button {
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            cursor: pointer;
        }
        #dynamic-content {
            margin-top: 20px;
            padding: 20px;
            background-color: #f0f0f0;
            display: none;
        }
    </style>
</head>
<body>
    <h1>Waiting Strategies Test Page</h1>
    
    <button id="load-btn">Load Content</button>
    <div class="loading" id="loading">Loading...</div>
    
    <div id="dynamic-content">
        <h2>Dynamic Content Loaded</h2>
        <p>This content appears after a delay.</p>
    </div>
    
    <div class="content">
        <h2>Static Content</h2>
        <p>This content is always visible.</p>
    </div>
    
    <script>
        document.getElementById('load-btn').addEventListener('click', function() {
            const loading = document.getElementById('loading');
            const content = document.getElementById('dynamic-content');
            
            loading.style.display = 'block';
            
            setTimeout(function() {
                loading.style.display = 'none';
                content.style.display = 'block';
            }, 2000);
        });
    </script>
</body>
</html>
```

## Best Practices

1. **Rely on auto-waiting**: Playwright's auto-wait is usually sufficient
2. **Avoid `wait_for_timeout()`**: Use condition-based waits instead
3. **Use `wait_for_load_state()`**: For page-level waits
4. **Wait for specific conditions**: Instead of fixed timeouts
5. **Set appropriate timeouts**: Balance between speed and reliability
6. **Platform-specific handling**: On macOS, use Firefox to avoid Chromium crashes
7. **Use try/finally**: Always ensure browser cleanup with try/finally blocks

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

