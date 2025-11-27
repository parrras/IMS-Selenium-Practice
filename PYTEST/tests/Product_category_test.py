import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Add_Product_Category import AddProductCategoryPage


@allure.title("Add Product Category in IMS Application")
@allure.description("Logs in, navigates to Product Category page, and adds a new category named 'Hygiene'.")
def test_add_product_category(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # Handle any previous session logout
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        # --- Step 2: Navigate to Product Category page ---
        add_category = AddProductCategoryPage(driver)
        add_category.navigate_to_add_product()

        # --- Step 3: Add Product Category ---
        add_category.add_product_category("Sunscreen")
        print("✅ Product category 'Sunscreen' added successfully.")

        # Screenshot for success proof
        allure.attach(driver.get_screenshot_as_png(), name="Add_Product_Category_Success", attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        # Capture screenshot and log error details for Allure
        allure.attach(driver.get_screenshot_as_png(), name="Add_Product_Category_Error", attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"❌ Test failed due to: {e}")
