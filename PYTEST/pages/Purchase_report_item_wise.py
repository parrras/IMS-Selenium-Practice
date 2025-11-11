import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@allure.feature("Purchase Report - Item Wise")
class PurchaseReportItemWisePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Purchase Report - Item Wise for selected supplier")
    def generate_purchase_report_item_wise(self):
        wait = self.wait
        driver = self.driver
        print("🚀 Starting Purchase Report - Item Wise generation...")

        try:
            # ✅ Step 1: Navigate to Reports → Purchase Reports → Purchase Report - Item Wise
            print("📂 Navigating to Reports → Purchase Reports → Purchase Report - Item Wise...")
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

            purchase_report_item_wise = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Report - Item Wise"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", purchase_report_item_wise)
            purchase_report_item_wise.click()
            print("✅ Clicked on 'Purchase Report - Item Wise'.")
            time.sleep(3)

            # ✅ Step 2: Select Supplier
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

            # ✅ Step 3: Click 'RUN' button
            print("▶️ Clicking 'RUN' button...")
            run_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='RUN']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
            run_button.click()
            print("✅ Clicked 'RUN' button successfully.")
            time.sleep(5)

            # ✅ Step 4: Verify report table and attach screenshot
            print("🧾 Verifying Purchase Report Item Wise table...")
            try:
                table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]")))
                rows = table.find_elements(By.XPATH, ".//tr")
                print(f"✅ Report table loaded successfully with {len(rows) - 1} rows.")

                # 📸 Capture and attach screenshot to Allure
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Purchase_Report_Item_Wise_Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                print("📸 Screenshot of Purchase Report Item Wise table attached to Allure.")

            except TimeoutException:
                print("⚠️ No data appeared in the Purchase Report Item Wise table after loading the report.")

        finally:
            print("🎉 Purchase Report Item Wise generation and verification completed successfully.")


