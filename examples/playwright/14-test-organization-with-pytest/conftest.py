import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="session")
def base_url():
    """Base URL fixture."""
    return "https://example.com"

@pytest.fixture
def test_page(page: Page, base_url):
    """Page fixture with base URL."""
    page.goto(base_url)
    return page

