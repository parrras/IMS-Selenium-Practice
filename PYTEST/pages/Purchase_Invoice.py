import time
import csv
import random
import allure
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Purchase Invoice")
class PurchaseInvoicePage:

    def __init__(self, driver, csv_file='Added_Products.csv'):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.csv_file = csv_file

    # noinspection PyBroadException
    @allure.step("Generate purchase invoice from CSV products")
    def generate_invoice(self):
        print("🚀 Starting Purchase Invoice generation...")

        # ✅ Step 1: Read barcodes dynamically from CSV
        print("📄 Reading barcodes from CSV file...")
        barcodes = []
        if not os.path.exists(self.csv_file):
            raise FileNotFoundError(f"❌ CSV file not found: {self.csv_file}")

        with open(self.csv_file, newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) > 5 and row[5].strip():  # Ensure valid barcode field
                    barcodes.append(row[5].strip())

        print(f"✅ Total barcodes found: {len(barcodes)}")

        if not barcodes:
            raise ValueError("❌ No barcodes found in CSV file!")

        wait = self.wait

        # ✅ Step 2: Navigate to Transactions → Purchase Invoice
        print("📂 Navigating to Transactions → Purchase Invoice...")
        transaction_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Transactions']"))
        )
        transaction_btn.click()
        time.sleep(1)

        try:
            purchase_transaction = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Transaction"))
            )
        except:
            purchase_transaction = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[normalize-space()='Purchase Transaction']")
                )
            )

        ActionChains(self.driver).move_to_element(purchase_transaction).pause(0.3).perform()
        time.sleep(2)

        purchase_invoice = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Invoice")))
        purchase_invoice.click()
        print("✅ Purchase Invoice page opened.")
        time.sleep(2)

        # ✅ Step 3: Enter invoice number
        print("🧾 Entering invoice number...")
        invoice_number = str(random.randint(1000000, 9999999))
        invoice_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='invoiceNO']")))
        invoice_input.clear()
        invoice_input.send_keys(invoice_number)
        print(f"✅ Invoice number entered: {invoice_number}")

        # ✅ Step 4: Select Sujata Vendor account
        print("🏢 Selecting Sujata Vendor account...")
        account_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='accountfield']")))
        account_field.click()
        account_field.send_keys(Keys.ENTER)

        sujata_ven = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Sujata Vendor']")))
        ActionChains(self.driver).move_to_element(sujata_ven).double_click(sujata_ven).perform()
        print("✅ Sujata Vendor selected.")
        time.sleep(2)

        # ✅ Step 5: Add each product dynamically by barcode/itemcode
        print("📦 Adding products from barcode list...")
        for barcode_value in barcodes:
            print(f"➡️ Adding product with barcode: {barcode_value}")
            barcode_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='barcodeField']")))
            barcode_field.clear()
            barcode_field.send_keys(barcode_value)
            barcode_field.send_keys(Keys.ENTER)
            time.sleep(2)

            quantity_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='quantityBarcode']")))
            quantity_field.clear()
            quantity_field.send_keys("20")
            quantity_field.send_keys(Keys.ENTER)
            time.sleep(1)

        print("✅ All products added successfully.")

        # ✅ Step 6: Save invoice
        print("💾 Saving the invoice...")
        save_invoice_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-info') and contains(text(),'SAVE')]"))
        )
        save_invoice_btn.click()

        # ✅ Step 7: Handle alert
        try:
            print("⏳ Waiting for alert confirmation...")
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print(f"✅ Alert handled successfully. Message: {alert_text}")
        except TimeoutException:
            print("⚠️ No alert appeared after saving invoice.")

        print("🎉 Purchase Invoice process completed successfully.")
