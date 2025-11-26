import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@allure.feature("Debit Note Creation")
class DebitNotePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.actions = ActionChains(driver)

    @allure.step("Create Debit Note Entry")
    def create_debit_note(self):
        driver = self.driver
        wait = self.wait
        actions = self.actions

        print("🚀 Starting Debit Note creation process...")

        try:
            # --- Navigate to Transactions → Purchase Transaction → Debit Note (Purchase Return) ---
            transaction_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Transactions']"))
            )
            driver.execute_script("arguments[0].click();", transaction_btn)
            print("✅ Clicked on 'Transactions'")

            try:
                purchase_transaction = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Transaction")))
            except:
                purchase_transaction = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Purchase Transaction']"))
                )

            actions.move_to_element(purchase_transaction).perform()
            time.sleep(1)

            debit_note = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Debit Note (Purchase Return)")))
            driver.execute_script("arguments[0].click();", debit_note)
            print("✅ Opened 'Debit Note (Purchase Return)' page.")
            time.sleep(4)

            # --- Step 1: Enter Reference PI Number ---
            ref_pi_field = wait.until(EC.element_to_be_clickable((By.ID, "invoiceNO")))
            driver.execute_script("arguments[0].scrollIntoView(true);", ref_pi_field)
            ref_pi_field.click()
            ref_pi_field.send_keys("REF12345")
            print("✅ Entered Reference PI Number")
            time.sleep(1)

            # --- Step 2: Enter Supplier Bill No ---
            supp_bill_field = wait.until(EC.element_to_be_clickable((By.ID, "suppBillNo")))
            driver.execute_script("arguments[0].scrollIntoView(true);", supp_bill_field)
            supp_bill_field.click()
            supp_bill_field.send_keys("SUPP98765")
            print("✅ Entered Supplier Bill Number")
            time.sleep(1)

            # --- Step 3: Select Return Mode ---
            return_mode = wait.until(EC.element_to_be_clickable((By.ID, "paymentTerms")))
            driver.execute_script("arguments[0].scrollIntoView(true);", return_mode)
            return_mode.click()
            return_mode_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//option[@value='cash']")))
            return_mode_option.click()
            print("✅ Selected Return Mode: Cash")
            time.sleep(1)

            # --- Step 4: Select Supplier ---
            supplier_input = wait.until(EC.element_to_be_clickable((By.ID, "customerselectid")))
            driver.execute_script("arguments[0].scrollIntoView(true);", supplier_input)
            supplier_input.click()
            supplier_input.send_keys("\n")
            time.sleep(2)

            supplier_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Sujata Vendor']")))
            actions.double_click(supplier_option).perform()
            print("✅ Selected Supplier: Sujata Vendor")
            time.sleep(1)

            # --- Step 5: Enter Remarks ---
            remarks_field = wait.until(EC.element_to_be_clickable((By.ID, "remarksid")))
            driver.execute_script("arguments[0].scrollIntoView(true);", remarks_field)
            remarks_field.clear()
            remarks_field.send_keys("Debit note created for returned goods.")
            print("✅ Remarks entered")
            time.sleep(1)

            # --- Step 6: Add Barcodes and Quantities ---
            barcodes = ["1.3", "14.2", "14.3"]
            quantity = "20"
            for barcode in barcodes:
                barcode_field = wait.until(EC.element_to_be_clickable((By.ID, "barcodeField")))
                driver.execute_script("arguments[0].scrollIntoView(true);", barcode_field)
                barcode_field.click()
                barcode_field.clear()
                barcode_field.send_keys(barcode)
                actions.send_keys("\n").perform()
                time.sleep(1)

                quantity_field = wait.until(EC.element_to_be_clickable((By.ID, "quantityBarcode")))
                driver.execute_script("arguments[0].scrollIntoView(true);", quantity_field)
                quantity_field.click()
                quantity_field.clear()
                quantity_field.send_keys(quantity)
                actions.send_keys("\n").perform()
                time.sleep(1)

                print(f"✅ Added barcode {barcode} with quantity {quantity}")

            # --- Step 7: Click SAVE ---
            save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'SAVE')]")))
            driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
            save_button.click()
            print("✅ Clicked SAVE successfully")
            time.sleep(2)

            # ✅ Step 7: Handle alert
            try:
                print("⏳ Waiting for alert confirmation...")
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                print(f"✅ Alert handled successfully. Message: {alert_text}")
            except TimeoutException: (
                    print("⚠️ No alert appeared after saving invoice."))

            # --- Step 8: Attach screenshot to Allure ---
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, name="Debit_Note_Screenshot", attachment_type=allure.attachment_type.PNG)
            print("📸 Screenshot attached for Allure")

        except TimeoutException:
            print("⚠️ Timeout waiting for element while creating Debit Note")
            raise
        except Exception as e:
            print(f"❌ Error while creating Debit Note: {e}")
            raise
