# Navigation and URLs

Navigating between pages and managing URLs is a fundamental part of web testing. This tutorial covers navigation methods and URL handling in Playwright.

## Overview

Playwright provides several methods for navigation:
- `goto()`: Navigate to a URL
- `go_back()`: Go back in browser history
- `go_forward()`: Go forward in browser history
- `reload()`: Reload the current page
- URL assertions and checks

## Basic Navigation

### Navigate to URL

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_navigate():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Navigate to a URL
        file_url = get_file_url("page1.html")
        page.goto(file_url)
        
        print(f"✓ Current URL: {page.url[:50]}...")
        print(f"✓ Page title: {page.title()}")
        
        browser.close()

if __name__ == "__main__":
    test_navigate()
```

### Navigation Options

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_navigation_options():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Navigate with options
        page.goto(
            get_file_url("page1.html"),
            wait_until="load",  # Wait for load event
            timeout=30000  # 30 second timeout
        )
        
        browser.close()

if __name__ == "__main__":
    test_navigation_options()
```

## Wait Until Options

Control when navigation is considered complete:

```python
from playwright.sync_api import sync_playwright

def test_wait_until():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Wait for DOM content loaded
        page.goto("https://example.com", wait_until="domcontentloaded")
        
        # Wait for network to be idle
        page.goto("https://example.com", wait_until="networkidle")
        
        # Wait for load event
        page.goto("https://example.com", wait_until="load")
        
        # Wait for commit (navigation started)
        page.goto("https://example.com", wait_until="commit")
        
        browser.close()

if __name__ == "__main__":
    test_wait_until()
```

## Browser History

Navigate through browser history:

```python
from playwright.sync_api import sync_playwright

def test_history():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Navigate to first page
        page.goto(get_file_url("page1.html"))
        print(f"Page 1: {page.url}")
        
        # Navigate to second page
        page.goto("https://playwright.dev")
        print(f"Page 2: {page.url}")
        
        # Go back
        page.go_back()
        print(f"After back: {page.url}")
        
        # Go forward
        page.go_forward()
        print(f"After forward: {page.url}")
        
        browser.close()

if __name__ == "__main__":
    test_history()
```

## Reload Page

Reload the current page:

```python
from playwright.sync_api import sync_playwright

def test_reload():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url("page1.html"))
        
        # Reload page
        page.reload()
        
        # Reload and wait for network idle
        page.reload(wait_until="networkidle")
        
        browser.close()

if __name__ == "__main__":
    test_reload()
```

## URL Assertions

Verify URLs:

```python
from playwright.sync_api import sync_playwright, expect

def test_url_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url("page1.html"))
        
        # Assert exact URL
        expect(page).to_have_url(r".*page1\.html.*")
        
        # Assert URL contains
        expect(page).to_have_url(r".*example.*")
        
        # Assert URL with regex
        expect(page).to_have_url(r"https://.*\.com/")
        
        browser.close()

if __name__ == "__main__":
    test_url_assertions()
```

## Waiting for Navigation

Wait for navigation to complete:

```python
from playwright.sync_api import sync_playwright

def test_wait_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url("page1.html"))
        
        # Wait for navigation after click
        with page.expect_navigation():
            page.locator("a").click()
        
        print(f"Navigated to: {page.url}")
        
        browser.close()

if __name__ == "__main__":
    test_wait_navigation()
```

## URL Parameters

Work with URL parameters:

```python
from playwright.sync_api import sync_playwright

def test_url_params():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Navigate with query parameters
        page.goto("https://example.com?param1=value1&param2=value2")
        
        # Get current URL
        current_url = page.url
        print(f"Current URL: {current_url}")
        
        # Evaluate URL in browser
        url_params = page.evaluate("() => new URL(window.location.href).searchParams.get('param1')")
        print(f"Param1: {url_params}")
        
        browser.close()

if __name__ == "__main__":
    test_url_params()
```

## Redirect Handling

Handle redirects:

```python
from playwright.sync_api import sync_playwright

def test_redirects():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Follow redirects automatically (default)
        response = page.goto("https://example.com", wait_until="networkidle")
        
        # Check if redirect occurred
        if response:
            print(f"Final URL: {response.url}")
            print(f"Status: {response.status}")
        
        browser.close()

if __name__ == "__main__":
    test_redirects()
```

## Best Practices

1. **Use appropriate wait_until**: Choose based on what you need
2. **Set timeouts**: Prevent tests from hanging
3. **Wait for navigation**: Use `expect_navigation()` when clicking links
4. **Verify URLs**: Assert URLs after navigation
5. **Handle redirects**: Be aware of redirect behavior

## Common Patterns

```python
# Pattern 1: Navigate and wait
page.goto(get_file_url("page1.html"), wait_until="networkidle")

# Pattern 2: Wait for navigation
with page.expect_navigation():
    page.click("a")

# Pattern 3: Assert URL
expect(page).to_have_url(r".*page1\.html.*")

# Pattern 4: Go back/forward
page.go_back()
page.go_forward()
```

## HTML Pages for Testing

Here are the HTML pages used in the examples above:

**page1.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navigation Page 1</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #e8f4f8;
        }
        a {
            color: #3498db;
            text-decoration: none;
            font-size: 18px;
            margin-right: 20px;
        }
    </style>
</head>
<body>
    <h1>Navigation Page 1</h1>
    <p>This is the first page for testing navigation.</p>
    <a href="page2.html">Go to Page 2</a>
</body>
</html>
```

**page2.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navigation Page 2</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f8e8e8;
        }
        a {
            color: #3498db;
            text-decoration: none;
            font-size: 18px;
            margin-right: 20px;
        }
    </style>
</head>
<body>
    <h1>Navigation Page 2</h1>
    <p>This is the second page for testing navigation.</p>
    <a href="page1.html">Go to Page 1</a>
</body>
</html>
```

## Next Steps

Now that you understand navigation, learn about:
- Cookies and storage management
- Screenshots and videos
- Network interception

