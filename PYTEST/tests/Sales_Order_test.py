import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Sales_Order import SalesOrderPage


# noinspection PyBroadException
@allure.title("Generate Sales Order in IMS Application")
@allure.description(
    "Logs in, navigates to Transactions → Sales Transaction → Sales Order, "
    "fills Reference No, selects Customer, adds items via barcode, sets quantity, "
    "adds remarks, and finally SAVES the order with verification."
)
def test_generate_sales_order(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- STEP 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # Optional: Handle active session popup
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        # --- STEP 2: Generate Sales Order ---
        sales_order_page = SalesOrderPage(driver)
        sales_order_page.generate_sales_order()

        print("📦 Sales Order generated successfully.")

        # Screenshot on success
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Sales_Order_Success",
            attachment_type=allure.attachment_type.PNG
        )
        print("📸 Screenshot captured after successful Sales Order creation.")

    except Exception as e:
        # Screenshot on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Sales_Order_Error",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            str(e),
            name="Error_Details",
            attachment_type=allure.attachment_type.TEXT
        )

        pytest.fail(f"❌ Sales Order test failed due to: {e}")
