from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_multiple_pages():
    """Demonstrate creating multiple pages in a single context."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        context = browser.new_context()
        
        # Create multiple pages
        page1 = context.new_page()
        page2 = context.new_page()
        
        # Navigate each page independently
        page1.goto(get_file_url("page1.html"))
        page2.goto(get_file_url("page2.html"))
        
        print(f"Page 1 title: {page1.title()}")
        print(f"Page 2 title: {page2.title()}")
        
        browser.close()

def test_multiple_contexts():
    """Demonstrate creating multiple isolated contexts."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        
        # Create two separate contexts
        context1 = browser.new_context()
        context2 = browser.new_context()
        
        # Pages in different contexts are isolated
        page1 = context1.new_page()
        page2 = context2.new_page()
        
        page1.goto(get_file_url("page1.html"))
        page2.goto(get_file_url("page2.html"))
        
        print(f"Context 1 - Page title: {page1.title()}")
        print(f"Context 2 - Page title: {page2.title()}")
        
        browser.close()

def test_context_options():
    """Demonstrate configuring context with options."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        
        # Create context with custom options
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            locale='en-US',
            timezone_id='America/New_York'
        )
        
        page = context.new_page()
        page.goto(get_file_url("page1.html"))
        
        # Display configured viewport (context.viewport_size may not be available in all versions)
        print(f"Viewport configured: 1920x1080")
        print(f"Page title: {page.title()}")
        
        browser.close()

def test_page_events():
    """Demonstrate listening to page events."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Listen to console messages
        console_messages = []
        def handle_console(msg):
            console_messages.append(msg.text)
            print(f"Console: {msg.text}")
        
        page.on("console", handle_console)
        
        # Navigate to a page that might log to console
        page.goto(get_file_url("page1.html"))
        
        print(f"Captured {len(console_messages)} console messages")
        
        browser.close()

if __name__ == "__main__":
    print("Testing multiple pages...")
    test_multiple_pages()
    print("\nTesting multiple contexts...")
    test_multiple_contexts()
    print("\nTesting context options...")
    test_context_options()
    print("\nTesting page events...")
    test_page_events()
    print("\nAll tests completed!")

