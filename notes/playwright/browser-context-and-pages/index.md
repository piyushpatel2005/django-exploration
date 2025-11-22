# Browser Context and Pages

Understanding browser contexts and pages is fundamental to working with Playwright. This tutorial explains how browsers, contexts, and pages relate to each other and how to use them effectively.

## Overview

In Playwright, the hierarchy is:
- **Browser**: The browser instance (Chromium, Firefox, or WebKit)
- **Browser Context**: An isolated session (like an incognito window)
- **Page**: A single tab within a context

## Browser Instance

A browser instance represents a browser process. You launch it once and can create multiple contexts from it.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
    # Create contexts and pages here
    browser.close()
```

## Browser Context

A browser context is an isolated environment, similar to an incognito window. Each context:
- Has its own cookies and storage
- Has its own cache
- Is isolated from other contexts
- Can have multiple pages (tabs)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
    
    # Create a browser context
    context = browser.new_context()
    
    # Create pages within the context
    page1 = context.new_page()
    page2 = context.new_page()
    
    browser.close()
```

## Pages

A page represents a single tab within a browser context. You can have multiple pages in one context.

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_multiple_pages():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        context = browser.new_context()
        
        # Create multiple pages
        page1 = context.new_page()
        page2 = context.new_page()
        
        # Navigate each page independently
        page1.goto(get_file_url("page1.html"))
        page2.goto(get_file_url("page2.html"))
        
        print(f"Page 1 title: {page1.title()}")
        print(f"Page 2 title: {page2.title()}")
        
        browser.close()

if __name__ == "__main__":
    test_multiple_pages()
```

## Shortcut: Direct Page Creation

For simple cases, you can create a page directly from the browser (Playwright creates a context automatically):

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="page1.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
    page = browser.new_page()  # Context created automatically
    page.goto(get_file_url())
    browser.close()
```

## Multiple Contexts

You can create multiple isolated contexts, each with their own pages:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_multiple_contexts():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        
        # Create two separate contexts
        context1 = browser.new_context()
        context2 = browser.new_context()
        
        # Pages in different contexts are isolated
        page1 = context1.new_page()
        page2 = context2.new_page()
        
        page1.goto(get_file_url("page1.html"))
        page2.goto(get_file_url("page2.html"))
        
        # Each context has separate cookies/storage
        page1.context.cookies()  # Empty
        page2.context.cookies()  # Empty
        
        browser.close()

if __name__ == "__main__":
    test_multiple_contexts()
```

## Context Options

You can configure contexts with various options:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="page1.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_context_options():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        
        # Create context with options
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            locale='en-US',
            timezone_id='America/New_York'
        )
        
        page = context.new_page()
        page.goto(get_file_url())
        
        # Note: context.viewport_size may not be available in all Playwright versions
        # The viewport is configured when creating the context
        print(f"Viewport configured: 1920x1080")
        
        browser.close()

if __name__ == "__main__":
    test_context_options()
```

## Managing Multiple Pages

You can work with multiple pages simultaneously:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_multiple_pages_interaction():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        context = browser.new_context()
        
        page1 = context.new_page()
        page2 = context.new_page()
        
        # Navigate both pages
        page1.goto(get_file_url("page1.html"))
        page2.goto(get_file_url("page2.html"))
        
        # Interact with each page independently
        title1 = page1.title()
        title2 = page2.title()
        
        print(f"Page 1: {title1}")
        print(f"Page 2: {title2}")
        
        # Switch between pages
        page1.bring_to_front()  # Bring page1 to front
        page2.bring_to_front()  # Bring page2 to front
        
        browser.close()

if __name__ == "__main__":
    test_multiple_pages_interaction()
```

## Page Events

You can listen to page events:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="page1.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_page_events():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Listen to console messages
        def handle_console(msg):
            print(f"Console: {msg.text}")
        
        page.on("console", handle_console)
        
        # Listen to page errors
        def handle_error(error):
            print(f"Page error: {error}")
        
        page.on("pageerror", handle_error)
        
        page.goto(get_file_url())
        browser.close()

if __name__ == "__main__":
    test_page_events()
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
    <title>Page 1 - Browser Context</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #e8f4f8;
        }
        h1 {
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <h1>Page 1</h1>
    <p>This is the first page for testing browser contexts.</p>
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
    <title>Page 2 - Browser Context</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f8e8e8;
        }
        h1 {
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <h1>Page 2</h1>
    <p>This is the second page for testing browser contexts.</p>
</body>
</html>
```

## Best Practices

1. **Use contexts for isolation**: Create separate contexts for different test scenarios
2. **Close pages when done**: While contexts handle cleanup, explicitly closing pages is good practice
3. **Reuse browser instances**: Launch the browser once and create multiple contexts
4. **Use context options**: Configure viewport, locale, and other settings at the context level

## Next Steps

Now that you understand browser contexts and pages, you're ready to learn about:
- Locating elements on pages
- Interacting with web elements
- Waiting for elements to be ready

