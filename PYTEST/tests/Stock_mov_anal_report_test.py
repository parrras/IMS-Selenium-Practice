import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Stock_Movement_Analysis_Report import StockMovementAnalysisReportPage


# noinspection PyBroadException
@allure.title("Generate Stock Movement Analysis Report in IMS Application")
@allure.description("Logs in, navigates to Stock Movement Analysis Report, selects supplier, and runs the report.")
def test_stock_movement_analysis_report(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # Handle previous active session popup
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        # --- Step 2: Generate Stock Movement Analysis Report ---
        stock_mv_report = StockMovementAnalysisReportPage(driver)
        stock_mv_report.generate_stock_movement_analysis_report()

        print("✅ Stock Movement Analysis Report generated successfully.")

        # Screenshot on success
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Stock_Movement_Analysis_Report_Success",
            attachment_type=allure.attachment_type.PNG
        )

    except Exception as e:

        # Screenshot on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Stock_Movement_Analysis_Report_Error",
            attachment_type=allure.attachment_type.PNG
        )

        # Attach error details
        allure.attach(
            str(e),
            name="Error Details",
            attachment_type=allure.attachment_type.TEXT
        )

        pytest.fail(f"❌ Test failed due to: {e}")
