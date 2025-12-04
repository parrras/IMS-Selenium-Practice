import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Vat_Sales_Register import VatSalesRegisterReportPage


# noinspection PyBroadException
@allure.title("Generate VAT Sales Register Report in IMS Application")
@allure.description("Logs in, navigates to VAT Sales Register Report, selects customer, and runs the report.")
def test_vat_sales_register_report(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # Handle previous active session popup (if appears)
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        # --- Step 2: Generate VAT Sales Register Report ---
        vat_sales_report = VatSalesRegisterReportPage(driver)
        vat_sales_report.generate_vat_sales_register_report()

        print("✅ VAT Sales Register Report generated successfully.")

        # Screenshot on success
        allure.attach(
            driver.get_screenshot_as_png(),
            name="VAT_Sales_Register_Success",
            attachment_type=allure.attachment_type.PNG
        )

    except Exception as e:

        # Screenshot on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="VAT_Sales_Register_Error",
            attachment_type=allure.attachment_type.PNG
        )

        # Attach exception details
        allure.attach(
            str(e),
            name="Error Details",
            attachment_type=allure.attachment_type.TEXT
        )

        pytest.fail(f"❌ Test failed due to: {e}")
