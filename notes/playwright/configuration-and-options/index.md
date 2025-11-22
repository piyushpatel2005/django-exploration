# Configuration and Options

Playwright provides extensive configuration options. This tutorial covers configuring Playwright for different scenarios.

## Overview

Configuration options include:
- Browser settings
- Viewport and device emulation
- Timeouts
- Screenshots and videos
- Network settings

## Test Page

The examples in this tutorial use the following HTML page:

**index.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configuration and Options</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
    </style>
</head>
<body>
    <h1>Configuration and Options Test Page</h1>
    <p>This page is used for testing Playwright configuration options.</p>
</body>
</html>
```

## Playwright Configuration File

Create `playwright.config.js`:

```javascript
module.exports = {
  use: {
    headless: false,
    viewport: { width: 1280, height: 720 },
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  timeout: 30000,
};
```

## Python Configuration

In `conftest.py`:

```python
import pytest
from playwright.sync_api import BrowserContext

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }
```

## Browser Options

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_browser_options():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # Set headless=False to see browser window
            slow_mo=500  # Slow down by 500ms
        )
        page = browser.new_page()
        page.goto(get_file_url())
        print("✓ Browser configured with options")
        browser.close()

if __name__ == "__main__":
    test_browser_options()
```

## Viewport Configuration

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_viewport_config():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        page.goto(get_file_url())
        
        # Get viewport size from the page
        viewport_size = page.viewport_size
        print(f"✓ Viewport: {viewport_size['width']}x{viewport_size['height']}")
        
        browser.close()

if __name__ == "__main__":
    test_viewport_config()
```

## Device Emulation

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_device_emulation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        
        # Emulate iPhone
        iphone = p.devices["iPhone 12"]
        context = browser.new_context(**iphone)
        
        page = context.new_page()
        page.goto(get_file_url())
        
        # Get viewport size from the page
        viewport_size = page.viewport_size
        print(f"✓ Device viewport: {viewport_size['width']}x{viewport_size['height']}")
        
        browser.close()

if __name__ == "__main__":
    test_device_emulation()
```

## Timeout Configuration

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_timeout_config():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Set default timeout
        page.set_default_timeout(10000)
        
        page.goto(get_file_url())
        print("✓ Timeout configured")
        
        browser.close()

if __name__ == "__main__":
    test_timeout_config()
```

## Best Practices

1. **Set appropriate timeouts**: Balance speed and reliability
2. **Use device emulation**: Test responsive designs
3. **Configure screenshots**: For debugging failures
4. **Set viewport**: Consistent rendering
5. **Use configuration files**: Centralize settings

## Next Steps

Learn about:
- Error handling
- CI/CD integration
- Advanced scenarios

