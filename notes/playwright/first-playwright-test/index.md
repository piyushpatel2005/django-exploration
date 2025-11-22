# First Playwright Test

Now that Playwright is installed, let's write your first test! This tutorial will introduce you to the basic structure of a Playwright test and how to run it.

## Overview

A Playwright test typically follows this structure:
1. Launch a browser
2. Create a browser context and page
3. Navigate to a URL
4. Interact with elements or verify content
5. Close the browser

## Basic Test Structure

Let's start with a simple test that navigates to a local HTML file and checks the page title:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_example():
    with sync_playwright() as p:
        # Launch browser in headless mode (more stable)
        # Change headless=False if you want to see the browser window
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(get_file_url())
        assert page.title() == "First Playwright Test"
        browser.close()

if __name__ == "__main__":
    test_example()
```

Let's break down what's happening:

1. **`sync_playwright()`**: Creates a Playwright instance. The `with` statement ensures proper cleanup
2. **`browser.launch()`**: Launches a browser instance. `headless=True` runs without a visible window (more stable). Change to `headless=False` to see the browser window
3. **`browser.new_page()`**: Creates a new page (tab) in the browser
4. **`page.goto()`**: Navigates to the specified URL
5. **`page.title()`**: Gets the title of the current page
6. **`assert`**: Verifies that the title matches our expectation
7. **`browser.close()`**: Closes the browser

## Running the Test

Save the code to a file (e.g., `test_example.py`) and run it:

```shell{ .show-prompt lineNos=false }
python test_example.py
```

**Output:**
```output{ lineNos=false }
✓ Page title verified: First Playwright Test
```

**Note:** The browser runs in headless mode by default, so you won't see a browser window. Change `headless=True` to `headless=False` if you want to see the browser window.

## Using Different Browsers

Playwright supports multiple browsers. You can easily switch between them:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_chromium():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        print(f"Chromium: {page.title()}")
        browser.close()

def test_firefox():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        print(f"Firefox: {page.title()}")
        browser.close()

def test_webkit():
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        print(f"WebKit: {page.title()}")
        browser.close()

if __name__ == "__main__":
    test_chromium()
    test_firefox()
    test_webkit()
```

## Headless vs Headed Mode

- **Headless mode** (`headless=True`): Browser runs without a visible window (faster, more stable, good for CI/CD) - **Recommended default**
- **Headed mode** (`headless=False`): Browser window is visible (useful for debugging, but may have issues on some systems like macOS)

```python
# Headless mode (default - recommended for stability)
browser = p.chromium.launch(headless=True)

# Headed mode (for debugging - change if you want to see the browser)
browser = p.chromium.launch(headless=False)
```

**Note:** On macOS, `headless=False` may cause `TargetClosedError` due to system security settings. Use `headless=True` by default and only switch to `headless=False` when you need to debug visually.

## Basic Assertions

Playwright provides several ways to verify content:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_basic_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Check page title
        assert page.title() == "First Playwright Test"
        
        # Check URL (file URLs will be different)
        assert "index.html" in page.url
        
        # Check page content
        content = page.content()
        assert "First Playwright Test" in content
        
        browser.close()

if __name__ == "__main__":
    test_basic_assertions()
```

## A More Complete Example

Let's create a test that interacts with a local HTML page:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_page_content():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Navigate to local HTML file
        page.goto(get_file_url())
        
        # Verify page loaded
        assert "First Playwright Test" in page.title()
        
        # Check for specific text on the page
        heading = page.locator("h1").first
        assert heading.is_visible()
        
        print("Test passed!")
        browser.close()

if __name__ == "__main__":
    test_page_content()
```

## HTML Page for Testing

Here's the HTML page (`index.html`) used in the examples above:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>First Playwright Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        h1 {
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <h1>First Playwright Test</h1>
    <p>This page is used for your first Playwright test.</p>
</body>
</html>
```

## Common Patterns

### Pattern 1: Simple Test Function

```python
def test_something():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # ... your test code ...
        browser.close()
```

### Pattern 2: Using Context Manager

The `with` statement automatically handles cleanup, but you still need to close the browser explicitly.

## Next Steps

Now that you've written your first test, you're ready to learn about:
- Browser contexts and pages
- Locating elements on the page
- Interacting with elements

In the next tutorial, we'll dive deeper into browser contexts and how to manage multiple pages.

