# Page Object Model (POM)

Page Object Model is a design pattern that improves test maintainability by encapsulating page elements and actions in classes. This tutorial covers implementing POM with Playwright.

## Overview

Page Object Model:
- Separates test logic from page interactions
- Makes tests more readable
- Improves maintainability
- Reduces code duplication

## Basic Page Object

```python
class HomePage:
    def __init__(self, page):
        self.page = page
        self.heading = page.locator("h1")
        self.search_box = page.locator("input[type='search']")
        self.search_button = page.locator("button[type='submit']")
    
    def goto(self):
        self.page.goto("https://example.com")
    
    def search(self, query):
        self.search_box.fill(query)
        self.search_button.click()
```

## Using Page Objects

```python
from playwright.sync_api import sync_playwright

def test_with_page_object():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        home_page = HomePage(page)
        home_page.goto()
        home_page.search("Playwright")
        
        browser.close()
```

## Complete Example

```python
# pages/home_page.py
class HomePage:
    def __init__(self, page):
        self.page = page
        self.url = "https://example.com"
    
    def goto(self):
        self.page.goto(self.url)
    
    def get_heading_text(self):
        return self.page.locator("h1").text_content()
    
    def click_link(self, link_text):
        self.page.get_by_text(link_text).click()

# pages/login_page.py
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.submit_button = page.locator("button[type='submit']")
    
    def goto(self):
        self.page.goto("https://example.com/login")
    
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()

# tests/test_login.py
def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login("user", "pass")
        
        browser.close()
```

## Base Page Class

Create a base class for common functionality:

```python
class BasePage:
    def __init__(self, page):
        self.page = page
    
    def goto(self, url):
        self.page.goto(url)
    
    def get_title(self):
        return self.page.title()
    
    def take_screenshot(self, path):
        self.page.screenshot(path=path)

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://example.com"
    
    def goto(self):
        super().goto(self.url)
```

## Best Practices

1. **One page object per page**: Keep pages separate
2. **Return page objects**: Return next page from actions
3. **Use locators**: Store locators as properties
4. **Keep it simple**: Don't overcomplicate
5. **Reuse common code**: Use base classes

## Next Steps

Now that you understand POM, learn about:
- Parallel execution
- Configuration
- Error handling

