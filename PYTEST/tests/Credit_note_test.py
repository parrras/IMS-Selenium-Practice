import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Credit_note import CreditNotePage


# noinspection PyBroadException
@allure.title("Generate Credit Note in IMS Application")
@allure.description("Logs in, navigates to the Credit Note section, selects a Ref Bill, and saves the Credit Note.")
def test_generate_credit_note(setup):
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

        # --- Step 2: Create Credit Note ---
        credit_note_page = CreditNotePage(driver)
        credit_note_page.create_credit_note()
        print("🧾 Credit Note created successfully.")

        # --- Step 3: Capture screenshot after successful Credit Note creation ---
        allure.attach(driver.get_screenshot_as_png(), name="Credit_Note_Success_Screenshot",
                      attachment_type=allure.attachment_type.PNG)
        print("📸 Screenshot captured for successful Credit Note creation.")

    except Exception as e:
        # 📸 Capture screenshot & log error in Allure
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details",
                      attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"❌ Credit Note test failed due to: {e}")
