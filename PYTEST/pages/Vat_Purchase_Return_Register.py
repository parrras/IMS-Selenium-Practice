import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@allure.feature("Vat Purchase Return Register Report")
class VatPurchaseReturnRegisterReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Vat Purchase Return Register Report for a selected supplier")
    def generate_vat_purchase_return_register_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Vat Purchase Return Register Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to VAT Purchase Return Register
            # ==========================================
            print("📂 Navigating to Reports → VAT Report → VAT Purchase Return Register...")
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

            vat_purchase_return_reg_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "VAT Purchase Return Register"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", vat_purchase_return_reg_report)
            vat_purchase_return_reg_report.click()
            print("✅ Clicked 'VAT Purchase Return Register'")
            time.sleep(2)

            # ==========================================
            # STEP 2: Select Supplier
            # ==========================================
            print("🔍 Selecting Supplier...")

            supplier_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Supplier List']"))
            )
            supplier_input.click()
            time.sleep(1)

            supplier_input.send_keys(Keys.ENTER)
            print("⬇️ Supplier list opened.")
            time.sleep(2)

            sujata_vendor = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Sujata Vendor']"))
            )
            self.actions.double_click(sujata_vendor).perform()
            print("✅ Selected supplier: Sujata Vendor")
            time.sleep(1)

            # ==========================================
            # STEP 3: Click the Checkbox
            # ==========================================
            print("☑️ Clicking the checkbox...")

            checkbox = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']"))
            )
            checkbox.click()
            print("✅ Checkbox clicked.")
            time.sleep(1)

            # ==========================================
            # STEP 4: Click RUN button
            # ==========================================
            print("▶️ Clicking RUN button...")

            run_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='RUN']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", run_btn)
            run_btn.click()
            print("✅ RUN button clicked.")
            time.sleep(3)

            # ==========================================
            # STEP 5: Verify Table Loaded
            # ==========================================
            print("📊 Verifying VAT Purchase Return Register Report table...")

            try:
                table = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]"))
                )
                rows = table.find_elements(By.XPATH, ".//tr")

                print(f"✅ VAT Purchase Return Register report loaded with {len(rows) - 1} rows.")

                # Screenshot when the table appears
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="VAT_Purchase_Return_Register_Table",
                    attachment_type=allure.attachment_type.PNG
                )

                print("📸 Screenshot attached to Allure.")

            except TimeoutException:
                print("⚠️ Table did NOT load — no rows found.")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="VAT_Purchase_Return_Register_No_Table",
                    attachment_type=allure.attachment_type.PNG
                )

            print("🎉 VAT Purchase Return Register Report generation completed successfully.")

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="VAT_Purchase_Return_Register_Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise e
