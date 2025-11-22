# Parallel Execution

Running tests in parallel speeds up test execution significantly. This tutorial covers how to run Playwright tests in parallel with pytest.

## Overview

Parallel execution:
- Runs multiple tests simultaneously
- Reduces total test time
- Uses workers to manage concurrency
- Requires proper test isolation

## Running Tests in Parallel

```shell{ .show-prompt lineNos=false }
pytest --numprocesses=4
```

Or with pytest-xdist:

```shell{ .show-prompt lineNos=false }
pytest -n auto
```

## Configuring Workers

In `pytest.ini`:

```ini
[pytest]
addopts = -n auto
```

## Test Isolation

Ensure tests are isolated:

```python
import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="function")
def isolated_page(page: Page):
    """Create isolated page for each test."""
    page.goto("about:blank")
    yield page
    # Cleanup if needed
```

## Browser Context Isolation

Each test gets its own context:

```python
@pytest.fixture(scope="function")
def context(browser_context):
    """Isolated context per test."""
    context = browser_context.new_context()
    yield context
    context.close()
```

## Best Practices

1. **Isolate tests**: Each test should be independent
2. **Use fixtures**: For setup/teardown
3. **Avoid shared state**: Don't depend on other tests
4. **Monitor resources**: Watch CPU/memory usage
5. **Adjust workers**: Based on system capabilities

## Next Steps

Learn about:
- Configuration options
- Error handling
- CI/CD integration

