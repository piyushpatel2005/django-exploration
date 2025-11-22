# Installation and Setup

Before we can start writing Playwright tests, we need to install Playwright and set up our development environment. This tutorial will guide you through the installation process.

## Overview

Installing Playwright involves two main steps:
1. Installing the Playwright Python package
2. Installing browser binaries

## Installing Playwright

The easiest way to install Playwright is using `pip`, Python's package manager.

### Using pip

```shell{ .show-prompt lineNos=false }
pip install playwright
```

### Using pip with virtual environment (Recommended)

It's a best practice to use a virtual environment to isolate your project dependencies:

```shell{ .show-prompt lineNos=false }
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install playwright
```

## Installing Browser Binaries

After installing the Playwright package, you need to install the browser binaries. Playwright provides a command-line tool for this:

```shell{ .show-prompt lineNos=false }
playwright install
```

This command downloads Chromium, Firefox, and WebKit browsers. If you only need specific browsers, you can install them individually:

```shell{ .show-prompt lineNos=false }
playwright install chromium
playwright install firefox
playwright install webkit
```

## Verifying Installation

Let's create a simple script to verify that Playwright is installed correctly.

Create a file `main.py`:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

def main():
    # Get the path to the HTML file in the same directory
    html_file = Path(__file__).parent / "index.html"
    file_url = f"file://{html_file.absolute()}"
    
    with sync_playwright() as p:
        # Launch browser in headless mode (more stable)
        # Change headless=False if you want to see the browser window
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(file_url)
        print(f"Page title: {page.title()}")
        browser.close()

if __name__ == "__main__":
    main()
```

Run the script:

```shell{ .show-prompt lineNos=false }
python main.py
```

If everything is set up correctly, you should see:
- The script runs (browser runs in headless mode by default)
- Prints the page title
- Browser closes automatically

```output{ lineNos=false }
Page title: Playwright Test Page
```

**Note:** The browser runs in headless mode by default (`headless=True`). If you want to see the browser window, change `headless=True` to `headless=False` in the code above.

## Project Structure

For a typical Playwright project, you might organize your files like this:

```
project/
├── tests/
│   ├── test_example.py
│   └── test_login.py
├── pages/
│   └── login_page.py
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## Requirements File

Create a `requirements.txt` file to manage dependencies:

```txt
playwright==1.40.0
pytest==7.4.3
pytest-playwright==0.4.3
```

Then install all dependencies:

```shell{ .show-prompt lineNos=false }
pip install -r requirements.txt
```

## Common Installation Issues

### Issue: Browser binaries not found

If you get an error about browsers not being found, run:

```shell{ .show-prompt lineNos=false }
playwright install --force
```

### Issue: Permission errors on Linux/Mac

You might need to install system dependencies:

```shell{ .show-prompt lineNos=false }
playwright install-deps
```

### Issue: Python version

Playwright requires Python 3.8 or higher. Check your Python version:

```shell{ .show-prompt lineNos=false }
python --version
```

### Issue: TargetClosedError on macOS

If you encounter `TargetClosedError` when using `headless=False` on macOS, this is often due to system security settings. Solutions:

1. **Use headless mode** (recommended for automated testing):
   ```python
   browser = p.chromium.launch(headless=True)
   ```

2. **Reinstall browser binaries**:
   ```shell
   playwright install --force chromium
   ```

3. **Check macOS security settings** - Ensure Terminal/iTerm has necessary permissions in System Preferences > Security & Privacy

## Next Steps

Now that Playwright is installed, you're ready to write your first test! In the next tutorial, we'll create a simple test and learn the basic structure of Playwright tests.

