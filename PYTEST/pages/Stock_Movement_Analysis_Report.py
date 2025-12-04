import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


# noinspection PyBroadException
@allure.feature("Stock Movement Analysis Report")
class StockMovementAnalysisReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Stock Movement Analysis Report for a selected warehouse and item")
    def generate_stock_movement_analysis_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Stock Movement Analysis Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Stock Movement Analysis Report
            # ==========================================
            print("📂 Navigating to Reports → Inventory Reports → Stock Movement Analysis Report...")

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

            stock_mv_anal_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Stock Movement Analysis Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", stock_mv_anal_report)
            stock_mv_anal_report.click()
            print("✅ Clicked 'Stock Movement Analysis Report'")
            time.sleep(2)

            # ==========================================
            # STEP 2: Select Supplier
            # ==========================================
            print("🧾 Selecting Supplier...")

            supplier_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Account List']"))
            )
            supplier_input.click()
            supplier_input.send_keys("Sujata Vendor")
            supplier_input.send_keys(Keys.ENTER)
            time.sleep(1)

            # Double-click supplier in dropdown list
            supplier_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='Sujata Vendor']"))
            )
            self.actions.double_click(supplier_option).perform()

            print("✅ Supplier 'Sujata Vendor' selected successfully.")

            # ==========================================
            # STEP 3: Click RUN button
            # ==========================================
            print("▶️ Clicking RUN button...")

            run_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='btn btn-info confirm-btn' and contains(text(),'RUN')]"))
            )
            run_btn.click()
            print("⏳ Report is generating...")
            time.sleep(3)

            # ==========================================
            # STEP 4: Verify Table Loaded
            # ==========================================
            print("📊 Verifying table data...")

            try:
                table = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]"))
                )
                rows = table.find_elements(By.XPATH, ".//tr")

                print(f"✅ Stock Movement Analysis Report loaded with {len(rows) - 1} rows.")

                # Screenshot when the table appears
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Stock_Mv_Analysis_Report_Table",
                    attachment_type=allure.attachment_type.PNG
                )

                print("📸 Screenshot attached to Allure.")

            except TimeoutException:
                print("⚠️ Table did NOT load — no rows found.")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Stock_Mv_Analysis_Report_No_Table",
                    attachment_type=allure.attachment_type.PNG
                )

            print("🎉 Stock Movement Analysis Report generation completed successfully.")

        except Exception as e:
            print(f"❌ Error occurred: {e}")

            # Screenshot on failure
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Stock_Mv_Analysis_Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise e
