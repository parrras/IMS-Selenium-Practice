import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Credit_Note_Book_Report import CreditNoteBookReportPage


# noinspection PyBroadException
@allure.title("Generate Credit Note Book Report in IMS Application")
@allure.description("Logs in, navigates to the Credit Note Book Report section, selects customer, and runs the report.")
def test_generate_credit_note_book_report(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # Optional: handle logout popup from previous session
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In button")

        # --- Step 2: Generate Credit Note Book Report ---
        report_page = CreditNoteBookReportPage(driver)
        report_page.generate_credit_note_book_report()
        print("📘 Credit Note Book Report generated successfully.")

        # --- Step 3: Capture screenshot of success ---
        allure.attach(driver.get_screenshot_as_png(), name="Credit_Note_Book_Report_Success",
                      attachment_type=allure.attachment_type.PNG)
        print("📸 Screenshot added for successful report generation.")

    except Exception as e:
        # 📸 Capture screenshot & log error in Allure
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(e), name="Error Details",
                      attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"❌ Credit Note Book Report test failed due to: {e}")
