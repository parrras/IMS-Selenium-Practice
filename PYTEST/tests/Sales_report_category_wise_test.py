import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Sales_report_category_wise import SalesReportCategoryWisePage


@allure.title("Generate Sales Report Category Wise in IMS Application")
@allure.description("Logs in, navigates to Reports → Sales Reports → Sales Report Category Wise, and generates the report with screenshots on success and failure.")
def test_generate_sales_report_category_wise(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)
    login = Login(driver)

    try:
        # --- Step 1: Login ---
        driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        login.perform_login("Paras", "Ims@1234")
        print("✅ Logged into IMS")

        # --- Optional: Handle logout pop-up if exists ---
        try:
            login.perform_logout()
            login.perform_ok()
        except Exception:
            pass

        login.click_signin()
        print("✅ Clicked Sign In")

        # --- Step 2: Generate Purchase Report Category Wise ---
        sales_report_category_page = SalesReportCategoryWisePage(driver)
        sales_report_category_page.generate_sales_report_category_wise()
        print("📊 Sales Report Category Wise generated successfully.")

        # ✅ Step 3: Capture screenshot after successful report generation
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Sales_Report_Category_Wise_Success",
            attachment_type=allure.attachment_type.PNG
        )
        print("📸 Screenshot captured after successful Sales Report Category Wise generation.")

    except Exception as e:
        # ❌ Step 4: Capture screenshot & error details on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Sales_Report_Category_Wise_Error",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            str(e),
            name="Error_Details",
            attachment_type=allure.attachment_type.TEXT
        )
        pytest.fail(f"❌ Sales Report Category Wise test failed due to: {e}")
