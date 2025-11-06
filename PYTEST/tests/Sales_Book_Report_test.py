import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Sales_Book_Report import SalesBookReportPage


@allure.title("Generate Sales Book Report in IMS Application")
@allure.description("Logs in, navigates to Reports → Sales Reports → Sales Book Report, and generates the report.")
def test_generate_sales_book_report(setup):
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

        # --- Step 2: Generate Sales Book Report ---
        sales_report_page = SalesBookReportPage(driver)
        sales_report_page.generate_sales_book_report()
        print("📊 Sales Book Report generated successfully.")

    except Exception as e:
        # Capture screenshot & log error in Allure
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"❌ Sales Book Report test failed due to: {e}")
