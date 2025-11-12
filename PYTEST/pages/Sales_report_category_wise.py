import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@allure.feature("Sales Report - Item Wise")
class SalesReportCategoryWisePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Sales Report - Category Wise")
    def generate_sales_report_category_wise(self):
        wait = self.wait
        driver = self.driver
        actions = self.actions
        print("🚀 Starting Sales Report - Category Wise generation...")

        # ✅ Step 1: Navigate to Reports → Sales Reports → Sales Report - Item Wise
        print("📂 Navigating to Reports → Sales Reports → Sales Report - Category Wise...")
        reports_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Reports')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", reports_btn)
        reports_btn.click()
        time.sleep(2)

        try:
            sales_reports = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Sales Report"))
            )
        except:
            sales_reports = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Sales Report']"))
            )

        driver.execute_script("arguments[0].scrollIntoView(true);", sales_reports)
        actions.move_to_element(sales_reports).pause(0.5).perform()
        print("✅ Hovered over 'Sales Reports'.")
        time.sleep(1)

        item_wise_report = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sales Report - Category Wise"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", item_wise_report)
        item_wise_report.click()
        print("✅ Clicked on 'Sales Report - Category Wise'.")
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
            allure.attach(screenshot, name="Sales_Report_Category_Wise", attachment_type=allure.attachment_type.PNG)

        except TimeoutException:
            print("⚠️ No data appeared in the report table.")

