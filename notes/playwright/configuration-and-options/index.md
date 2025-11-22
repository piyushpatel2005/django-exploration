# Configuration and Options

Playwright provides extensive configuration options. This tutorial covers configuring Playwright for different scenarios.

## Overview

Configuration options include:
- Browser settings
- Viewport and device emulation
- Timeouts
- Screenshots and videos
- Network settings

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

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,  # Set headless=False to see browser window (may have issues on macOS)
        slow_mo=1000,  # Slow down operations
        args=["--disable-blink-features=AutomationControlled"]
    )
```

## Viewport Configuration

```python
context = browser.new_context(
    viewport={"width": 1920, "height": 1080},
    device_scale_factor=1,
)
```

## Device Emulation

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
    
    # Emulate iPhone
    iphone = p.devices["iPhone 12"]
    context = browser.new_context(**iphone)
    
    page = context.new_page()
    page.goto("https://example.com")
```

## Timeout Configuration

```python
# Global timeout
page.set_default_timeout(30000)

# Navigation timeout
page.goto("https://example.com", timeout=60000)

# Action timeout
page.click("button", timeout=10000)
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

