import time
import csv
import random
import allure
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

    @allure.step("Generate purchase invoice from CSV products")
    def generate_invoice(self):
        # Read barcodes from CSV
        barcodes = []
        with open(self.csv_file, newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                barcodes.append(row[5])

        wait = self.wait

        # Navigate to Transactions → Purchase Invoice
        transaction_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Transactions']"))
        )
        transaction_btn.click()
        time.sleep(1)

        try:
            purchase_transaction = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Transaction")))
        except:
            purchase_transaction = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Purchase Transaction']")))

        ActionChains(self.driver).move_to_element(purchase_transaction).pause(0.3).perform()
        time.sleep(2)

        purchase_invoice = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Invoice")))
        purchase_invoice.click()
        time.sleep(2)

        # Enter invoice number
        invoice_number = str(random.randint(1000000, 9999999))
        invoice_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='invoiceNO']")))
        invoice_input.clear()
        invoice_input.send_keys(invoice_number)

        # Select account
        account_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='accountfield']")))
        account_field.click()
        account_field.send_keys(Keys.ENTER)

        sujata_ven = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='Sujata Vendor']"))
        )
        ActionChains(self.driver).move_to_element(sujata_ven).double_click(sujata_ven).perform()
        time.sleep(2)

        # Add all products by barcode
        for barcode_value in barcodes:
            barcode_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='barcodeField']")))
            barcode_field.clear()
            barcode_field.send_keys(barcode_value)
            barcode_field.send_keys(Keys.ENTER)
            time.sleep(3)

            quantity_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='quantityBarcode']")))
            quantity_field.clear()
            quantity_field.send_keys("20")
            quantity_field.send_keys(Keys.ENTER)


        time.sleep(5)
        # Save invoice
        save_invoice_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-info') and contains(text(),'SAVE')]"))
        )
        save_invoice_btn.click()

        # Handle alert
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("✅ Invoice saved successfully.")
        except TimeoutException:
            print("⚠️ No alert after saving invoice")
