import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Purchase_report_item_wise_detail import PurchaseReportItemWiseDetailPage


@allure.title("Generate Purchase Report Item Wise Detail in IMS Application")
@allure.description("Logs in, navigates to Reports → Purchase Reports → Purchase Report Item Wise Detail, and generates the report with screenshots on success and failure.")
def test_generate_purchase_report_item_wise_detail(setup):
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

        # --- Step 2: Generate Purchase Report Item Wise Detail ---
        purchase_detail_page = PurchaseReportItemWiseDetailPage(driver)
        purchase_detail_page.generate_purchase_report_item_wise_detail()
        print("📊 Purchase Report Item Wise Detail generated successfully.")

        # ✅ Step 3: Capture screenshot after successful report generation
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Purchase_Report_Item_Wise_Detail_Success",
            attachment_type=allure.attachment_type.PNG
        )
        print("📸 Screenshot captured after successful Purchase Report Item Wise Detail generation.")

    except Exception as e:
        # ❌ Step 4: Capture screenshot & error details on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Purchase_Report_Item_Wise_Detail_Error",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            str(e),
            name="Error_Details",
            attachment_type=allure.attachment_type.TEXT
        )
        pytest.fail(f"❌ Purchase Report Item Wise Detail test failed due to: {e}")
