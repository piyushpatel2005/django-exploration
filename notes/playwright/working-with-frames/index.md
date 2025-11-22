# Working with Frames and iframes

Many web applications use frames or iframes to embed content from other sources. This tutorial covers how to work with frames in Playwright.

## Overview

Frames (iframes) are HTML documents embedded within other HTML documents. Playwright provides methods to:
- Access frame content
- Switch between frames
- Interact with elements inside frames
- Handle nested frames

## Accessing Frames

### By Name or URL

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_access_frame():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Access frame by name
        frame = page.frame(name="frame-name")
        
        # Access frame by URL
        frame = page.frame(url=r".*example.*")
        
        # Access frame using frame_locator (recommended approach)
        frame_locator = page.frame_locator("iframe").first
        
        # Or access frame directly by name
        frame = page.frame(name="content-frame")
        
        browser.close()

if __name__ == "__main__":
    test_access_frame()
```

## Interacting with Frame Content

Once you have a frame reference, interact with it like a page:

```python
from playwright.sync_api import sync_playwright

def test_frame_interaction():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Wait for page to load frames
        page.wait_for_load_state("load")
        
        # Use frame_locator to access frame content
        # frame_locator returns a FrameLocator that can locate elements inside the frame
        frame_locator = page.frame_locator("iframe").first
        
        # Interact with elements inside frame using frame_locator
        heading = frame_locator.locator("h1")
        if heading.count() > 0:
            print(f"✓ Frame heading: {heading.first.text_content()}")
        
        button = frame_locator.locator("button")
        if button.count() > 0:
            print(f"✓ Found button in frame")
        
        browser.close()

if __name__ == "__main__":
    test_frame_interaction()
```

## Finding Frames

Find all frames on a page:

```python
from playwright.sync_api import sync_playwright

def test_find_frames():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Get all frames
        frames = page.frames
        print(f"Total frames: {len(frames)}")
        
        # Access main frame
        main_frame = page.main_frame
        
        # Access child frames
        for frame in frames:
            print(f"Frame URL: {frame.url}")
        
        browser.close()

if __name__ == "__main__":
    test_find_frames()
```

## Waiting for Frames

Wait for a frame to load:

```python
from playwright.sync_api import sync_playwright

def test_wait_for_frame():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Wait for page to load
        page.wait_for_load_state("load")
        
        # Use frame_locator to access frame content
        frame_locator = page.frame_locator("iframe").first
        
        # Wait for frame content to be ready
        heading = frame_locator.locator("h1")
        heading.wait_for(state="visible")
        
        # Interact with frame elements
        heading.click()
        
        browser.close()

if __name__ == "__main__":
    test_wait_for_frame()
```

## Nested Frames

Handle nested frames (frames within frames):

```python
from playwright.sync_api import sync_playwright

def test_nested_frames():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Access outer frame
        outer_frame = page.frame(name="outer-frame")
        
        if outer_frame:
            # Access inner frame
            inner_frame = outer_frame.frame(name="inner-frame")
            
            if inner_frame:
                # Interact with inner frame
                element = inner_frame.locator("button")
                element.click()
        
        browser.close()

if __name__ == "__main__":
    test_nested_frames()
```

## Frame Assertions

Assert frame content:

```python
from playwright.sync_api import sync_playwright, expect

def test_frame_assertions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Use frame_locator to access frame content
        frame_locator = page.frame_locator("iframe").first
        
        # Assert frame content
        heading = frame_locator.locator("h1")
        if heading.count() > 0:
            expect(heading.first).to_be_visible()
            expect(heading.first).to_have_text("Frame Content")
            print(f"✓ Frame heading: {heading.first.text_content()}")
        
        browser.close()

if __name__ == "__main__":
    test_frame_assertions()
```

## Switching Between Frames

Switch between multiple frames:

```python
from playwright.sync_api import sync_playwright

def test_switch_frames():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Work with main page
        main_heading = page.locator("h1")
        
        # Switch to frame
        frame = page.frame(name="content-frame")
        if frame:
            frame_heading = frame.locator("h1")
            frame_heading.click()
        
        # Back to main page
        main_heading.click()
        
        browser.close()

if __name__ == "__main__":
    test_switch_frames()
```

## Frame URL and Name

Get frame information:

```python
from playwright.sync_api import sync_playwright

def test_frame_info():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        frames = page.frames
        
        for frame in frames:
            print(f"Frame name: {frame.name}")
            print(f"Frame URL: {frame.url}")
            print(f"Parent frame: {frame.parent_frame}")
        
        browser.close()

if __name__ == "__main__":
    test_frame_info()
```

## Best Practices

1. **Wait for frames**: Always wait for frames to load before interacting
2. **Check frame existence**: Verify frame exists before accessing
3. **Use frame locators**: Prefer `frame.locator()` over `page.locator()` for frame content
4. **Handle nested frames**: Be aware of frame hierarchy
5. **Frame isolation**: Remember frames are isolated contexts
6. **Avoid strict mode violations**: Use `.first` or specific selectors when multiple iframes exist
7. **Use specific selectors**: Prefer ID or name selectors over generic `iframe` selector

## Common Patterns

```python
# Pattern 1: Use frame_locator (recommended - works with multiple iframes)
frame_locator = page.frame_locator("iframe").first
frame_locator.locator("button").click()

# Pattern 2: Access frame by name (returns Frame object)
frame = page.frame(name="content-frame")
if frame:
    frame.locator("input").fill("text")

# Pattern 3: Use frame_locator with specific selector
frame_locator = page.frame_locator("#test-frame")
frame_locator.locator("h1").click()

# Pattern 4: Use frame_locator with name attribute
frame_locator = page.frame_locator("iframe[name='content-frame']")
frame_locator.locator("button").click()
```

## Important: frame_locator vs locator

There are two ways to work with frames in Playwright:

### Method 1: frame_locator() (Recommended)

`frame_locator()` returns a `FrameLocator` that can locate elements inside the frame:

```python
# ✅ Correct: Use frame_locator
frame_locator = page.frame_locator("iframe").first
heading = frame_locator.locator("h1")
heading.click()
```

### Method 2: frame() (For direct Frame access)

`frame()` returns a `Frame` object directly:

```python
# ✅ Correct: Use frame by name
frame = page.frame(name="content-frame")
if frame:
    heading = frame.locator("h1")
    heading.click()
```

### ❌ Incorrect: Using locator().content_frame()

```python
# ❌ This doesn't work - content_frame() is not available on Locator
frame_element = page.locator("iframe")
frame = frame_element.content_frame()  # AttributeError!
```

## Strict Mode and Multiple Frames

When a page has multiple iframes, use `.first` or specific selectors:

```python
# ✅ Use .first for the first iframe
frame_locator = page.frame_locator("iframe").first

# ✅ Or use a more specific selector
frame_locator = page.frame_locator("#test-frame")  # By ID
frame_locator = page.frame_locator("iframe[name='content-frame']")  # By name
```

## HTML Pages for Testing

Here are the HTML pages used in the examples above:

**index.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Working with Frames</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        iframe {
            width: 100%;
            height: 300px;
            border: 2px solid #3498db;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>Working with Frames</h1>
    <p>This page contains iframes for testing frame interactions.</p>
    
    <iframe name="content-frame" id="test-frame" src="frame-content.html"></iframe>
    
    <iframe name="nested-frame" src="nested-frame.html"></iframe>
</body>
</html>
```

**frame-content.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Frame Content</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f0f0f0;
        }
        h1 {
            color: #2c3e50;
        }
        button {
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Frame Content</h1>
    <p>This is content inside an iframe.</p>
    <button>Click Me</button>
</body>
</html>
```

## Next Steps

Now that you can work with frames, learn about:
- Navigation and URL handling
- Cookies and storage
- Screenshots and videos

