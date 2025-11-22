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

def test_access_frame():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Access frame by name
        frame = page.frame(name="frame-name")
        
        # Access frame by URL
        frame = page.frame(url=r".*example.*")
        
        # Access frame by locator
        frame_element = page.locator("iframe")
        frame = frame_element.content_frame()
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Get frame
        frame_element = page.locator("iframe")
        frame = frame_element.content_frame()
        
        if frame:
            # Interact with elements inside frame
            heading = frame.locator("h1")
            heading.click()
            
            # Type in frame
            input_field = frame.locator("input")
            input_field.fill("Hello")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Wait for frame to appear
        frame_element = page.locator("iframe")
        frame_element.wait_for(state="attached")
        
        # Get frame content
        frame = frame_element.content_frame()
        
        if frame:
            # Wait for frame content to load
            frame.wait_for_load_state("load")
            
            # Interact with frame
            heading = frame.locator("h1")
            heading.wait_for(state="visible")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        frame_element = page.locator("iframe")
        frame = frame_element.content_frame()
        
        if frame:
            # Assert frame content
            heading = frame.locator("h1")
            expect(heading).to_be_visible()
            expect(heading).to_have_text("Expected Text")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
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

## Common Patterns

```python
# Pattern 1: Access frame by locator
frame_element = page.locator("iframe")
frame = frame_element.content_frame()
if frame:
    frame.locator("button").click()

# Pattern 2: Access frame by name
frame = page.frame(name="my-frame")
if frame:
    frame.locator("input").fill("text")

# Pattern 3: Wait for frame
frame_element = page.locator("iframe")
frame_element.wait_for(state="attached")
frame = frame_element.content_frame()
```

## Next Steps

Now that you can work with frames, learn about:
- Navigation and URL handling
- Cookies and storage
- Screenshots and videos

