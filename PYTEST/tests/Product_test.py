import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Add_Product import AddProductPage


# noinspection PyBroadException
@allure.title("Add Products and Generate Invoice in IMS Application")
@allure.description("Logs in, navigates to Product Master, adds 10 products, and generates a purchase invoice.")
def test_add_products(setup):
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

        # --- Step 2: Add Product Page ---
        add_product = AddProductPage(driver)

        # Navigate to Add Product page
        add_product.navigate_to_add_product()

        # Select Item Group
        add_product.select_item_group()

        # Add 10 Products (first 5 inventory & ticked, last 5 service & unticked)
        add_product.add_multiple_products(count=10)

    except Exception as e:
        # Capture screenshot and log error details for Allure
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"❌ Test failed due to: {e}")
