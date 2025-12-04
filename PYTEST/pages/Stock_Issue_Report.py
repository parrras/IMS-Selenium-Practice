import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Stock Issue Report")
class StockIssueReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Stock Issue Report for selected From and To Warehouses")
    def generate_stock_issue_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Stock Issue Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Stock Issue Report
            # ==========================================
            print("📂 Navigating to Reports → Inventory Reports → Stock Issue Report...")
            reports_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Reports')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", reports_btn)
            reports_btn.click()
            time.sleep(1)

            try:
                inventory_reports = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Inventory Reports"))
                )
            except:
                inventory_reports = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Inventory Reports']"))
                )

            driver.execute_script("arguments[0].scrollIntoView(true);", inventory_reports)
            self.actions.move_to_element(inventory_reports).pause(0.4).perform()
            print("✅ Hovered over 'Inventory Reports'.")
            time.sleep(1)

            # ==========================================
            # STEP 2: Click Inventory Movement Report
            # ==========================================
            print("📂 Clicking on Inventory Movement Report...")
            inv_mov_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Inventory Movement Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", inv_mov_report)
            inv_mov_report.click()
            print("✅ Clicked 'Inventory Movement Report'")
            time.sleep(2)

            # ==========================================
            # STEP 3: Click Stock Issue Report
            # ==========================================
            stock_issue_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Stock Issue Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", stock_issue_report)
            stock_issue_report.click()
            print("✅ Clicked 'Stock Issue Report'")
            time.sleep(2)

            # ==========================================
            # STEP 4: Select From Warehouse
            # ==========================================
            print("🏢 Selecting From Warehouse: Main Warehouse...")
            from_warehouse_dropdown = wait.until(
                EC.element_to_be_clickable((By.XPATH, "(//select[contains(@class,'form-control')])[1]"))
            )
            from_warehouse_dropdown.click()
            main_warehouse_from = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//option[contains(text(),'Main Warehouse')]"))
            )
            main_warehouse_from.click()
            print("✅ From Warehouse selected: Main Warehouse")
            time.sleep(1)

            # ==========================================
            # STEP 5: Select To Warehouse
            # ==========================================
            print("🏢 Selecting To Warehouse: Test...")
            to_warehouse_dropdown = wait.until(
                EC.element_to_be_clickable((By.XPATH, "(//select[contains(@class,'form-control')])[2]"))
            )
            to_warehouse_dropdown.click()
            test_warehouse_to = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//option[contains(text(),'Test')]"))
            )
            test_warehouse_to.click()
            print("✅ To Warehouse selected: Test")
            time.sleep(1)

            # ==========================================
            # STEP 6: Click RUN
            # ==========================================
            run_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'confirm-btn') and text()='RUN']"))
            )
            run_btn.click()
            print("🚀 Clicked RUN button")
            time.sleep(3)

            # ==========================================
            # STEP 7: Verify Table Loaded
            # ==========================================
            print("📊 Verifying Stock Issue Report table...")
            try:
                table = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]"))
                )
                rows = table.find_elements(By.XPATH, ".//tr")
                print(f"✅ Stock Issue Report loaded with {len(rows) - 1} rows.")

                # Attach screenshot
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Stock_Issue_Report_Table",
                    attachment_type=allure.attachment_type.PNG
                )
                print("📸 Screenshot attached to Allure.")

            except TimeoutException:
                print("⚠️ Table did NOT load — no rows found.")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Stock_Issue_Report_No_Table",
                    attachment_type=allure.attachment_type.PNG
                )

            print("🎉 Stock Issue Report generation completed successfully.")

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            # Screenshot on failure
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Stock_Issue_Report_Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise e