import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Debit_Note_Book_Report import DebitNoteBookReportPage


# noinspection PyBroadException
@allure.title("Generate Debit Note Book Report in IMS Application")
@allure.description("Logs in, navigates to Debit Note Book Report, selects Detail Report, runs report, and verifies table.")
def test_generate_debit_note_book_report(setup):
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

        # --- Step 2: Generate Debit Note Book Report ---
        debit_report_page = DebitNoteBookReportPage(driver)
        debit_report_page.generate_debit_note_book_report()
        print("📘 Debit Note Book Report generated successfully.")

        # --- Step 3: Screenshot for success ---
        allure.attach(driver.get_screenshot_as_png(), name="Debit_Note_Book_Report_Success",
                      attachment_type=allure.attachment_type.PNG)
        print("📸 Screenshot captured for Debit Note Book Report success.")

    except Exception as e:
        # 📸 Capture failure screenshot
        allure.attach(driver.get_screenshot_as_png(), name="Debit_Note_Book_Report_Error",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)

        pytest.fail(f"❌ Debit Note Book Report test failed due to: {e}")
