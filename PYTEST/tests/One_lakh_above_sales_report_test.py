import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.One_Lakh_Above_Sales_Report import OneLakhAboveSalesReportPage


@allure.title("Generate One Lakh Above Sales Report in IMS Application")
@allure.description("Logs in, navigates to One Lakh Above Sales Report, clicks RUN, and verifies the table.")
def test_one_lakh_above_sales_report(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # Handle previous active session popup (if appears)
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        # --- Step 2: Generate One Lakh Above Sales Report ---
        one_lakh_sales_report = OneLakhAboveSalesReportPage(driver)
        one_lakh_sales_report.generate_one_lakh_above_sales_report()

        print("✅ One Lakh Above Sales Report generated successfully.")

        # Screenshot on success
        allure.attach(
            driver.get_screenshot_as_png(),
            name="One_Lakh_Above_Sales_Report_Success",
            attachment_type=allure.attachment_type.PNG
        )

    except Exception as e:

        # Screenshot on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="One_Lakh_Above_Sales_Report_Error",
            attachment_type=allure.attachment_type.PNG
        )

        # Attach exception details
        allure.attach(
            str(e),
            name="Error Details",
            attachment_type=allure.attachment_type.TEXT
        )

        pytest.fail(f"❌ Test failed due to: {e}")
