import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Purchase_Invoice import PurchaseInvoicePage


# noinspection PyBroadException
@allure.title(" Generate Purchase Invoice in IMS Application")
@allure.description("Logs in, navigates to Transactions, then Purchase Invoice, and generates a purchase invoice.")
def test_generate_purchase_invoice(setup):
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

        invoice_page = PurchaseInvoicePage(driver)

        # --- Step 1: Navigate and Generate Invoice ---
        invoice_page.generate_invoice()
        print("🧾 Purchase invoice generated successfully.")

    except Exception as e:
        # Capture screenshot and log error details for Allure
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"❌ Purchase Invoice test failed due to: {e}")

