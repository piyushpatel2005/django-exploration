# CI/CD Integration

Integrating Playwright tests into CI/CD pipelines ensures tests run automatically. This tutorial covers CI/CD integration for Playwright.

## Overview

CI/CD integration involves:
- Running tests in CI environments
- Using headless mode
- Handling browser installation
- Reporting results
- Parallel execution

## GitHub Actions

Create `.github/workflows/playwright.yml`:

```yaml
name: Playwright Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps
      - name: Run tests
        run: pytest
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

## Headless Mode

Run tests headless in CI:

```python
browser = p.chromium.launch(headless=True)
```

## Browser Installation

Install browsers in CI:

```shell{ .show-prompt lineNos=false }
playwright install --with-deps
```

## Environment Variables

```python
import os

headless = os.getenv("CI") == "true"
browser = p.chromium.launch(headless=headless)
```

## Best Practices

1. **Use headless mode**: In CI environments
2. **Install dependencies**: Include browser installation
3. **Set timeouts**: Longer timeouts for CI
4. **Save artifacts**: Screenshots and reports
5. **Run in parallel**: Speed up execution

## Next Steps

Learn about:
- Advanced scenarios
- Best practices

