import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Opening_Stock import OpeningStockPage


# noinspection PyBroadException
@allure.title("Generate Opening Stock Entry in IMS Application")
@allure.description("Logs in, navigates to Opening Stock page, adds items with quantity, and saves the entry.")
def test_opening_stock_entry(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # Handle previous session logout popup (if exists)
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        # --- Step 2: Navigate to Opening Stock page ---
        opening_stock = OpeningStockPage(driver)
        opening_stock.generate_opening_stock()

        print("✅ Opening Stock entry created successfully.")

        # Screenshot on success
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Opening_Stock_Success",
            attachment_type=allure.attachment_type.PNG
        )

    except Exception as e:
        # Screenshot on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Opening_Stock_Error",
            attachment_type=allure.attachment_type.PNG
        )

        # Log the error text also
        allure.attach(
            str(e),
            name="Error Details",
            attachment_type=allure.attachment_type.TEXT
        )

        pytest.fail(f"❌ Test failed due to: {e}")
