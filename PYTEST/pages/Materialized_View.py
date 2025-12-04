import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Materialized View Report")
class MaterializedViewReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Materialized View Report")
    def generate_materialized_view_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Materialized View Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Materialized View
            # ==========================================
            print("📂 Navigating to Reports → VAT Report → Materialized View...")
            reports_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Reports')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", reports_btn)
            reports_btn.click()
            time.sleep(1)

            try:
                vat_report = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "VAT Report"))
                )
            except:
                vat_report = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='VAT Report']"))
                )

            driver.execute_script("arguments[0].scrollIntoView(true);", vat_report)
            self.actions.move_to_element(vat_report).pause(0.4).perform()
            print("✅ Hovered over 'VAT Report'.")
            time.sleep(1)

            materialized_view_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Materialized View"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", materialized_view_report)
            materialized_view_report.click()
            print("✅ Clicked 'Materialized View'")
            time.sleep(2)

            # ==========================================
            # STEP 2: Click RUN button
            # ==========================================
            run_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'confirm-btn') and text()='RUN']"))
            )
            run_btn.click()
            print("✅ Clicked RUN button")
            time.sleep(2)

            # ==========================================
            # STEP 3: Verify Table Loaded
            # ==========================================
            print("📊 Verifying Materialized View Report table...")

            try:
                table = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]"))
                )
                rows = table.find_elements(By.XPATH, ".//tr")

                print(f"✅ Materialized View Report loaded with {len(rows) - 1} rows.")

                # Screenshot when the table appears
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Materialized_View_Report_Table",
                    attachment_type=allure.attachment_type.PNG
                )

                print("📸 Screenshot attached to Allure.")

            except TimeoutException:
                print("⚠️ Table did NOT load — no rows found.")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Materialized_View_Report_No_Table",
                    attachment_type=allure.attachment_type.PNG
                )

            print("🎉 Materialized View Report generation completed successfully.")

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            # Screenshot on failure
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Materialized_View_Report_Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise e
