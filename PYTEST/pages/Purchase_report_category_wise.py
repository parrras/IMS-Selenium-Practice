import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Purchase Report - Category Wise")
class PurchaseReportCategoryWisePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Purchase Report - Category Wise for selected supplier")
    def generate_purchase_report_category_wise(self):
        wait = self.wait
        driver = self.driver
        print("🚀 Starting Purchase Report - Category Wise generation...")


        # ✅ Step 1: Navigate to Reports → Purchase Reports → Purchase Report - Item Wise
        print("📂 Navigating to Reports → Purchase Reports → Purchase Report - Category Wise...")
        reports_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Reports')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", reports_btn)
        reports_btn.click()
        time.sleep(2)

        try:
            purchase_reports = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Reports"))
            )
        except:
            purchase_reports = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Purchase Reports']"))
            )

        driver.execute_script("arguments[0].scrollIntoView(true);", purchase_reports)
        self.actions.move_to_element(purchase_reports).pause(0.5).perform()
        print("✅ Hovered over 'Purchase Reports'.")
        time.sleep(1)

        purchase_report_supplier_wise = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Report - Category Wise"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", purchase_report_supplier_wise)
        purchase_report_supplier_wise.click()
        print("✅ Clicked on 'Purchase Report - Item Wise'.")
        time.sleep(3)


        # Step 2: Select Detail Report radio button
        detail_report_radio = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='reportType' and @value='1']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", detail_report_radio)
        detail_report_radio.click()
        print("✅ Detail Report selected")
        time.sleep(1)

        # Step 3: Click RUN button
        run_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='RUN']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
        run_button.click()
        print("✅ Clicked RUN button")
        time.sleep(5)

        # Step 4: Verify report table
        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]")))
            rows = table.find_elements(By.XPATH, ".//tr")
            print(f"✅ Report table loaded with {len(rows) - 1} rows")

            # Capture screenshot
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, name="Purchase_Report_Category_Wise", attachment_type=allure.attachment_type.PNG)

        except TimeoutException:
            print("⚠️ No data appeared in the report table.")


