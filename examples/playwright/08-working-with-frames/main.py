from playwright.sync_api import sync_playwright
from pathlib import Path

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_find_frames():
    """Demonstrate finding frames on a page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Get all frames
        frames = page.frames
        print(f"✓ Total frames: {len(frames)}")
        
        # Access main frame
        main_frame = page.main_frame
        print(f"✓ Main frame URL: {main_frame.url[:50]}...")
        
        browser.close()

def test_frame_interaction():
    """Demonstrate interacting with frame content."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        # Wait for page to load frames
        page.wait_for_load_state("load")
        
        # Use frame_locator to access frame content
        # frame_locator returns a FrameLocator that can locate elements inside the frame
        frame_locator = page.frame_locator("iframe").first
        
        # Interact with elements inside frame using frame_locator
        heading = frame_locator.locator("h1")
        if heading.count() > 0:
            print(f"✓ Frame heading: {heading.first.text_content()}")
        
        button = frame_locator.locator("button")
        if button.count() > 0:
            print(f"✓ Found button in frame")
        
        browser.close()

def test_frame_info():
    """Demonstrate getting frame information."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        page.goto(get_file_url())
        
        frames = page.frames
        
        for i, frame in enumerate(frames):
            print(f"✓ Frame {i}:")
            print(f"  Name: {frame.name or 'N/A'}")
            print(f"  URL: {frame.url[:50]}...")
        
        browser.close()

if __name__ == "__main__":
    print("Testing frame finding...")
    test_find_frames()
    print("\nTesting frame interaction...")
    test_frame_interaction()
    print("\nTesting frame information...")
    test_frame_info()
    print("\nAll tests completed!")

