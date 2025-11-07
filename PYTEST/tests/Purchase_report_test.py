import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Purchase_Report import PurchaseBookReportPage


@allure.title("Generate Purchase Book Report in IMS Application")
@allure.description("Logs in, navigates to Reports → Purchase Reports → Purchase Book Report, selects filters, and generates the report with screenshot evidence.")
def test_generate_purchase_book_report(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # Optional: handle logout from previous session
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        # --- Step 2: Navigate and Generate Purchase Book Report ---
        report_page = PurchaseBookReportPage(driver)
        report_page.generate_purchase_book_report()
        print("📊 Purchase Book Report generated successfully.")

        # ✅ Take screenshot after successful report generation
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Purchase_Report_Success",
            attachment_type=allure.attachment_type.PNG
        )
        print("📸 Screenshot captured after report generation.")

    except Exception as e:
        # ❌ Capture screenshot and error details if something fails
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Error_Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            str(e),
            name="Error_Details",
            attachment_type=allure.attachment_type.TEXT
        )
        pytest.fail(f"❌ Purchase Book Report test failed due to: {e}")
