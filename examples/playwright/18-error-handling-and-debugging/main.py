from playwright.sync_api import sync_playwright, TimeoutError
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_console_logging():
    """Demonstrate console logging."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Log console messages
        page.on("console", lambda msg: print(f"Console: {msg.text}"))
        
        page.goto(get_file_url())
        print("✓ Console logging enabled")
        
        # Click button that logs to console
        page.click("button:has-text('Log to Console')")
        page.wait_for_timeout(500)
        
        browser.close()

def test_error_handling():
    """Demonstrate error handling."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
            page = browser.new_page()
            page.goto(get_file_url())
            
            # This might fail
            try:
                page.click(".non-existent", timeout=2000)
            except TimeoutError:
                print("✓ Handled timeout error gracefully")
            
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

def test_trace_recording():
    """Demonstrate trace recording."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        context = browser.new_context()
        
        # Start tracing
        context.tracing.start(screenshots=True, snapshots=True)
        
        page = context.new_page()
        page.goto(get_file_url())
        
        # Stop tracing
        context.tracing.stop(path="trace.zip")
        print("✓ Trace recorded to trace.zip")
        
        browser.close()

if __name__ == "__main__":
    print("Testing console logging...")
    test_console_logging()
    print("\nTesting error handling...")
    test_error_handling()
    print("\nTesting trace recording...")
    test_trace_recording()
    print("\nAll tests completed!")

