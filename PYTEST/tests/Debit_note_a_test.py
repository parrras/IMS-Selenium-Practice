import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Debit_Note import DebitNotePage

# noinspection PyBroadException

@allure.title("Create Debit Note in IMS Application")
@allure.description("Logs in, navigates to Debit Note (Purchase Return), fills details, barcodes, and saves the entry.")
def test_create_debit_note(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # Optional: handle previous session logout popup
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        # --- Step 2: Create Debit Note ---
        debit_note_page = DebitNotePage(driver)
        debit_note_page.create_debit_note()
        print("🧾 Debit Note created successfully.")

        # --- Step 3: Capture screenshot for success ---
        allure.attach(driver.get_screenshot_as_png(), name="Debit_Note_Success",
                      attachment_type=allure.attachment_type.PNG)
        print("📸 Screenshot captured for successful Debit Note creation.")

    except Exception as e:
        # 📸 Capture screenshot & log error in Allure
        allure.attach(driver.get_screenshot_as_png(), name="Debit_Note_Error",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)

        pytest.fail(f"❌ Debit Note test failed due to: {e}")
