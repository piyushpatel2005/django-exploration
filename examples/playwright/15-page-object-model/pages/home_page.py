from playwright.sync_api import Page
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent.parent / filename
    return f"file://{html_file.absolute()}"

class HomePage:
    """Page Object for Home Page."""
    
    def __init__(self, page: Page):
        self.page = page
        self.url = get_file_url()
        self.heading = page.locator("h1")
        self.paragraphs = page.locator("p")
    
    def goto(self):
        """Navigate to home page."""
        self.page.goto(self.url)
    
    def get_heading_text(self):
        """Get heading text."""
        return self.heading.text_content()
    
    def get_paragraph_count(self):
        """Get number of paragraphs."""
        return self.paragraphs.count()

