# Test Organization with Pytest

Organizing tests with pytest makes them more maintainable and allows you to leverage pytest's powerful features. This tutorial covers organizing Playwright tests with pytest.

## Overview

Pytest provides:
- Test discovery
- Fixtures for setup/teardown
- Parametrized tests
- Test grouping and markers
- Plugins and extensions

## Installing Pytest Playwright

```shell{ .show-prompt lineNos=false }
pip install pytest pytest-playwright
playwright install
```

## Basic Pytest Test

```python
from playwright.sync_api import Page, expect

def test_example(page: Page):
    page.goto("https://example.com")
    expect(page).to_have_title("Example Domain")
```

Run the test:

```shell{ .show-prompt lineNos=false }
pytest test_example.py
```

## Using Pytest Fixtures

### Browser Fixture

```python
import pytest
from playwright.sync_api import Page, BrowserContext

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080}
    }

def test_with_fixture(page: Page):
    page.goto("https://example.com")
    assert page.title() == "Example Domain"
```

### Custom Fixtures

```python
import pytest
from playwright.sync_api import Page

@pytest.fixture
def logged_in_page(page: Page):
    """Fixture that logs in before test."""
    page.goto("https://example.com/login")
    page.fill("input[name='username']", "user")
    page.fill("input[name='password']", "pass")
    page.click("button[type='submit']")
    return page

def test_dashboard(logged_in_page):
    logged_in_page.goto("https://example.com/dashboard")
    assert "Dashboard" in logged_in_page.title()
```

## Parametrized Tests

Run the same test with different inputs:

```python
import pytest
from playwright.sync_api import Page

@pytest.mark.parametrize("url,expected_title", [
    ("https://example.com", "Example Domain"),
    ("https://playwright.dev", "Playwright"),
])
def test_multiple_sites(page: Page, url, expected_title):
    page.goto(url)
    assert expected_title in page.title()
```

## Test Classes

Organize tests into classes:

```python
from playwright.sync_api import Page, expect

class TestHomePage:
    def test_title(self, page: Page):
        page.goto("https://example.com")
        expect(page).to_have_title("Example Domain")
    
    def test_heading(self, page: Page):
        page.goto("https://example.com")
        heading = page.locator("h1")
        expect(heading).to_be_visible()
```

## Markers

Use markers to categorize tests:

```python
import pytest
from playwright.sync_api import Page

@pytest.mark.slow
def test_slow_operation(page: Page):
    page.goto("https://example.com")
    # Slow test here
    pass

@pytest.mark.smoke
def test_smoke(page: Page):
    page.goto("https://example.com")
    assert page.title() == "Example Domain"
```

Run tests with markers:

```shell{ .show-prompt lineNos=false }
pytest -m smoke
pytest -m "not slow"
```

## Conftest.py

Share fixtures across tests:

```python
# conftest.py
import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="session")
def base_url():
    return "https://example.com"

@pytest.fixture
def authenticated_page(page: Page, base_url):
    page.goto(f"{base_url}/login")
    # Login logic
    return page
```

## Test Organization Structure

```
tests/
├── conftest.py
├── test_homepage.py
├── test_login.py
└── fixtures/
    └── auth.py
```

## Best Practices

1. **Use fixtures**: For setup and teardown
2. **Organize by feature**: Group related tests
3. **Use markers**: Categorize tests
4. **Share fixtures**: Use conftest.py
5. **Parametrize**: When testing multiple scenarios

## Next Steps

Now that you understand test organization, learn about:
- Page Object Model
- Parallel execution
- Configuration

