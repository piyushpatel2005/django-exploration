# Cookies and Storage

Managing cookies and browser storage is essential for testing authenticated sessions and maintaining state. This tutorial covers working with cookies, local storage, and session storage in Playwright.

## Overview

Playwright allows you to:
- Get and set cookies
- Clear cookies
- Manage local storage
- Manage session storage
- Set authentication state

## Cookies

### Getting Cookies

```python
from playwright.sync_api import sync_playwright

def test_get_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://example.com")
        
        # Get all cookies
        cookies = context.cookies()
        print(f"Cookies: {cookies}")
        
        # Get cookies for specific URL
        cookies = context.cookies("https://example.com")
        
        browser.close()

if __name__ == "__main__":
    test_get_cookies()
```

### Setting Cookies

```python
from playwright.sync_api import sync_playwright

def test_set_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # Set cookies before navigation
        context.add_cookies([
            {
                "name": "session_id",
                "value": "abc123",
                "domain": "example.com",
                "path": "/"
            }
        ])
        
        page = context.new_page()
        page.goto("https://example.com")
        
        # Verify cookie was set
        cookies = context.cookies()
        print(f"Cookies: {cookies}")
        
        browser.close()

if __name__ == "__main__":
    test_set_cookies()
```

### Clearing Cookies

```python
from playwright.sync_api import sync_playwright

def test_clear_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://example.com")
        
        # Clear all cookies
        context.clear_cookies()
        
        # Clear cookies for specific URL
        context.clear_cookies(url="https://example.com")
        
        browser.close()

if __name__ == "__main__":
    test_clear_cookies()
```

## Local Storage

### Getting Local Storage

```python
from playwright.sync_api import sync_playwright

def test_get_local_storage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Get local storage items
        storage = page.evaluate("() => ({ ...localStorage })")
        print(f"Local storage: {storage}")
        
        # Get specific item
        value = page.evaluate("() => localStorage.getItem('key')")
        print(f"Value: {value}")
        
        browser.close()

if __name__ == "__main__":
    test_get_local_storage()
```

### Setting Local Storage

```python
from playwright.sync_api import sync_playwright

def test_set_local_storage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Set local storage before navigation
        page.add_init_script("""
            localStorage.setItem('user', 'John Doe');
            localStorage.setItem('theme', 'dark');
        """)
        
        page.goto("https://example.com")
        
        # Verify storage
        user = page.evaluate("() => localStorage.getItem('user')")
        print(f"User: {user}")
        
        browser.close()

if __name__ == "__main__":
    test_set_local_storage()
```

### Clearing Local Storage

```python
from playwright.sync_api import sync_playwright

def test_clear_local_storage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Clear local storage
        page.evaluate("() => localStorage.clear()")
        
        # Remove specific item
        page.evaluate("() => localStorage.removeItem('key')")
        
        browser.close()

if __name__ == "__main__":
    test_clear_local_storage()
```

## Session Storage

Session storage works similarly to local storage:

```python
from playwright.sync_api import sync_playwright

def test_session_storage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Set session storage
        page.add_init_script("""
            sessionStorage.setItem('session', 'active');
        """)
        
        page.goto("https://example.com")
        
        # Get session storage
        session = page.evaluate("() => sessionStorage.getItem('session')")
        print(f"Session: {session}")
        
        # Clear session storage
        page.evaluate("() => sessionStorage.clear()")
        
        browser.close()

if __name__ == "__main__":
    test_session_storage()
```

## Authentication State

Save and reuse authentication state:

```python
from playwright.sync_api import sync_playwright
import json

def test_auth_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Login (example)
        page.goto("https://example.com/login")
        page.fill("input[name='username']", "user")
        page.fill("input[name='password']", "pass")
        page.click("button[type='submit']")
        
        # Save authentication state
        context.storage_state(path="auth.json")
        
        browser.close()
        
        # Reuse authentication state
        browser2 = p.chromium.launch(headless=False)
        context2 = browser2.new_context(storage_state="auth.json")
        page2 = context2.new_page()
        page2.goto("https://example.com/dashboard")
        
        browser2.close()

if __name__ == "__main__":
    test_auth_state()
```

## Best Practices

1. **Set storage before navigation**: Use `add_init_script()` or context setup
2. **Save auth state**: Reuse authentication across tests
3. **Isolate contexts**: Each context has separate storage
4. **Clear between tests**: Ensure test isolation
5. **Verify storage**: Check that storage was set correctly

## Common Patterns

```python
# Pattern 1: Set cookies before navigation
context.add_cookies([{"name": "key", "value": "value", "domain": "example.com"}])

# Pattern 2: Set local storage
page.add_init_script("localStorage.setItem('key', 'value')")

# Pattern 3: Save auth state
context.storage_state(path="auth.json")

# Pattern 4: Reuse auth state
context = browser.new_context(storage_state="auth.json")
```

## Next Steps

Now that you understand storage, learn about:
- Screenshots and videos
- Network interception
- File downloads

