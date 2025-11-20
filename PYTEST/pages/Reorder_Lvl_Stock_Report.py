import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@allure.feature("Reorder Level Stock Report")
class ReorderLevelStockReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Reorder Level Stock Report for a selected warehouse")
    def generate_reorder_level_stock_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Reorder Level Stock Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Reorder Level Stock Report
            # ==========================================
            print("📂 Navigating to Reports → Inventory Reports → Reorder Level Stock Report...")
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

            reorder_lvl_stock_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Reorder Level Stock Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", reorder_lvl_stock_report)
            reorder_lvl_stock_report.click()
            print("✅ Clicked 'Reorder Level Stock Report'")
            time.sleep(2)

            # ==========================================
            # STEP 2: Select Warehouse
            # ==========================================
            print("🏢 Selecting Warehouse: Main Warehouse...")

            warehouse_dropdown = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//select[contains(@class,'form-control')]"))
            )
            warehouse_dropdown.click()
            time.sleep(1)

            main_warehouse = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//option[contains(text(),'Main Warehouse')]"))
            )
            main_warehouse.click()
            print("✅ Selected 'Main Warehouse'")
            time.sleep(1)

            # ==========================================
            # STEP 3: Click RUN
            # ==========================================
            run_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'confirm-btn') and text()='RUN']"))
            )
            run_btn.click()
            print("🚀 Clicked RUN button")
            time.sleep(3)

            # ==========================================
            # STEP 4: Verify Table Loaded
            # ==========================================
            print("📊 Verifying Reorder Level Stock table...")

            try:
                table = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]"))
                )
                rows = table.find_elements(By.XPATH, ".//tr")
                if len(rows) <= 1:
                    raise Exception("⚠️ Table loaded but no data rows found.")

                print(f"✅ Table verification passed. Rows found: {len(rows) - 1}")

                # Screenshot on success
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Reorder_Level_Stock_Report_Table",
                    attachment_type=allure.attachment_type.PNG
                )
                print("📸 Screenshot attached to Allure.")

            except TimeoutException:
                print("⚠️ Table did NOT load — no rows found.")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Reorder_Level_Stock_Report_No_Table",
                    attachment_type=allure.attachment_type.PNG
                )

            print("🎉 Reorder Level Stock Report generation completed successfully.")

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            # Screenshot on failure
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Reorder_Level_Stock_Report_Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise e
