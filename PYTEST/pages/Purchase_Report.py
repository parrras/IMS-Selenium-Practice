import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# noinspection PyBroadException
@allure.feature("Purchase Book Report")
class PurchaseBookReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Purchase Book Report for a selected supplier and warehouse")
    def generate_purchase_book_report(self):
        wait = self.wait
        driver = self.driver
        print("🚀 Starting Purchase Book Report generation...")

        try:
            # ✅ Step 1: Navigate to Reports → Purchase Reports → Purchase Book Report
            print("📂 Navigating to Reports → Purchase Reports → Purchase Book Report...")
            reports_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Reports')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", reports_btn)
            reports_btn.click()
            time.sleep(2)

            try:
                purchase_reports = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Reports"))
                )
            except:
                purchase_reports = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Purchase Reports']"))
                )

            driver.execute_script("arguments[0].scrollIntoView(true);", purchase_reports)
            self.actions.move_to_element(purchase_reports).pause(0.5).perform()
            print("✅ Hovered over 'Purchase Reports'.")
            time.sleep(1)

            purchase_book_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Book Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", purchase_book_report)
            purchase_book_report.click()
            print("✅ Clicked on 'Purchase Book Report'.")
            time.sleep(3)

            # ✅ Step 2: Select Warehouse → Main Warehouse
            print("🏭 Selecting Warehouse: Main Warehouse...")
            try:
                warehouse_dropdown = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//select[@class='form-control input-text ng-untouched ng-pristine ng-valid']"))
                )
                Select(warehouse_dropdown).select_by_visible_text("Main Warehouse")
                print("✅ Selected 'Main Warehouse' successfully.")
            except Exception as e:
                raise AssertionError(f"❌ Failed to select Warehouse: {e}")
            time.sleep(3)

            # ✅ Step 3: Select Supplier → Sujata Vendor
            print("🧾 Selecting Supplier: Sujata Vendor...")
            supplier_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Account List']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", supplier_input)
            supplier_input.click()
            supplier_input.send_keys(Keys.ENTER)
            time.sleep(2)

            sujata_vendor = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Sujata Vendor']"))
            )
            self.actions.move_to_element(sujata_vendor).double_click().perform()
            print("✅ Selected Supplier: Sujata Vendor.")
            time.sleep(2)

            # ✅ Step 4: Click Run Button
            print("▶️ Clicking 'RUN' button...")
            run_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='RUN']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
            run_button.click()
            print("✅ Clicked 'RUN' button successfully.")

            # ✅ Step 5: Wait for report table & take success screenshot
            print("🧾 Waiting for report table to load...")
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]")))
            rows = table.find_elements(By.XPATH, ".//tr")
            print(f"✅ Report table loaded with {len(rows) - 1} rows.")

            driver.execute_script("arguments[0].scrollIntoView(true);", table)
            time.sleep(2)

            # ✅ Take screenshot after successful report generation
            success_screenshot = driver.get_screenshot_as_png()
            allure.attach(
                success_screenshot,
                name="Purchase_Book_Report_Success",
                attachment_type=allure.attachment_type.PNG
            )
            print("📸 Screenshot after report generation captured and attached to Allure.")

        except Exception as e:
            print(f"❌ Error occurred while generating Purchase Book Report: {e}")
            # 📸 Capture screenshot if any error occurs
            try:
                error_screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    error_screenshot,
                    name="Purchase_Book_Report_Error",
                    attachment_type=allure.attachment_type.PNG
                )
                print("📸 Error screenshot captured and attached to Allure.")
            except Exception as ss_err:
                print(f"⚠️ Failed to capture error screenshot: {ss_err}")

            # Re-raise the exception so pytest marks it as failed
            raise AssertionError(f"Purchase Book Report failed: {e}")

        finally:
            print("🎯 Purchase Book Report execution completed (success or failure).")
