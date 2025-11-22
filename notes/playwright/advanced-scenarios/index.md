# Advanced Scenarios

This tutorial covers advanced Playwright scenarios for complex testing situations.

## Overview

Advanced scenarios include:
- Testing SPAs (Single Page Applications)
- Handling authentication
- Testing file uploads
- Working with WebSockets
- Testing geolocation

## Test Page

The examples in this tutorial use the following HTML page:

**index.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Scenarios</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        button {
            padding: 10px 20px;
            margin: 10px 5px;
            background-color: #3498db;
            color: white;
            border: none;
            cursor: pointer;
        }
        #content {
            margin-top: 20px;
            padding: 20px;
            background-color: #f0f0f0;
        }
    </style>
</head>
<body>
    <h1>Advanced Scenarios Test Page</h1>
    <p>This page demonstrates advanced testing scenarios including SPA behavior.</p>
    
    <button onclick="loadContent()">Load Content Dynamically</button>
    <button onclick="getLocation()">Get Location</button>
    
    <div id="content"></div>
    
    <script>
        function loadContent() {
            const content = document.getElementById('content');
            content.innerHTML = '<h2>Dynamic Content Loaded</h2><p>This content was loaded dynamically, simulating SPA behavior.</p>';
        }
        
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    document.getElementById('content').innerHTML = 
                        '<p>Latitude: ' + position.coords.latitude + '</p>' +
                        '<p>Longitude: ' + position.coords.longitude + '</p>';
                });
            } else {
                document.getElementById('content').innerHTML = '<p>Geolocation is not supported.</p>';
            }
        }
    </script>
</body>
</html>
```

## Testing SPAs

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_spa_waiting():
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
            
            # Wait for network to be idle (SPA loaded)
            page.wait_for_load_state("networkidle")
            
            # Click button to load dynamic content
            page.click("button:has-text('Load Content Dynamically')")
            page.wait_for_selector("#content", state="visible")
            print("✓ SPA dynamic content loaded")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_spa_waiting()
```

## Handling Authentication

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys
import os

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_with_auth():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)
            
            context = browser.new_context()
            page = context.new_page()
            
            # Navigate to page (simulating login)
            page.goto(get_file_url())
            
            # Save auth state
            auth_file = Path(__file__).parent / "auth.json"
            context.storage_state(path=str(auth_file))
            
            print("✓ Auth state saved")
            
            # Cleanup
            if auth_file.exists():
                auth_file.unlink()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_with_auth()
```

## Testing File Uploads

```python
from playwright.sync_api import sync_playwright, expect
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_file_upload():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes with file operations
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            page.goto(get_file_url())
            
            # Create a test file
            test_file = Path(__file__).parent / "test_upload.txt"
            with open(test_file, "w") as f:
                f.write("Test content")
            
            with page.expect_file_chooser() as fc_info:
                page.click("button#upload")
            
            file_chooser = fc_info.value
            file_chooser.set_files(str(test_file))
            
            print("✓ File upload handled")
            
            # Cleanup
            if test_file.exists():
                test_file.unlink()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_file_upload()
```

## Testing Geolocation

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_geolocation():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            
            context = browser.new_context(
                geolocation={"latitude": 40.7128, "longitude": -74.0060},
                permissions=["geolocation"]
            )
            page = context.new_page()
            page.goto(get_file_url())
            
            # Click button to get location
            page.click("button:has-text('Get Location')")
            page.wait_for_timeout(1000)
            print("✓ Geolocation configured and tested")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_geolocation()
```

## WebSocket Testing

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_websocket():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            
            messages = []
            
            def handle_websocket(ws):
                ws.on("framereceived", lambda event: messages.append(event.payload))
            
            page.on("websocket", handle_websocket)
            page.goto(get_file_url())
            
            # Wait for messages
            page.wait_for_timeout(2000)
            
            print(f"✓ Received {len(messages)} messages")
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_websocket()
```

## Best Practices

1. **Wait appropriately**: SPAs need special waiting
2. **Save auth state**: Reuse authentication
3. **Handle async operations**: WebSockets, etc.
4. **Test edge cases**: Geolocation, permissions
5. **Isolate tests**: Each test independent
6. **Platform-specific handling**: On macOS, use Firefox to avoid Chromium crashes
7. **Use try/finally**: Always ensure browser cleanup with try/finally blocks

## Next Steps

Learn about:
- Best practices
- Optimizing test performance
- Maintaining test suites

