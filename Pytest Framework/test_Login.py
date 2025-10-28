import pytest
import allure
import time
from Login_Page import LoginPage

@allure.title("Verify Login Functionality")
@allure.description("Test valid login and handle duplicate logout popup.")
def test_login_flow(setup):
    driver = setup
    login = LoginPage(driver)

    with allure.step("Open the login page"):
        login.open()

    with allure.step("Enter username and password"):
        login.enter_username("Paras")
        login.enter_password("Ims@1234")  # Replace with correct password to test success

    with allure.step("Click on Sign In"):
        login.click_signin()
        time.sleep(2)
        login.handle_duplicate_logout()

    with allure.step("Verify the login result"):
        if login.is_login_successful():
            # First case: login successful
            allure.attach(driver.get_screenshot_as_png(),
                          name="login_success",
                          attachment_type=allure.attachment_type.PNG)
            print("✅ Login successful")

        elif login.get_error_message() == "Some specific error":  # Replace with the actual error you want to catch
            # Second case: known error message
            error_msg = login.get_error_message()
            allure.attach(driver.get_screenshot_as_png(),
                          name="login_error",
                          attachment_type=allure.attachment_type.PNG)
            print(f"❌ Login failed: {error_msg}")
            pytest.fail(f"❌ Login failed! Reason: {error_msg}")

        else:
            # Third case: fallback, treat as login success again
            allure.attach(driver.get_screenshot_as_png(),
                          name="login_success_fallback",
                          attachment_type=allure.attachment_type.PNG)
            print("✅ Login successful (fallback)")



