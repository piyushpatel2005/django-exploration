# Advanced Scenarios

This tutorial covers advanced Playwright scenarios for complex testing situations.

## Overview

Advanced scenarios include:
- Testing SPAs (Single Page Applications)
- Handling authentication
- Testing file uploads
- Working with WebSockets
- Testing geolocation

## Testing SPAs

```python
from playwright.sync_api import sync_playwright, expect

def test_spa():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://spa-example.com")
        
        # Wait for SPA to load
        page.wait_for_load_state("networkidle")
        
        # Wait for specific content
        page.wait_for_selector(".app-loaded")
        
        # Test SPA navigation
        page.click("a[href='/about']")
        expect(page).to_have_url("**/about")
        
        browser.close()
```

## Handling Authentication

```python
from playwright.sync_api import sync_playwright
import json

def test_with_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Login
        page.goto("https://example.com/login")
        page.fill("input[name='username']", "user")
        page.fill("input[name='password']", "pass")
        page.click("button[type='submit']")
        
        # Save auth state
        context.storage_state(path="auth.json")
        
        # Use saved auth state
        browser2 = p.chromium.launch(headless=False)
        context2 = browser2.new_context(storage_state="auth.json")
        page2 = context2.new_page()
        page2.goto("https://example.com/dashboard")
        
        browser2.close()
```

## Testing File Uploads

```python
from playwright.sync_api import sync_playwright

def test_file_upload():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/upload")
        
        with page.expect_file_chooser() as fc_info:
            page.click("button#upload")
        
        file_chooser = fc_info.value
        file_chooser.set_files("path/to/file.pdf")
        
        # Verify upload
        expect(page.locator(".success")).to_be_visible()
        
        browser.close()
```

## Testing Geolocation

```python
from playwright.sync_api import sync_playwright

def test_geolocation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            geolocation={"latitude": 40.7128, "longitude": -74.0060},
            permissions=["geolocation"]
        )
        page = context.new_page()
        page.goto("https://example.com")
        
        # Test geolocation feature
        page.click("button#get-location")
        expect(page.locator(".location")).to_contain_text("New York")
        
        browser.close()
```

## WebSocket Testing

```python
from playwright.sync_api import sync_playwright

def test_websocket():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        messages = []
        
        def handle_websocket(ws):
            ws.on("framereceived", lambda event: messages.append(event.payload))
        
        page.on("websocket", handle_websocket)
        page.goto("https://example.com/websocket")
        
        # Wait for messages
        page.wait_for_timeout(2000)
        
        print(f"Received {len(messages)} messages")
        
        browser.close()
```

## Best Practices

1. **Wait appropriately**: SPAs need special waiting
2. **Save auth state**: Reuse authentication
3. **Handle async operations**: WebSockets, etc.
4. **Test edge cases**: Geolocation, permissions
5. **Isolate tests**: Each test independent

## Next Steps

Learn about:
- Best practices
- Optimizing test performance
- Maintaining test suites

