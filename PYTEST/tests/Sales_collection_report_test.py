import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Sales_collection_report import SalesCollectionReportPage


@allure.title("Generate Sales Collection Report in IMS Application")
@allure.description("Logs in, navigates to Reports → Sales Reports → Sales Collection Report, and generates the report with screenshots on success and failure.")
def test_generate_sales_collection_report(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # --- Optional: Handle logout pop-up if it appears ---
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        # --- Step 2: Generate Sales Collection Report ---
        sales_collection_page = SalesCollectionReportPage(driver)
        sales_collection_page.generate_sales_collection_report()
        print("📊 Sales Collection Report generated successfully.")

        # ✅ Step 3: Capture screenshot after successful generation
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Sales_Collection_Report_Success",
            attachment_type=allure.attachment_type.PNG
        )
        print("📸 Screenshot captured after successful Sales Collection Report generation.")

    except Exception as e:
        # ❌ Step 4: Capture screenshot & error details on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Sales_Collection_Report_Error",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            str(e),
            name="Error_Details",
            attachment_type=allure.attachment_type.TEXT
        )
        pytest.fail(f"❌ Sales Collection Report test failed due to: {e}")
