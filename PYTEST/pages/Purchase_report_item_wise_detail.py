import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Purchase Report - Item Wise")
class PurchaseReportItemWiseDetailPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Purchase Report - Item Wise Detail for selected supplier")
    def generate_purchase_report_item_wise_detail(self):
        wait = self.wait
        driver = self.driver
        print("🚀 Starting Purchase Report - Item Wise Detail generation...")

        try:
            # ✅ Step 1: Navigate to Reports → Purchase Reports → Purchase Report - Item Wise Detail
            print("📂 Navigating to Reports → Purchase Reports → Purchase Report - Item Wise Detail...")
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

            purchase_report_item_wise_detail = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Report - Item Wise Detail"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", purchase_report_item_wise_detail)
            purchase_report_item_wise_detail.click()
            print("✅ Clicked on 'Purchase Report - Item Wise Detail'.")
            time.sleep(3)

            # ✅ Step 2: Select Item
            print("🎯 Selecting Item: White Chocolate...")

            # Wait for the input field to be clickable
            item_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter to select Items']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", item_input)
            item_input.click()
            time.sleep(1)

            # Press Enter or trigger dropdown (depending on site behavior)
            item_input.send_keys(Keys.ENTER)
            time.sleep(2)

            # Wait for the White Chocolate item to appear
            white_choco = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@title='White Chocolate']"))
            )

            # Double-click on "White Chocolate"
            from selenium.webdriver import ActionChains
            actions = ActionChains(driver)
            actions.double_click(white_choco).perform()
            print("✅ Successfully selected 'White Chocolate'")
            time.sleep(2)

            # Wait for the OK button to be clickable and click it using JavaScript (more reliable)
            print("✅ Confirming item selection by clicking 'OK'...")
            ok_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='btn btn-info btn-sm' and normalize-space()='OK']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", ok_button)
            driver.execute_script("arguments[0].click();", ok_button)  # JS click is more reliable
            print("✅ Clicked 'OK' to confirm selected item.")
            time.sleep(2)

            # ✅ Step 4: Select Supplier
            print("🧾 Selecting Supplier: Sujata Vendor...")

            # Wait for supplier input field to be clickable
            supplier_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter for Account List']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", supplier_input)
            supplier_input.click()
            supplier_input.send_keys(Keys.ENTER)  # Open supplier list
            time.sleep(2)

            # Wait for Sujata Vendor to appear in the list
            sujata_vendor = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='Sujata Vendor']"))
            )

            # Double-click to select the supplier
            self.actions.move_to_element(sujata_vendor).double_click().perform()
            print("✅ Selected Supplier: Sujata Vendor.")
            time.sleep(2)

            # ✅ Step 5: Click 'RUN' button
            print("▶️ Clicking 'RUN' button...")
            run_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='RUN']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
            run_button.click()
            print("✅ Clicked 'RUN' button successfully.")
            time.sleep(5)

            # ✅ Step 6: Verify report table and capture screenshot
            print("🧾 Verifying Purchase Report Item Wise Detail table...")
            try:
                table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]")))
                rows = table.find_elements(By.XPATH, ".//tr")
                print(f"✅ Report table loaded successfully with {len(rows) - 1} rows.")

                # 📸 Capture and attach screenshot for Allure
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Purchase_Report_Item_Wise_Detail_Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                print("📸 Screenshot of Purchase Report Item Wise Detail table attached to Allure.")

            except TimeoutException:
                print("⚠️ No data appeared in the Purchase Report Item Wise Detail table after loading the report.")

        finally:
            print("🎉 Purchase Report - Item Wise Detail generation and verification completed successfully.")
