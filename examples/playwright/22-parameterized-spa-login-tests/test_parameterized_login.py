"""
Parameterized SPA Login Tests

This example demonstrates how to use pytest parameterization to test
different user roles in a Single Page Application (SPA) login flow.
"""

import pytest
from playwright.sync_api import Page, expect
from pathlib import Path


def get_file_url(filename="index.html"):
    """Helper function to get file URL."""
    html_file = Path(__file__).parent / filename
    return f"file://{html_file.absolute()}"


# Define test data as a list of tuples
# Each tuple contains: (username, password, expected_role, expected_features_count)
LOGIN_CREDENTIALS = [
    ("admin", "admin123", "admin", 6),
    ("moderator", "mod123", "moderator", 4),
    ("user", "user123", "user", 4),
    ("guest", "guest123", "guest", 2),
]


@pytest.mark.parametrize("username,password,expected_role,expected_features_count", LOGIN_CREDENTIALS)
def test_login_with_different_roles(
    page: Page,
    username: str,
    password: str,
    expected_role: str,
    expected_features_count: int
):
    """
    Parameterized test that verifies login functionality for different user roles.
    
    This test:
    1. Navigates to the login page
    2. Logs in with different credentials
    3. Verifies the user role is displayed correctly
    4. Verifies the correct features are shown based on role
    """
    # Navigate to the SPA login page
    page.goto(get_file_url())
    
    # Wait for the page to load (SPA)
    page.wait_for_load_state("networkidle")
    
    # Verify login form is visible
    login_form = page.locator("#loginForm")
    expect(login_form).to_be_visible()
    
    # Fill in login credentials
    page.fill("#username", username)
    page.fill("#password", password)
    
    # Click login button
    page.click("button:has-text('Login')")
    
    # Wait for dashboard to appear (SPA navigation - no page reload)
    dashboard = page.locator("#dashboard")
    expect(dashboard).to_be_visible(timeout=5000)
    
    # Verify login form is hidden
    expect(login_form).not_to_be_visible()
    
    # Verify user name is displayed
    user_name = page.locator("#userName")
    expect(user_name).to_have_text(username)
    
    # Verify role badge is visible and has correct text
    role_badge = page.locator("#roleBadge")
    expect(role_badge).to_be_visible()
    expect(role_badge).to_have_text(expected_role.upper())
    
    # Verify role badge has correct CSS class
    expect(role_badge).to_have_class(f"role-badge role-{expected_role}")
    
    # Verify correct number of features are displayed
    features = page.locator("#featureList li")
    expect(features).to_have_count(expected_features_count)
    
    print(f"✓ Login test passed for {username} with role {expected_role}")


@pytest.mark.parametrize("username,password,expected_role,expected_features_count", LOGIN_CREDENTIALS)
def test_role_specific_features(
    page: Page,
    username: str,
    password: str,
    expected_role: str,
    expected_features_count: int
):
    """
    Parameterized test that verifies role-specific features are displayed correctly.
    """
    page.goto(get_file_url())
    page.wait_for_load_state("networkidle")
    
    # Login
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button:has-text('Login')")
    
    # Wait for dashboard
    page.wait_for_selector("#dashboard", state="visible")
    
    # Verify role-specific features based on role
    features = page.locator("#featureList li")
    
    if expected_role == "admin":
        # Admin should have all features including "System Settings"
        expect(features.filter(has_text="System Settings")).to_be_visible()
        expect(features.filter(has_text="Manage Users")).to_be_visible()
        expect(features.filter(has_text="Delete Content")).to_be_visible()
    elif expected_role == "moderator":
        # Moderator should have moderation features but not system settings
        expect(features.filter(has_text="Moderate Comments")).to_be_visible()
        expect(features.filter(has_text="System Settings")).not_to_be_visible()
    elif expected_role == "user":
        # User should have basic features
        expect(features.filter(has_text="Create Posts")).to_be_visible()
        expect(features.filter(has_text="System Settings")).not_to_be_visible()
    elif expected_role == "guest":
        # Guest should have minimal features
        expect(features.filter(has_text="Browse Content")).to_be_visible()
        expect(features.filter(has_text="System Settings")).not_to_be_visible()
    
    print(f"✓ Role-specific features verified for {expected_role}")


@pytest.mark.parametrize("username,password,expected_role,_", LOGIN_CREDENTIALS)
def test_logout_functionality(
    page: Page,
    username: str,
    password: str,
    expected_role: str,
    _: int  # Unused parameter
):
    """
    Parameterized test that verifies logout functionality works for all roles.
    """
    page.goto(get_file_url())
    page.wait_for_load_state("networkidle")
    
    # Login
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button:has-text('Login')")
    
    # Wait for dashboard
    page.wait_for_selector("#dashboard", state="visible")
    
    # Verify dashboard is visible
    expect(page.locator("#dashboard")).to_be_visible()
    
    # Click logout
    page.click("button:has-text('Logout')")
    
    # Verify login form is visible again (SPA navigation)
    expect(page.locator("#loginForm")).to_be_visible()
    
    # Verify dashboard is hidden
    expect(page.locator("#dashboard")).not_to_be_visible()
    
    # Verify form fields are cleared
    expect(page.locator("#username")).to_have_value("")
    expect(page.locator("#password")).to_have_value("")
    
    print(f"✓ Logout test passed for {username}")


def test_invalid_credentials(page: Page):
    """Test that invalid credentials show an error message."""
    page.goto(get_file_url())
    page.wait_for_load_state("networkidle")
    
    # Try to login with invalid credentials
    page.fill("#username", "invalid_user")
    page.fill("#password", "wrong_password")
    page.click("button:has-text('Login')")
    
    # Verify error message is shown
    error_message = page.locator("#errorMessage")
    expect(error_message).to_be_visible()
    expect(error_message).to_have_text("Invalid username or password")
    
    # Verify login form is still visible
    expect(page.locator("#loginForm")).to_be_visible()
    
    # Verify dashboard is not shown
    expect(page.locator("#dashboard")).not_to_be_visible()
    
    print("✓ Invalid credentials test passed")


def test_empty_credentials(page: Page):
    """Test that empty credentials show an error message."""
    page.goto(get_file_url())
    page.wait_for_load_state("networkidle")
    
    # Try to login with empty credentials
    page.click("button:has-text('Login')")
    
    # Verify error message is shown
    error_message = page.locator("#errorMessage")
    expect(error_message).to_be_visible()
    expect(error_message).to_have_text("Please enter both username and password")
    
    print("✓ Empty credentials test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

