from playwright.sync_api import sync_playwright
from pathlib import Path
import json

def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"

def test_route_interception():
    """Demonstrate route interception."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Intercept and mock a route
        intercepted = False
        
        def handle_route(route):
            nonlocal intercepted
            if "index.html" in route.request.url or "api" in route.request.url.lower():
                intercepted = True
                print(f"✓ Intercepted: {route.request.url}")
            route.continue_()
        
        page.route("**/*", handle_route)
        page.goto(get_file_url())
        
        if intercepted:
            print("✓ Route interception working")
        
        browser.close()

def test_mock_api():
    """Demonstrate mocking API responses."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        # Mock API response
        mocked = False
        
        def handle_route(route):
            nonlocal mocked
            if "api" in route.request.url.lower():
                mocked = True
                route.fulfill(
                    status=200,
                    body=json.dumps({"message": "Mocked response"}),
                    headers={"Content-Type": "application/json"}
                )
            else:
                route.continue_()
        
        page.route("**/api/**", handle_route)
        page.goto(get_file_url())
        
        if mocked:
            print("✓ API mocking working")
        
        browser.close()

def test_monitor_network():
    """Demonstrate monitoring network activity."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        requests = []
        responses = []
        
        def handle_request(request):
            requests.append(request.url)
        
        def handle_response(response):
            responses.append(response.url)
        
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        page.goto(get_file_url())
        
        print(f"✓ Monitored {len(requests)} requests")
        print(f"✓ Monitored {len(responses)} responses")
        
        browser.close()

def test_block_resources():
    """Demonstrate blocking resources."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False to see browser window
        page = browser.new_page()
        
        blocked_count = 0
        
        def handle_route(route):
            nonlocal blocked_count
            if route.request.resource_type in ["image", "stylesheet"]:
                blocked_count += 1
                route.abort()
            else:
                route.continue_()
        
        page.route("**/*", handle_route)
        page.goto(get_file_url())
        
        print(f"✓ Blocked {blocked_count} resources")
        
        browser.close()

if __name__ == "__main__":
    print("Testing route interception...")
    test_route_interception()
    print("\nTesting API mocking...")
    test_mock_api()
    print("\nTesting network monitoring...")
    test_monitor_network()
    print("\nTesting resource blocking...")
    test_block_resources()
    print("\nAll tests completed!")

