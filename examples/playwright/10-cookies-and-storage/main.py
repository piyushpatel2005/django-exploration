from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_cookies():
    """Demonstrate working with cookies."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        context = browser.new_context()
        
        # Set cookies before navigation (using localhost for file:// URLs)
        context.add_cookies([
            {
                "name": "test_cookie",
                "value": "test_value",
                "domain": "localhost",
                "path": "/"
            }
        ])
        
        page = context.new_page()
        page.goto(get_file_url())
        
        # Get cookies
        cookies = context.cookies()
        print(f"✓ Cookies: {len(cookies)} cookie(s) found")
        
        browser.close()

def test_local_storage():
    """Demonstrate working with local storage."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Set local storage before navigation
        page.add_init_script("""
            localStorage.setItem('user', 'John Doe');
            localStorage.setItem('theme', 'dark');
        """)
        
        page.goto(get_file_url())
        
        # Get local storage
        storage = page.evaluate("() => ({ ...localStorage })")
        print(f"✓ Local storage items: {len(storage)}")
        
        # Get specific item
        user = page.evaluate("() => localStorage.getItem('user')")
        print(f"✓ User from storage: {user}")
        
        browser.close()

def test_session_storage():
    """Demonstrate working with session storage."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Set session storage
        page.add_init_script("""
            sessionStorage.setItem('session', 'active');
        """)
        
        page.goto(get_file_url())
        
        # Get session storage
        session = page.evaluate("() => sessionStorage.getItem('session')")
        print(f"✓ Session: {session}")
        
        browser.close()

def test_clear_storage():
    """Demonstrate clearing storage."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        context = browser.new_context()
        page = context.new_page()
        
        # Set some cookies
        context.add_cookies([
            {"name": "cookie1", "value": "value1", "domain": "localhost", "path": "/"}
        ])
        
        page.goto(get_file_url())
        
        # Clear cookies
        context.clear_cookies()
        cookies = context.cookies()
        print(f"✓ Cookies after clear: {len(cookies)}")
        
        browser.close()

if __name__ == "__main__":
    print("Testing cookies...")
    test_cookies()
    print("\nTesting local storage...")
    test_local_storage()
    print("\nTesting session storage...")
    test_session_storage()
    print("\nTesting clear storage...")
    test_clear_storage()
    print("\nAll tests completed!")

