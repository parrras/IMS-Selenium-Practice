import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Stock_Issue_Return import StockIssueReturnPage


@allure.title("Generate Stock Issue Return Entry in IMS Application")
@allure.description("Logs in, navigates to Stock Issue Return page, selects warehouses, selects reference IS number, and saves the entry.")
def test_stock_issue_return_entry(setup):
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

        # --- Step 2: Navigate to Stock Issue Return page ---
        stock_issue_return = StockIssueReturnPage(driver)
        stock_issue_return.generate_stock_issue_return()

        print("✅ Stock Issue Return entry created successfully.")

        # Screenshot on success
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Stock_Issue_Return_Success",
            attachment_type=allure.attachment_type.PNG
        )

    except Exception as e:
        # Screenshot on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Stock_Issue_Return_Error",
            attachment_type=allure.attachment_type.PNG
        )

        # Log the error text also
        allure.attach(
            str(e),
            name="Error Details",
            attachment_type=allure.attachment_type.TEXT
        )

        pytest.fail(f"❌ Test failed due to: {e}")
