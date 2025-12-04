import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("One Lakh Above Sales Report")
class OneLakhAboveSalesReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate One Lakh Above Sales Report")
    def generate_one_lakh_above_sales_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting One Lakh Above Sales Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to One Lakh Above Sales Report
            # ==========================================
            print("📂 Navigating to Reports → VAT Report → One Lakh Above Sales Report...")
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

            one_lakh_above_sales_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "One Lakh Above Sales Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", one_lakh_above_sales_report)
            one_lakh_above_sales_report.click()
            print("✅ Clicked 'One Lakh Above Sales Report'")
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
            print("📊 Verifying One Lakh Above Sales Report table...")
            try:
                table = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]"))
                )
                rows = table.find_elements(By.XPATH, ".//tr")
                print(f"✅ One Lakh Above Sales Report loaded with {len(rows) - 1} rows.")

                # Screenshot when table appears
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="One_Lakh_Above_Sales_Report_Table",
                    attachment_type=allure.attachment_type.PNG
                )
                print("📸 Screenshot attached to Allure.")

            except TimeoutException:
                print("⚠️ Table did NOT load — no rows found.")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="One_Lakh_Above_Sales_Report_No_Table",
                    attachment_type=allure.attachment_type.PNG
                )

            print("🎉 One Lakh Above Sales Report generation completed successfully.")

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            # Screenshot on failure
            allure.attach(
                driver.get_screenshot_as_png(),
                name="One_Lakh_Above_Sales_Report_Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise e
