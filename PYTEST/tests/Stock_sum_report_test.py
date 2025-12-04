import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Stock_Sum_Report import StockSumReportPage


# noinspection PyBroadException
@allure.title("Generate Stock Summary Report in IMS Application")
@allure.description("Logs in, navigates to Stock Summary Report, selects supplier and warehouse, and runs the report.")
def test_stock_summary_report(setup):
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

        # --- Step 2: Navigate to Stock Summary Report ---
        stock_sum_report = StockSumReportPage(driver)
        stock_sum_report.generate_stock_sum_report()

        print("✅ Stock Summary Report generated successfully.")

        # Screenshot on success
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Stock_Summary_Report_Success",
            attachment_type=allure.attachment_type.PNG
        )

    except Exception as e:
        # Screenshot on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Stock_Summary_Report_Error",
            attachment_type=allure.attachment_type.PNG
        )

        # Attach error details as text
        allure.attach(
            str(e),
            name="Error Details",
            attachment_type=allure.attachment_type.TEXT
        )

        pytest.fail(f"❌ Test failed due to: {e}")
