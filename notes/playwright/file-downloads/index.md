# File Downloads

Handling file downloads is essential for testing applications that allow users to download files. This tutorial covers how to handle file downloads in Playwright.

## Overview

Playwright provides ways to:
- Wait for downloads
- Get download information
- Save downloaded files
- Verify download content
- Handle file chooser dialogs

## Test Page

The examples in this tutorial use the following HTML page:

**index.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Downloads</title>
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
        input[type="file"] {
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>File Downloads Test Page</h1>
    
    <div>
        <a href="test-file.txt" download="test-file.txt">
            <button>Download Text File</button>
        </a>
    </div>
    
    <div>
        <h2>File Upload</h2>
        <input type="file" id="file-input">
        <button onclick="document.getElementById('file-input').click()">Upload File</button>
    </div>
</body>
</html>
```

## Basic Download Handling

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import os
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_download():
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
            
            # Wait for download
            with page.expect_download() as download_info:
                page.click("a[href*='test-file.txt']")
            
            download = download_info.value
            
            # Save downloaded file
            download_path = Path(__file__).parent / "downloaded_file.txt"
            download.save_as(str(download_path))
            
            print(f"✓ Downloaded: {download.suggested_filename}")
            
            # Cleanup
            if download_path.exists():
                download_path.unlink()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_download()
```

## Getting Download Information

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_download_info():
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
            
            with page.expect_download() as download_info:
                page.click("a[href*='test-file.txt']")
            
            download = download_info.value
            
            # Get download information
            filename = download.suggested_filename
            url = download.url
            
            print(f"✓ Download filename: {filename}")
            print(f"✓ Download URL: {url}")
            
            # Save download
            download_path = Path(__file__).parent / "downloaded_file.txt"
            download.save_as(str(download_path))
            
            if download_path.exists():
                print("✓ File downloaded successfully")
                download_path.unlink()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_download_info()
```

## Download Path

Access the download path:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import os
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_download_path():
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
            
            with page.expect_download() as download_info:
                page.click("a[href*='test-file.txt']")
            
            download = download_info.value
            
            # Get temporary download path
            path = download.path()
            
            if os.path.exists(path):
                print(f"✓ File downloaded to: {path}")
            
            # Save with custom name
            download_path = Path(__file__).parent / "custom_name.txt"
            download.save_as(str(download_path))
            
            if download_path.exists():
                download_path.unlink()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_download_path()
```

## File Upload Dialog

Handle file upload dialogs:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import os
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
            
            # Handle file chooser
            with page.expect_file_chooser() as fc_info:
                page.click("button:has-text('Upload File')")
            
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

## Multiple File Upload

Upload multiple files:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_multiple_files():
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
            
            # Create test files
            test_file1 = Path(__file__).parent / "test_file1.txt"
            test_file2 = Path(__file__).parent / "test_file2.txt"
            
            with open(test_file1, "w") as f:
                f.write("File 1 content")
            with open(test_file2, "w") as f:
                f.write("File 2 content")
            
            with page.expect_file_chooser() as fc_info:
                page.click("button:has-text('Upload File')")
            
            file_chooser = fc_info.value
            file_chooser.set_files([
                str(test_file1),
                str(test_file2)
            ])
            
            print("✓ Multiple files uploaded")
            
            # Cleanup
            if test_file1.exists():
                test_file1.unlink()
            if test_file2.exists():
                test_file2.unlink()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_multiple_files()
```

## Verifying Download Content

Verify downloaded file content:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import os
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_verify_download():
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
            
            with page.expect_download() as download_info:
                page.click("a[href*='test-file.txt']")
            
            download = download_info.value
            download_path = Path(__file__).parent / "downloaded_file.txt"
            download.save_as(str(download_path))
            
            # Verify file exists
            if download_path.exists():
                file_size = os.path.getsize(download_path)
                print(f"✓ File size: {file_size} bytes")
                
                # Read and verify content
                with open(download_path, "r") as f:
                    content = f.read()
                    print(f"✓ File content: {content[:50]}...")
                
                download_path.unlink()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_verify_download()
```

## Setting Download Path

Configure download directory:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_download_directory():
    with sync_playwright() as p:
        browser = None
        try:
            # Use Firefox on macOS to avoid Chromium crashes with file operations
            if sys.platform == "darwin":  # macOS
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.chromium.launch(headless=True)
            
            # Set download directory
            context = browser.new_context(
                accept_downloads=True
            )
            
            page = context.new_page()
            page.goto(get_file_url())
            
            with page.expect_download() as download_info:
                page.click("a[href*='test-file.txt']")
            
            download = download_info.value
            
            # Create downloads directory if it doesn't exist
            downloads_dir = Path(__file__).parent / "downloads"
            downloads_dir.mkdir(exist_ok=True)
            
            download_path = downloads_dir / "file.txt"
            download.save_as(str(download_path))
            
            if download_path.exists():
                print(f"✓ File saved to: {download_path}")
                download_path.unlink()
                downloads_dir.rmdir()
        finally:
            if browser:
                browser.close()

if __name__ == "__main__":
    test_download_directory()
```

## Best Practices

1. **Wait for downloads**: Use `expect_download()` before clicking
2. **Save files explicitly**: Use `save_as()` to control file location
3. **Verify downloads**: Check file existence and size
4. **Clean up**: Delete test files after verification
5. **Handle failures**: Check if download completed successfully
6. **Platform-specific handling**: On macOS, use Firefox for file operations to avoid Chromium crashes
7. **Use try/finally**: Always ensure browser cleanup with try/finally blocks

## Common Patterns

```python
# Pattern 1: Basic download
browser = None
try:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True) if sys.platform == "darwin" else p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(get_file_url())
        
        with page.expect_download() as download_info:
            page.click("a")
        download = download_info.value
        download.save_as("file.txt")
finally:
    if browser:
        browser.close()

# Pattern 2: File upload
browser = None
try:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True) if sys.platform == "darwin" else p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(get_file_url())
        
        with page.expect_file_chooser() as fc_info:
            page.click("button")
        fc_info.value.set_files("file.txt")
finally:
    if browser:
        browser.close()
```

## macOS Considerations

On macOS, Chromium may crash when handling file operations in headless mode. To avoid this:

1. Use Firefox instead of Chromium for file operations
2. Always use try/finally blocks for proper cleanup
3. Add small delays between tests if running multiple file operations

## Next Steps

Now that you understand file downloads, learn about:
- Test organization with pytest
- Page Object Model
- Parallel execution

