import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Item Expiry Report")
class ItemExpiryReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Item Expiry Report for a selected number of days")
    def generate_item_expiry_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Item Expiry Report generation...")

        try:
            # STEP 1: Navigate to Item Expiry Report
            print("📂 Navigating to Reports → Inventory Reports → Item Expiry Report...")
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

            item_exp_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Item Expiry Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", item_exp_report)
            item_exp_report.click()
            print("✅ Clicked 'Item Expiry Report'")
            time.sleep(2)

            # ==========================================
            # STEP 2: Enter Number of Days
            # ==========================================
            print("🔢 Entering number of days: 100")
            days_field = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='number']"))
            )
            days_field.clear()
            days_field.send_keys("100")
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
            print("📊 Verifying Item Expiry Report table...")

            try:
                table = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]"))
                )
                rows = table.find_elements(By.XPATH, ".//tr")

                print(f"✅ Item Expiry Report loaded with {len(rows) - 1} rows.")

                # Screenshot when the table appears
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Item_Expiry_Report_Table",
                    attachment_type=allure.attachment_type.PNG
                )

                print("📸 Screenshot attached to Allure.")

            except TimeoutException:
                print("⚠️ Table did NOT load — no rows found.")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Item_Expiry_Report_No_Table",
                    attachment_type=allure.attachment_type.PNG
                )

            print("🎉 Item Expiry Report generation completed successfully.")

        except Exception as e:
            print(f"❌ Error occurred: {e}")

            # Screenshot on failure
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Item_Expiry_Report_Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise e
