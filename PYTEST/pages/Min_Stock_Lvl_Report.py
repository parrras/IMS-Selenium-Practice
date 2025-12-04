import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# noinspection PyBroadException
@allure.feature("Minimum Stock Level Report")
class MinStockLevelReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Minimum Stock Level Report for a selected warehouse")
    def generate_min_stock_level_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Minimum Stock Level Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Minimum Stock Level Report
            # ==========================================
            print("📂 Navigating to Reports → Inventory Reports → Minimum Stock Level Report...")
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

            min_stock_lvl_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Minimum Stock Level Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", min_stock_lvl_report)
            min_stock_lvl_report.click()
            print("✅ Clicked 'Minimum Stock Level Report'")
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

            print("🎉 Minimum Stock Level Report generation completed successfully.")

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            raise e
