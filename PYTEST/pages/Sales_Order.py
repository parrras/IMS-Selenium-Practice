import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# noinspection PyBroadException
@allure.feature("Sales Order")
class SalesOrderPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Sales Order")
    def generate_sales_order(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Sales Order generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Sales Order
            # ==========================================
            print("📂 Navigating to Transactions → Sales Transaction → Sales Order...")

            transaction_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Transactions')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", transaction_btn)
            transaction_btn.click()
            time.sleep(1)

            try:
                sales_trn = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Sales Transaction"))
                )
            except:
                sales_trn = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Sales Transaction']"))
                )

            driver.execute_script("arguments[0].scrollIntoView(true);", sales_trn)
            self.actions.move_to_element(sales_trn).pause(0.4).perform()
            print("✅ Hovered over 'Sales Transaction'.")
            time.sleep(1)

            sales_order = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Sales Order"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", sales_order)
            sales_order.click()
            print("✅ Clicked 'Sales Order'")
            time.sleep(2)

            # ==========================================
            # STEP 2: Enter Reference Number
            # ==========================================
            print("✏️ Entering Reference Number...")
            ref_field = wait.until(
                EC.element_to_be_clickable((By.ID, "invoiceNO"))
            )
            ref_field.clear()
            ref_field.send_keys("REF" + str(int(time.time())))   # random unique ref
            time.sleep(1)

            # ==========================================
            # STEP 3: Select Customer
            # ==========================================
            print("🧑 Selecting Customer...")

            customer_field = wait.until(
                EC.element_to_be_clickable((By.ID, "customerselectid"))
            )
            customer_field.click()
            customer_field.send_keys("\n")   # press Enter
            time.sleep(1)

            customer_to_select = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='Carti']"))
            )
            self.actions.double_click(customer_to_select).perform()
            print("✅ Customer 'Carti' selected.")
            time.sleep(1)

            # ==========================================
            # STEP 4: Enter Remark
            # ==========================================
            print("📝 Entering remarks...")
            remark_field = wait.until(
                EC.element_to_be_clickable((By.ID, "remarksid"))
            )
            remark_field.click()
            remark_field.send_keys("Automated Sales Order Test")
            time.sleep(1)

            # ==========================================
            # STEP 5: Enter Barcode 1 → 1.3
            # ==========================================
            print("📦 Adding first item (Barcode 1.3)...")

            barcode_field = wait.until(
                EC.element_to_be_clickable((By.ID, "barcodeField"))
            )
            barcode_field.click()
            barcode_field.clear()
            barcode_field.send_keys("1.3")
            barcode_field.send_keys("\n")
            time.sleep(5)

            quantity_field = wait.until(
                EC.element_to_be_clickable((By.ID, "quantityBarcode"))
            )
            quantity_field.clear()
            quantity_field.send_keys("20")
            quantity_field.send_keys("\n")
            time.sleep(5)

            # ==========================================
            # STEP 6: Enter Barcode 2 → 14.3
            # ==========================================
            print("📦 Adding second item (Barcode 14.3)...")

            barcode_field = wait.until(
                EC.element_to_be_clickable((By.ID, "barcodeField"))
            )
            barcode_field.click()
            barcode_field.clear()
            barcode_field.send_keys("14.3")
            barcode_field.send_keys("\n")
            time.sleep(5)

            quantity_field = wait.until(
                EC.element_to_be_clickable((By.ID, "quantityBarcode"))
            )
            quantity_field.clear()
            quantity_field.send_keys("20")
            quantity_field.send_keys("\n")
            time.sleep(5)

            # ==========================================
            # STEP 7: Click SAVE
            # ==========================================
            print("💾 Saving Sales Order...")

            save_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'SAVE')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
            save_btn.click()
            print("✅ Sales Order Saved Successfully.")

            time.sleep(2)

            # Screenshot Success
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Sales_Order_Success",
                attachment_type=allure.attachment_type.PNG
            )

        except Exception as e:
            print(f"❌ Error occurred: {e}")

            allure.attach(
                driver.get_screenshot_as_png(),
                name="Sales_Order_Error",
                attachment_type=allure.attachment_type.PNG
            )

            raise e
