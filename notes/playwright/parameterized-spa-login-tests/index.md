# Parameterized SPA Login Tests with Pytest

Testing Single Page Applications (SPAs) with parameterized tests allows you to verify different user roles and permissions efficiently. This tutorial covers how to use pytest's parameterization feature to test login functionality with multiple user credentials and verify role-based UI visibility.

## Overview

Parameterized tests enable you to:
- Run the same test logic with different input data
- Test multiple user roles efficiently
- Reduce code duplication
- Easily add new test cases

## What is Parameterization?

Parameterization is a pytest feature that allows you to run the same test function multiple times with different input values. This is particularly useful for testing scenarios where the logic is the same but the inputs vary.

## Setting Up Parameterized Tests

### Basic Parameterization Syntax

```python
import pytest
from playwright.sync_api import Page

@pytest.mark.parametrize("username,password", [
    ("admin", "admin123"),
    ("user", "user123"),
    ("guest", "guest123"),
])
def test_login(page: Page, username: str, password: str):
    page.goto("https://example.com/login")
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button[type='submit']")
    # Assertions...
```

## SPA Login Testing with Parameterization

### Understanding SPAs

Single Page Applications (SPAs) don't reload the entire page when navigating. Instead, they:
- Update the DOM dynamically
- Use JavaScript to show/hide elements
- Maintain state in memory or sessionStorage
- Require waiting for dynamic content

### Test Data Structure

Define your test data as a list of tuples:

```python
LOGIN_CREDENTIALS = [
    ("admin", "admin123", "admin", 6),      # username, password, role, feature_count
    ("moderator", "mod123", "moderator", 4),
    ("user", "user123", "user", 4),
    ("guest", "guest123", "guest", 2),
]
```

### Complete Example: Parameterized Login Test

```python
import pytest
from playwright.sync_api import Page, expect
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

LOGIN_CREDENTIALS = [
    ("admin", "admin123", "admin", 6),
    ("moderator", "mod123", "moderator", 4),
    ("user", "user123", "user", 4),
    ("guest", "guest123", "guest", 2),
]

@pytest.mark.parametrize("username,password,expected_role,expected_features_count", LOGIN_CREDENTIALS)
def test_login_with_different_roles(
    page: Page,
    username: str,
    password: str,
    expected_role: str,
    expected_features_count: int
):
    """Test login for different user roles."""
    # Navigate to SPA
    page.goto(get_file_url())
    page.wait_for_load_state("networkidle")
    
    # Verify login form is visible
    login_form = page.locator("#loginForm")
    expect(login_form).to_be_visible()
    
    # Fill credentials
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button:has-text('Login')")
    
    # Wait for dashboard (SPA navigation - no reload)
    dashboard = page.locator("#dashboard")
    expect(dashboard).to_be_visible(timeout=5000)
    
    # Verify login form is hidden
    expect(login_form).not_to_be_visible()
    
    # Verify user name
    expect(page.locator("#userName")).to_have_text(username)
    
    # Verify role badge
    role_badge = page.locator("#roleBadge")
    expect(role_badge).to_have_text(expected_role.upper())
    expect(role_badge).to_have_class(f"role-badge role-{expected_role}")
    
    # Verify feature count
    features = page.locator("#featureList li")
    expect(features).to_have_count(expected_features_count)
```

## Key Concepts

### 1. Waiting for SPA Navigation

SPAs don't reload pages, so you need to wait for dynamic content:

```python
# Wait for network to be idle
page.wait_for_load_state("networkidle")

# Wait for specific element to appear
page.wait_for_selector("#dashboard", state="visible")

# Or use expect with timeout
expect(page.locator("#dashboard")).to_be_visible(timeout=5000)
```

### 2. Verifying Element Visibility

After SPA navigation, verify elements are shown/hidden:

```python
# Verify element is visible
expect(page.locator("#dashboard")).to_be_visible()

# Verify element is hidden
expect(page.locator("#loginForm")).not_to_be_visible()
```

### 3. Role-Based Assertions

Test role-specific UI elements:

```python
@pytest.mark.parametrize("username,password,expected_role,_", LOGIN_CREDENTIALS)
def test_role_specific_features(page: Page, username, password, expected_role, _):
    # Login...
    
    features = page.locator("#featureList li")
    
    if expected_role == "admin":
        expect(features.filter(has_text="System Settings")).to_be_visible()
    elif expected_role == "moderator":
        expect(features.filter(has_text="System Settings")).not_to_be_visible()
```

### 4. Testing Logout (SPA State Reset)

Verify logout clears SPA state:

```python
@pytest.mark.parametrize("username,password,expected_role,_", LOGIN_CREDENTIALS)
def test_logout_functionality(page: Page, username, password, expected_role, _):
    # Login...
    
    # Click logout
    page.click("button:has-text('Logout')")
    
    # Verify login form is visible again
    expect(page.locator("#loginForm")).to_be_visible()
    
    # Verify dashboard is hidden
    expect(page.locator("#dashboard")).not_to_be_visible()
    
    # Verify form is cleared
    expect(page.locator("#username")).to_have_value("")
```

## Advanced Parameterization

### Using IDs for Test Identification

```python
@pytest.mark.parametrize("username,password,expected_role,expected_features_count", 
                         LOGIN_CREDENTIALS,
                         ids=["admin", "moderator", "user", "guest"])
def test_login(page: Page, username, password, expected_role, expected_features_count):
    # Test implementation...
```

### Combining Multiple Parameters

```python
@pytest.mark.parametrize("username,password", [
    ("admin", "admin123"),
    ("user", "user123"),
])
@pytest.mark.parametrize("browser_type", ["chromium", "firefox"])
def test_cross_browser_login(page: Page, username, password, browser_type):
    # Test runs for each combination
    pass
```

### Using Fixtures with Parameters

```python
@pytest.fixture
def login_credentials():
    return [
        ("admin", "admin123", "admin"),
        ("user", "user123", "user"),
    ]

@pytest.mark.parametrize("username,password,role", 
                         indirect=True,
                         argvalues=login_credentials())
def test_with_fixture(page: Page, username, password, role):
    # Test implementation...
```

## Best Practices

### 1. Organize Test Data

Keep test data separate and well-documented:

```python
# test_data.py
ADMIN_CREDENTIALS = ("admin", "admin123", "admin", 6)
MODERATOR_CREDENTIALS = ("moderator", "mod123", "moderator", 4)
USER_CREDENTIALS = ("user", "user123", "user", 4)
GUEST_CREDENTIALS = ("guest", "guest123", "guest", 2)

LOGIN_CREDENTIALS = [
    ADMIN_CREDENTIALS,
    MODERATOR_CREDENTIALS,
    USER_CREDENTIALS,
    GUEST_CREDENTIALS,
]
```

### 2. Use Descriptive Test Names

```python
@pytest.mark.parametrize("username,password,expected_role,expected_features_count",
                         LOGIN_CREDENTIALS,
                         ids=lambda x: f"role_{x[2]}")  # Use role as test ID
def test_login_with_different_roles(...):
    """Test login for different user roles."""
    pass
```

### 3. Handle SPA State Properly

```python
def test_with_state_management(page: Page):
    # Clear any existing state
    page.evaluate("sessionStorage.clear()")
    
    # Perform actions
    page.goto(get_file_url())
    # ... test logic ...
    
    # Verify state
    user = page.evaluate("JSON.parse(sessionStorage.getItem('currentUser'))")
    assert user['role'] == 'admin'
```

### 4. Test Error Cases

Don't forget to test invalid scenarios:

```python
def test_invalid_credentials(page: Page):
    page.goto(get_file_url())
    page.fill("#username", "invalid")
    page.fill("#password", "wrong")
    page.click("button:has-text('Login')")
    
    # Verify error message
    expect(page.locator("#errorMessage")).to_be_visible()
    expect(page.locator("#errorMessage")).to_have_text("Invalid username or password")
```

## Running Parameterized Tests

### Run All Parameterized Tests

```shell{ .show-prompt lineNos=false }
pytest test_parameterized_login.py -v
```

### Run Specific Parameter

```shell{ .show-prompt lineNos=false }
pytest test_parameterized_login.py::test_login_with_different_roles[admin] -v
```

### Run with Specific Markers

```shell{ .show-prompt lineNos=false }
pytest -m "parametrize" -v
```

## Common Patterns

### Pattern 1: Testing Multiple Roles

```python
@pytest.mark.parametrize("role,expected_permissions", [
    ("admin", ["read", "write", "delete", "admin"]),
    ("user", ["read", "write"]),
    ("guest", ["read"]),
])
def test_role_permissions(page: Page, role, expected_permissions):
    # Test implementation...
```

### Pattern 2: Testing Different Environments

```python
@pytest.mark.parametrize("environment", ["dev", "staging", "prod"])
def test_across_environments(page: Page, environment):
    url = f"https://{environment}.example.com"
    page.goto(url)
    # Test implementation...
```

### Pattern 3: Testing with Different Data Sets

```python
@pytest.mark.parametrize("test_data", [
    {"username": "admin", "role": "admin"},
    {"username": "user", "role": "user"},
])
def test_with_dict_data(page: Page, test_data):
    username = test_data["username"]
    role = test_data["role"]
    # Test implementation...
```

## Debugging Parameterized Tests

### View Test IDs

```shell{ .show-prompt lineNos=false }
pytest test_parameterized_login.py --collect-only
```

### Run Failed Tests Only

```shell{ .show-prompt lineNos=false }
pytest test_parameterized_login.py --lf
```

### Show Print Statements

```python
def test_with_debugging(page: Page, username, password, expected_role, _):
    print(f"Testing login for {username} with role {expected_role}")
    # Test implementation...
    print(f"✓ Test completed for {username}")
```

## Troubleshooting

### Issue: Tests Running Too Fast

**Solution**: Add explicit waits for SPA navigation:

```python
# Wait for network idle
page.wait_for_load_state("networkidle")

# Wait for specific element
page.wait_for_selector("#dashboard", state="visible")
```

### Issue: State Persisting Between Tests

**Solution**: Clear state in setup or use fixtures:

```python
@pytest.fixture(autouse=True)
def clear_state(page: Page):
    page.evaluate("sessionStorage.clear()")
    yield
    page.evaluate("sessionStorage.clear()")
```

### Issue: Parameterized Test Failing for One Case

**Solution**: Use `--tb=short` to see which parameter failed:

```shell{ .show-prompt lineNos=false }
pytest test_parameterized_login.py --tb=short -v
```

## Example: Complete Test Suite

```python
import pytest
from playwright.sync_api import Page, expect
from pathlib import Path

def get_file_url(filename="index.html"):
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

LOGIN_CREDENTIALS = [
    ("admin", "admin123", "admin", 6),
    ("moderator", "mod123", "moderator", 4),
    ("user", "user123", "user", 4),
    ("guest", "guest123", "guest", 2),
]

@pytest.mark.parametrize("username,password,expected_role,expected_features_count",
                         LOGIN_CREDENTIALS)
def test_login_with_different_roles(page: Page, username, password, 
                                     expected_role, expected_features_count):
    """Test login for different user roles."""
    page.goto(get_file_url())
    page.wait_for_load_state("networkidle")
    
    # Login
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button:has-text('Login')")
    
    # Verify dashboard appears
    dashboard = page.locator("#dashboard")
    expect(dashboard).to_be_visible(timeout=5000)
    
    # Verify role
    role_badge = page.locator("#roleBadge")
    expect(role_badge).to_have_text(expected_role.upper())
    
    # Verify features
    features = page.locator("#featureList li")
    expect(features).to_have_count(expected_features_count)
```

## Summary

Parameterized tests with pytest allow you to:
- ✅ Test multiple user roles efficiently
- ✅ Reduce code duplication
- ✅ Easily add new test cases
- ✅ Verify role-based UI visibility in SPAs
- ✅ Test SPA navigation without page reloads

## Next Steps

Now that you understand parameterized SPA login tests, you can:
- Apply parameterization to other test scenarios
- Combine with Page Object Model pattern
- Use with parallel execution for faster test runs
- Integrate with CI/CD pipelines

