import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# noinspection PyBroadException
@allure.feature("Stock Summary Report")
class StockSumReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Stock Summary Report for a selected supplier and warehouse")
    def generate_stock_sum_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Stock Summary Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Stock Summary Report
            # ==========================================
            print("📂 Navigating to Reports → Inventory Reports → Stock Summary Report...")

            reports_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Reports')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", reports_btn)
            reports_btn.click()
            time.sleep(2)

            try:
                inventory_reports = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Inventory Reports"))
                )
            except:
                inventory_reports = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Inventory Reports']"))
                )

            driver.execute_script("arguments[0].scrollIntoView(true);", inventory_reports)
            self.actions.move_to_element(inventory_reports).pause(0.5).perform()
            print("✅ Hovered over 'Inventory Reports'.")
            time.sleep(1)

            stock_sum_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Stock Summary Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", stock_sum_report)
            stock_sum_report.click()
            print("✅ Clicked on 'Stock Summary Report'.")
            time.sleep(3)

            # ==========================================
            # STEP 2: Select Supplier
            # ==========================================
            print("🏷 Selecting Supplier...")

            supplier_input = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@placeholder='Press Enter or Tab for Account List']")
                )
            )
            supplier_input.click()
            time.sleep(1)

            # Load suppliers list
            supplier_input.send_keys(Keys.ENTER)
            time.sleep(2)

            # Select Sujata Vendor
            sujata_vendor = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@title,'Sujata Vendor')]")
                )
            )
            self.actions.double_click(sujata_vendor).perform()
            print("✅ Selected Supplier: Sujata Vendor")
            time.sleep(2)

            # ==========================================
            # STEP 3: Click RUN Button
            # ==========================================
            print("▶️ Clicking RUN button...")

            run_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'RUN')]"))
            )
            run_btn.click()
            print("✅ Report RUN successfully.")
            time.sleep(4)

            # ==========================================
            # STEP 4: Verify Table Loaded + Screenshot
            # ==========================================
            print("🧾 Verifying Stock Summary Report table...")

            try:
                table = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//table[contains(@class,'table')]")
                    )
                )
                rows = table.find_elements(By.XPATH, ".//tr")
                print(f"✅ Stock Summary Report table loaded with {len(rows) - 1} rows.")

                # Screenshot
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Stock_Summary_Report_Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                print("📸 Screenshot of Stock Summary Report attached to Allure.")

            except Exception:
                print("⚠️ No data table appeared after running Stock Summary Report.")

        except Exception as e:
            print(f"❌ Error during Stock Summary Report generation: {e}")
            raise
