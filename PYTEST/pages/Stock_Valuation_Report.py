import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# noinspection PyBroadException
@allure.feature("Stock Valuation Report")
class StockValuationReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Stock Valuation Report for a selected warehouse and item")
    def generate_stock_valuation_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Stock Valuation Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Stock Valuation Report
            # ==========================================
            print("📂 Navigating to Reports → Inventory Reports → Stock Valuation Report...")

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

            stock_val_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Stock Valuation Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", stock_val_report)
            stock_val_report.click()
            print("✅ Clicked 'Stock Valuation Report'")
            time.sleep(2)

            # ==========================================
            # STEP 2: Select Item
            # ==========================================
            print("🏷 Selecting Item...")

            item_input = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@placeholder='Press Enter or Tab for Item List']")
                )
            )
            item_input.click()
            time.sleep(1)

            # Press ENTER to load item list
            item_input.send_keys(Keys.ENTER)
            time.sleep(2)

            # Wait for item and double-click "White Chocolate"
            white_choco = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@title,'White Chocolate')]")
                )
            )
            self.actions.double_click(white_choco).perform()
            print("✅ Selected Item: White Chocolate")
            time.sleep(2)

            # ==========================================
            # STEP 3: RUN the Report
            # ==========================================
            print("▶️ Clicking RUN button...")

            run_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'RUN')]")
                )
            )
            run_btn.click()
            print("✅ Report RUN successfully.")
            time.sleep(4)

            # ==========================================
            # STEP 4: Verify Report Table + Screenshot
            # ==========================================
            print("🧾 Verifying Stock Valuation Report table...")

            try:
                table = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//table[contains(@class,'table')]")
                    )
                )
                rows = table.find_elements(By.XPATH, ".//tr")
                print(f"✅ Stock Valuation Report table loaded with {len(rows) - 1} rows.")

                # Screenshot when table appears
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Stock_Valuation_Report_Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                print("📸 Screenshot of Stock Valuation Report attached.")

            except:
                print("⚠️ No report table found after running Stock Valuation Report.")

        except Exception as e:
            print(f"❌ Error in Stock Valuation Report: {e}")
            raise
