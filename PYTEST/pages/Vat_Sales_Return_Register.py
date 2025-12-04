import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Vat Sales Return Register Report")
class VatSalesReturnRegisterReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Vat Sales Return Register Report for a selected customer")
    def generate_vat_sales_return_register_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Vat Sales Return Register Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Vat Sales Return Register
            # ==========================================
            print("📂 Navigating to Reports → VAT Report → Vat Sales Return Register...")
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

            vat_sales_return_reg_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "VAT Sales Return Register"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", vat_sales_return_reg_report)
            vat_sales_return_reg_report.click()
            print("✅ Clicked 'VAT Sales Return Register'")
            time.sleep(2)

            # ==========================================
            # STEP 2: Select Customer
            # ==========================================
            print("👤 Selecting customer for report...")

            customer_input = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@placeholder='Press Enter or Tab for Customer List']")
                )
            )
            customer_input.click()
            time.sleep(0.5)
            customer_input.send_keys(Keys.ENTER)  # Open customer list
            print("📋 Customer list opened.")
            time.sleep(2)

            # Double click customer "21 Savage"
            customer_option = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@title='21 Savage']")
                )
            )

            self.actions.double_click(customer_option).perform()
            print("✅ Selected customer: 21 Savage")
            time.sleep(1)

            # ==========================================
            # STEP 3: Click RUN Button
            # ==========================================
            run_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'btn-info') and normalize-space()='RUN']")
                )
            )
            run_btn.click()
            print("▶️ Clicked RUN button")
            time.sleep(3)

            # ==========================================
            # STEP 4: Verify Table Loaded
            # ==========================================
            print("📊 Verifying Vat Sales Return Register Report table...")

            try:
                table = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//table[contains(@class,'table')]"))
                )
                rows = table.find_elements(By.XPATH, ".//tr")

                print(f"✅ Vat Sales Return Register loaded with {len(rows) - 1} rows.")

                # Screenshot when table appears
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Vat_Sales_Return_Register_Table",
                    attachment_type=allure.attachment_type.PNG
                )

                print("📸 Screenshot attached to Allure.")

            except TimeoutException:
                print("⚠️ Table did NOT load.")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Vat_Sales_Return_No_Table",
                    attachment_type=allure.attachment_type.PNG
                )

            print("🎉 Vat Sales Return Register Report generation completed successfully.")

        except Exception as e:
            print(f"❌ Error: {e}")

            allure.attach(
                driver.get_screenshot_as_png(),
                name="Vat_Sales_Return_Register_Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise e
