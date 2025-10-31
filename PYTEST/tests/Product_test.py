import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Add_Product import AddProductPage


# noinspection PyBroadException
@allure.title("Add Products in IMS Application")
@allure.description("Logs in, navigates to Product Master, and adds multiple products.")
def test_add_products(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        try:
            login.perform_logout()
            login.perform_ok()
        except:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        add_product = AddProductPage(driver)

        # --- Step 2: Navigate to Add Product ---
        add_product.navigate_to_add_product()

        # --- Step 3: Select Item Group ---
        add_product.select_item_group()

        # --- Step 4: Add 10 Products ---
        add_product.add_multiple_products(count=10)

        allure.attach("✅ Test completed successfully", name="Result", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        # Capture screenshot and log error details
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"❌ Test failed due to: {e}")
