import pytest
from playwright.sync_api import Page
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

@pytest.mark.parametrize("test_name", [
    "test1",
    "test2",
])
def test_parallel_example(page: Page, test_name):
    """Example test that can run in parallel."""
    page.goto(get_file_url())
    assert page.title() is not None
    print(f"✓ Test completed: {test_name}")

