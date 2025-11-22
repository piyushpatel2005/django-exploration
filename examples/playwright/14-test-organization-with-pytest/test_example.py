import pytest
from playwright.sync_api import Page, expect
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_example(page: Page):
    """Basic pytest test with Playwright."""
    page.goto(get_file_url())
    expect(page).to_have_title("Test Organization with Pytest")
    print("✓ Test passed")

@pytest.mark.parametrize("expected_title", [
    "Test Organization with Pytest",
])
def test_parametrized(page: Page, expected_title):
    """Parametrized test example."""
    page.goto(get_file_url())
    assert expected_title in page.title()
    print(f"✓ Test passed for {expected_title}")

class TestHomePage:
    """Test class example."""
    
    def test_title(self, page: Page):
        """Test page title."""
        page.goto(get_file_url())
        expect(page).to_have_title("Test Organization with Pytest")
        print("✓ Title test passed")
    
    def test_heading(self, page: Page):
        """Test page heading."""
        page.goto(get_file_url())
        heading = page.locator("h1")
        expect(heading).to_be_visible()
        print("✓ Heading test passed")

