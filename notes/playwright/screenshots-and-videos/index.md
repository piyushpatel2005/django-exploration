# Screenshots and Videos

Capturing screenshots and recording videos is essential for debugging tests and visual regression testing. This tutorial covers how to take screenshots and record videos in Playwright.

## Overview

Playwright can capture:
- Full page screenshots
- Element screenshots
- Screenshots on failure (automatic)
- Video recordings
- PDF generation

## Taking Screenshots

### Full Page Screenshot

```python
from playwright.sync_api import sync_playwright

def test_full_page_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Take full page screenshot
        page.screenshot(path="screenshot.png")
        
        # Screenshot with options
        page.screenshot(
            path="screenshot.png",
            full_page=True,  # Capture full page, not just viewport
            type="png"  # or "jpeg"
        )
        
        browser.close()

if __name__ == "__main__":
    test_full_page_screenshot()
```

### Element Screenshot

```python
from playwright.sync_api import sync_playwright

def test_element_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Screenshot of specific element
        heading = page.locator("h1")
        heading.screenshot(path="heading.png")
        
        browser.close()

if __name__ == "__main__":
    test_element_screenshot()
```

### Screenshot Options

```python
from playwright.sync_api import sync_playwright

def test_screenshot_options():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Screenshot with various options
        page.screenshot(
            path="screenshot.png",
            full_page=True,
            clip={"x": 0, "y": 0, "width": 800, "height": 600},  # Crop area
            quality=90,  # For JPEG
            animations="disabled"  # Disable animations
        )
        
        browser.close()

if __name__ == "__main__":
    test_screenshot_options()
```

## Automatic Screenshots on Failure

Configure automatic screenshots when tests fail:

```python
from playwright.sync_api import sync_playwright

def test_auto_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # Enable screenshot on failure
        context.tracing.start(screenshots=True, snapshots=True)
        
        page = context.new_page()
        page.goto("https://example.com")
        
        # If test fails, screenshot is automatically saved
        try:
            page.locator(".non-existent").click()
        except:
            context.tracing.stop(path="trace.zip")
        
        browser.close()

if __name__ == "__main__":
    test_auto_screenshot()
```

## Video Recording

Record videos of test execution:

```python
from playwright.sync_api import sync_playwright

def test_video_recording():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # Enable video recording
        context = browser.new_context(
            record_video_dir="videos/",
            record_video_size={"width": 1280, "height": 720}
        )
        
        page = context.new_page()
        page.goto("https://example.com")
        
        # Perform actions
        page.click("a")
        
        # Video is automatically saved when context closes
        context.close()
        browser.close()

if __name__ == "__main__":
    test_video_recording()
```

## PDF Generation

Generate PDFs of pages:

```python
from playwright.sync_api import sync_playwright

def test_pdf_generation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Generate PDF
        page.pdf(
            path="page.pdf",
            format="A4",
            print_background=True
        )
        
        browser.close()

if __name__ == "__main__":
    test_pdf_generation()
```

## Visual Regression Testing

Compare screenshots for visual regression:

```python
from playwright.sync_api import sync_playwright
import os

def test_visual_regression():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Take screenshot
        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path)
        
        # Compare with baseline (you'd use a library like pytest-playwright)
        baseline_path = "baseline.png"
        
        if os.path.exists(baseline_path):
            # Compare images (simplified example)
            print("Compare screenshots manually or use a library")
        
        browser.close()

if __name__ == "__main__":
    test_visual_regression()
```

## Best Practices

1. **Use full_page for long pages**: Capture entire page content
2. **Disable animations**: For consistent screenshots
3. **Record videos for debugging**: Especially for CI/CD
4. **Save screenshots on failure**: Automatic debugging aid
5. **Use consistent viewport**: For reliable visual tests

## Common Patterns

```python
# Pattern 1: Full page screenshot
page.screenshot(path="full.png", full_page=True)

# Pattern 2: Element screenshot
element.screenshot(path="element.png")

# Pattern 3: Video recording
context = browser.new_context(record_video_dir="videos/")

# Pattern 4: PDF generation
page.pdf(path="page.pdf")
```

## Next Steps

Now that you can capture screenshots and videos, learn about:
- Network interception
- File downloads
- Test organization

