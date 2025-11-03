import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Sales_Invoice import SalesInvoicePage


# noinspection PyBroadException
@allure.title(" Generate Sales Invoice in IMS Application")
@allure.description("Logs in, navigates to Transactions, then Sales Tax Invoice, and generates a sales tax invoice.")
def test_generate_sales_invoice(setup):
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

        sales_invoice_page = SalesInvoicePage(driver)

        # --- Step 1: Navigate and Generate Invoice ---
        sales_invoice_page.generate_sales_invoice()
        print("🧾 Purchase sales invoice generated successfully.")

    except Exception as e:
        # Capture screenshot and log error details for Allure
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"❌ Sales Invoice test failed due to: {e}")