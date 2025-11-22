# File Downloads

Handling file downloads is essential for testing applications that allow users to download files. This tutorial covers how to handle file downloads in Playwright.

## Overview

Playwright provides ways to:
- Wait for downloads
- Get download information
- Save downloaded files
- Verify download content
- Handle file chooser dialogs

## Basic Download Handling

```python
from playwright.sync_api import sync_playwright

def test_download():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/download")
        
        # Wait for download
        with page.expect_download() as download_info:
            page.click("a#download-link")
        
        download = download_info.value
        
        # Save downloaded file
        download.save_as("downloaded_file.pdf")
        
        print(f"Downloaded: {download.suggested_filename()}")
        
        browser.close()

if __name__ == "__main__":
    test_download()
```

## Getting Download Information

```python
from playwright.sync_api import sync_playwright

def test_download_info():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/download")
        
        with page.expect_download() as download_info:
            page.click("a#download-link")
        
        download = download_info.value
        
        # Get download information
        filename = download.suggested_filename()
        url = download.url
        path = download.path()
        
        print(f"Filename: {filename}")
        print(f"URL: {url}")
        print(f"Path: {path}")
        
        browser.close()

if __name__ == "__main__":
    test_download_info()
```

## Download Path

Access the download path:

```python
from playwright.sync_api import sync_playwright
import os

def test_download_path():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/download")
        
        with page.expect_download() as download_info:
            page.click("a#download-link")
        
        download = download_info.value
        
        # Get temporary download path
        path = download.path()
        
        if os.path.exists(path):
            print(f"File downloaded to: {path}")
        
        # Save with custom name
        download.save_as("custom_name.pdf")
        
        browser.close()

if __name__ == "__main__":
    test_download_path()
```

## File Upload Dialog

Handle file upload dialogs:

```python
from playwright.sync_api import sync_playwright

def test_file_upload():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/upload")
        
        # Handle file chooser
        with page.expect_file_chooser() as fc_info:
            page.click("button#upload")
        
        file_chooser = fc_info.value
        file_chooser.set_files("path/to/file.pdf")
        
        browser.close()

if __name__ == "__main__":
    test_file_upload()
```

## Multiple File Upload

Upload multiple files:

```python
from playwright.sync_api import sync_playwright

def test_multiple_files():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/upload")
        
        with page.expect_file_chooser() as fc_info:
            page.click("button#upload")
        
        file_chooser = fc_info.value
        file_chooser.set_files([
            "path/to/file1.pdf",
            "path/to/file2.pdf"
        ])
        
        browser.close()

if __name__ == "__main__":
    test_multiple_files()
```

## Verifying Download Content

Verify downloaded file content:

```python
from playwright.sync_api import sync_playwright
import os

def test_verify_download():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/download")
        
        with page.expect_download() as download_info:
            page.click("a#download-link")
        
        download = download_info.value
        download.save_as("downloaded_file.pdf")
        
        # Verify file exists
        if os.path.exists("downloaded_file.pdf"):
            file_size = os.path.getsize("downloaded_file.pdf")
            print(f"File size: {file_size} bytes")
        
        browser.close()

if __name__ == "__main__":
    test_verify_download()
```

## Setting Download Path

Configure download directory:

```python
from playwright.sync_api import sync_playwright

def test_download_directory():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # Set download directory
        context = browser.new_context(
            accept_downloads=True
        )
        
        page = context.new_page()
        page.goto("https://example.com/download")
        
        with page.expect_download() as download_info:
            page.click("a#download-link")
        
        download = download_info.value
        download.save_as("downloads/file.pdf")
        
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

## Common Patterns

```python
# Pattern 1: Basic download
with page.expect_download() as download_info:
    page.click("a")
download = download_info.value
download.save_as("file.pdf")

# Pattern 2: File upload
with page.expect_file_chooser() as fc_info:
    page.click("button")
fc_info.value.set_files("file.pdf")
```

## Next Steps

Now that you understand file downloads, learn about:
- Test organization with pytest
- Page Object Model
- Parallel execution

