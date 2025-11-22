# Playwright Examples

This directory contains executable examples for learning Playwright with Python.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

## Running Examples

### Option 1: Run Individual Examples

Each subdirectory contains a `main.py` file that can be run directly:

```bash
# Run a specific example
python 01-first-playwright-test/main.py

# Or navigate to the directory first
cd 01-first-playwright-test
python main.py
```

### Option 2: Run All Examples

Use the provided script to run all examples:

```bash
python run_all_tests.py
```

This will:
- Run all `main.py` files in subdirectories
- Run all pytest test files
- Provide a summary of results

### Option 3: Run with Pytest

For directories that contain pytest test files:

```bash
# Run all pytest tests
pytest

# Run tests in a specific directory
pytest 14-test-organization-with-pytest/

# Run with verbose output
pytest -v

# Run in parallel (if pytest-xdist is installed)
pytest -n auto
```

### Option 4: Run All Main Files with Shell Script

On Unix-like systems (Linux/Mac), you can use:

```bash
# Make the script executable
chmod +x run_all_tests.sh

# Run it
./run_all_tests.sh
```

Or manually:

```bash
for dir in */; do
    if [ -f "$dir/main.py" ]; then
        echo "Running $dir..."
        (cd "$dir" && python main.py)
    fi
done
```

## Directory Structure

- `00-installation-and-setup/` - Verify Playwright installation
- `01-first-playwright-test/` - Basic test structure
- `02-browser-context-and-pages/` - Browser contexts and pages
- `03-locating-elements/` - Element locators
- `04-interacting-with-elements/` - User interactions
- `05-waiting-strategies/` - Wait strategies
- `06-assertions-and-expectations/` - Assertions
- `07-handling-alerts-and-dialogs/` - Dialog handling
- `08-working-with-frames/` - Frame/iframe handling
- `09-navigation-and-urls/` - Navigation
- `10-cookies-and-storage/` - Storage management
- `11-screenshots-and-videos/` - Screenshots and videos
- `12-network-interception/` - Network mocking
- `13-file-downloads/` - File downloads
- `14-test-organization-with-pytest/` - Pytest organization
- `15-page-object-model/` - Page Object Model pattern
- `16-parallel-execution/` - Parallel test execution
- `17-configuration-and-options/` - Configuration
- `18-error-handling-and-debugging/` - Debugging
- `19-cicd-integration/` - CI/CD integration
- `20-advanced-scenarios/` - Advanced scenarios
- `21-best-practices/` - Best practices

## Notes

- All examples use local HTML files (no internet connection required)
- Examples are designed to be run individually for learning purposes
- Examples run in headless mode by default (headless=True) for stability
- You can change `headless=True` to `headless=False` in any example to see the browser window
- Screenshots and other generated files will be created in the respective directories

