# Network Interception

Network interception allows you to mock API responses, block resources, and monitor network activity. This tutorial covers how to intercept and modify network requests in Playwright.

## Overview

Playwright can:
- Mock API responses
- Block network requests
- Monitor network activity
- Modify requests and responses
- Handle authentication

## Route Interception

### Basic Route Handling

```python
from playwright.sync_api import sync_playwright

def test_route_interception():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Intercept and mock a route
        def handle_route(route):
            if "api/data" in route.request.url:
                route.fulfill(
                    status=200,
                    body='{"message": "Mocked response"}',
                    headers={"Content-Type": "application/json"}
                )
            else:
                route.continue_()
        
        page.route("**/api/**", handle_route)
        page.goto("https://example.com")
        
        browser.close()

if __name__ == "__main__":
    test_route_interception()
```

### Mocking API Responses

```python
from playwright.sync_api import sync_playwright
import json

def test_mock_api():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Mock API response
        page.route("**/api/users", lambda route: route.fulfill(
            status=200,
            body=json.dumps([{"id": 1, "name": "John"}]),
            headers={"Content-Type": "application/json"}
        ))
        
        page.goto("https://example.com")
        
        browser.close()

if __name__ == "__main__":
    test_mock_api()
```

## Blocking Resources

Block specific resources to speed up tests:

```python
from playwright.sync_api import sync_playwright

def test_block_resources():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Block images and stylesheets
        page.route("**/*.{png,jpg,jpeg,gif,svg,css}", lambda route: route.abort())
        
        page.goto("https://example.com")
        
        browser.close()

if __name__ == "__main__":
    test_block_resources()
```

## Monitoring Network Activity

Monitor network requests and responses:

```python
from playwright.sync_api import sync_playwright

def test_monitor_network():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        requests = []
        responses = []
        
        def handle_request(request):
            requests.append(request.url)
            print(f"Request: {request.url}")
        
        def handle_response(response):
            responses.append(response.url)
            print(f"Response: {response.url} - {response.status}")
        
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        page.goto("https://example.com")
        
        print(f"Total requests: {len(requests)}")
        print(f"Total responses: {len(responses)}")
        
        browser.close()

if __name__ == "__main__":
    test_monitor_network()
```

## Modifying Requests

Modify request headers or body:

```python
from playwright.sync_api import sync_playwright

def test_modify_request():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        def handle_route(route):
            # Modify headers
            headers = route.request.headers.copy()
            headers["Authorization"] = "Bearer token123"
            
            route.continue_(headers=headers)
        
        page.route("**/api/**", handle_route)
        page.goto("https://example.com")
        
        browser.close()

if __name__ == "__main__":
    test_modify_request()
```

## Waiting for Network Requests

Wait for specific network requests:

```python
from playwright.sync_api import sync_playwright

def test_wait_for_request():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Wait for API request
        with page.expect_request("**/api/data") as request_info:
            page.goto("https://example.com")
        
        request = request_info.value
        print(f"Request URL: {request.url}")
        
        # Wait for response
        with page.expect_response("**/api/data") as response_info:
            page.goto("https://example.com")
        
        response = response_info.value
        print(f"Response status: {response.status}")
        
        browser.close()

if __name__ == "__main__":
    test_wait_for_request()
```

## Best Practices

1. **Mock external APIs**: Avoid dependencies on external services
2. **Block unnecessary resources**: Speed up tests
3. **Monitor network**: Debug network issues
4. **Use route patterns**: Match URLs with glob patterns
5. **Clean up routes**: Unroute when done

## Common Patterns

```python
# Pattern 1: Mock API response
page.route("**/api/**", lambda route: route.fulfill(
    status=200,
    body='{"data": "mocked"}'
))

# Pattern 2: Block resources
page.route("**/*.{png,jpg,css}", lambda route: route.abort())

# Pattern 3: Monitor requests
page.on("request", lambda req: print(req.url))

# Pattern 4: Wait for request
with page.expect_request("**/api/**"):
    page.click("button")
```

## Next Steps

Now that you understand network interception, learn about:
- File downloads
- Test organization
- Page Object Model

