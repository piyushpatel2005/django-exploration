# Best Practices

This tutorial covers best practices for writing maintainable and reliable Playwright tests.

## Overview

Best practices include:
- Writing maintainable tests
- Managing test data
- Avoiding flaky tests
- Performance optimization
- Code organization

## Writing Maintainable Tests

### Use Descriptive Names

```python
def test_user_can_login_with_valid_credentials():
    # Test implementation
    pass

def test_user_cannot_login_with_invalid_password():
    # Test implementation
    pass
```

### Keep Tests Focused

```python
# Good: One assertion per test
def test_title_is_correct():
    page.goto("https://example.com")
    assert page.title() == "Example Domain"

# Bad: Multiple unrelated assertions
def test_everything():
    # Too many things
    pass
```

## Test Data Management

### Use Fixtures

```python
@pytest.fixture
def test_user():
    return {"username": "testuser", "password": "testpass"}

def test_login(test_user):
    # Use test_user fixture
    pass
```

### Externalize Test Data

```python
# test_data.json
{
    "users": {
        "admin": {"username": "admin", "password": "admin123"},
        "user": {"username": "user", "password": "user123"}
    }
}
```

## Avoiding Flaky Tests

### Use Explicit Waits

```python
# Good: Explicit wait
page.wait_for_selector(".element", state="visible")
page.click(".element")

# Bad: Fixed timeout
page.wait_for_timeout(5000)
page.click(".element")
```

### Avoid Hard-Coded Waits

```python
# Good: Conditional wait
page.wait_for_load_state("networkidle")

# Bad: Fixed wait
page.wait_for_timeout(5000)
```

## Performance Optimization

### Run Tests in Parallel

```shell{ .show-prompt lineNos=false }
pytest -n auto
```

### Block Unnecessary Resources

```python
page.route("**/*.{png,jpg,css}", lambda route: route.abort())
```

## Code Organization

### Use Page Object Model

```python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.submit_button = page.locator("button[type='submit']")
    
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()
```

### Organize by Feature

```
tests/
├── login/
│   ├── test_login.py
│   └── test_logout.py
├── dashboard/
│   └── test_dashboard.py
└── conftest.py
```

## Best Practices Summary

1. **Descriptive names**: Clear test names
2. **Focused tests**: One thing per test
3. **Use fixtures**: For test data
4. **Explicit waits**: Avoid flaky tests
5. **Page Objects**: Organize code
6. **Parallel execution**: Speed up tests
7. **Refactor**: Keep code DRY

## Common Mistakes to Avoid

1. **Hard-coded waits**: Use conditional waits
2. **Brittle selectors**: Use stable locators
3. **Large test files**: Split into smaller files
4. **Test dependencies**: Keep tests independent
5. **No cleanup**: Clean up after tests

## Next Steps

You now have a comprehensive understanding of Playwright! Continue practicing and applying these best practices to your test suites.

