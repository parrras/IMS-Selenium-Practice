import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Sales_Report_Membership_wise import SalesReportMembershipWisePage


# noinspection PyBroadException
@allure.title("Generate Sales Report (Membership Wise) in IMS Application")
@allure.description(
    "Logs in, navigates to Reports → Loyalty & Promotion Report → Sales Report - Membership Wise, "
    "selects Member, selects Detail Report option, clicks RUN, and verifies the table."
)
def test_generate_sales_report_membership_wise(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
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

        # --- Step 2: Generate Sales Report Membership Wise ---
        sales_mem_page = SalesReportMembershipWisePage(driver)
        sales_mem_page.generate_sales_report_membership_wise()

        print("📊 Sales Report (Membership Wise) generated successfully.")

        # Screenshot on success
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Sales_Report_Membership_Wise_Success",
            attachment_type=allure.attachment_type.PNG
        )
        print("📸 Screenshot captured after successful report generation.")

    except Exception as e:
        # Screenshot on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Sales_Report_Membership_Wise_Error",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            str(e),
            name="Error_Details",
            attachment_type=allure.attachment_type.TEXT
        )
        pytest.fail(f"❌ Sales Report (Membership Wise) test failed due to: {e}")
