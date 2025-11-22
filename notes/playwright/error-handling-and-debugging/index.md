# Error Handling and Debugging

Effective debugging is crucial for maintaining tests. This tutorial covers error handling and debugging techniques in Playwright.

## Overview

Debugging tools include:
- Playwright Inspector
- Trace Viewer
- Screenshots on failure
- Console logging
- Breakpoints

## Playwright Inspector

Run tests with inspector:

```shell{ .show-prompt lineNos=false }
PWDEBUG=1 pytest test.py
```

Or in Python:

```python
import os
os.environ["PWDEBUG"] = "1"
```

## Screenshots on Failure

Automatic screenshots:

```python
import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(page: Page, request):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"screenshots/{request.node.name}.png")
```

## Trace Viewer

Record traces:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    
    # Start tracing
    context.tracing.start(screenshots=True, snapshots=True)
    
    page = context.new_page()
    page.goto("https://example.com")
    
    # Stop tracing
    context.tracing.stop(path="trace.zip")
    
    browser.close()
```

View trace:

```shell{ .show-prompt lineNos=false }
playwright show-trace trace.zip
```

## Console Logging

```python
from playwright.sync_api import sync_playwright

def test_with_logging():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Log console messages
        page.on("console", lambda msg: print(f"Console: {msg.text}"))
        
        # Log requests
        page.on("request", lambda req: print(f"Request: {req.url}"))
        
        # Log responses
        page.on("response", lambda res: print(f"Response: {res.url} - {res.status}"))
        
        page.goto("https://example.com")
        browser.close()
```

## Error Handling

```python
from playwright.sync_api import sync_playwright, TimeoutError

def test_with_error_handling():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://example.com")
            
            # This might timeout
            page.click(".non-existent", timeout=5000)
    except TimeoutError:
        print("Element not found within timeout")
    except Exception as e:
        print(f"Error: {e}")
```

## Best Practices

1. **Use inspector**: For interactive debugging
2. **Record traces**: For failures in CI
3. **Screenshot on failure**: Automatic debugging aid
4. **Log appropriately**: Don't over-log
5. **Handle errors**: Graceful error handling

## Next Steps

Learn about:
- CI/CD integration
- Advanced scenarios
- Best practices

