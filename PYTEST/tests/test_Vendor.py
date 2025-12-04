# tests/test_Vendor.py
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Add_Vendor import Vendor


# noinspection PyBroadException
@allure.title("Create Customer in IMS Application")
@allure.description("Logs in, navigates to Customer Master, and creates a new customer record.")
def test_create_vendor(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)

    # --- Step 1: Login ---
    login = Login(driver)
    driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
    login.perform_login("Paras", "Ims@1234")
    print("✅ Logged into IMS")

    # Optional: handle logout from previous session
    try:
        login.perform_logout()
        login.perform_ok()
    except:
        pass

    login.click_signin()
    print("✅ Clicked Sign In")

    # --- Step 2: Create Customer ---
    vendor = Vendor(driver)
    vendor.create_vendor(
        name="Darren Watkins",
        address="Bali Indonesia",
        vat_no="900112226",
        email="ishowspeed@gmail.com",
        mobile="9899124353"
    )
    print("✅ Vendor creation process completed")

    # --- Step 3: Verify success message ---
    success_message = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Vendor saved successfully')]"))
    )
    assert success_message.is_displayed(), "❌ Vendor creation failed"
    print("🎉 Vendor created successfully and verified.")
