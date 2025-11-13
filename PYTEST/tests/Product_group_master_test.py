import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Add_Product_Group_Master import AddProductGroupMasterPage


@allure.title("Add Product Group in IMS Application")
@allure.description("Logs in, navigates to Product Group Master page, selects parent group, and adds a new product group named 'Hygiene'.")
def test_add_product_group_master(setup):
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

        # --- Step 2: Navigate to Product Group Master page ---
        add_group = AddProductGroupMasterPage(driver)
        add_group.navigate_to_add_product()

        # --- Step 3: Select Parent Group ---
        add_group.select_item_group()

        # --- Step 4: Fill Group Details and Save ---
        add_group.fill_group_details_and_save()
        print("✅ Product group 'Hygiene' added successfully.")

        # Screenshot for success proof
        allure.attach(driver.get_screenshot_as_png(), name="Add_Product_Group_Success", attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        # Capture screenshot and log error details for Allure
        allure.attach(driver.get_screenshot_as_png(), name="Add_Product_Group_Error", attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"❌ Test failed due to: {e}")
