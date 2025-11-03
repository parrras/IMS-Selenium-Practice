import time
import csv
import random
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@allure.feature("Sales Invoice")
class SalesInvoicePage:

    def __init__(self, driver, csv_file='Added_Products.csv'):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.csv_file = csv_file

    @allure.step("Generate sales invoice for 5 products from CSV")
    def generate_sales_invoice(self):
        # --- Read first 5 barcodes from CSV ---
        barcodes = []
        with open(self.csv_file, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for i, row in enumerate(reader):
                if i >= 5:  # only take 5 products
                    break
                barcodes.append(row[5])

        wait = self.wait

        # --- Navigate to Transactions → Sales Transaction → Sales Tax Invoice ---
        transaction_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Transactions']"))
        )
        self.driver.execute_script("arguments[0].click();", transaction_btn)
        print("✅ Clicked on 'Transactions'")

        try:
            sales_transaction = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sales Transaction")))
        except:
            sales_transaction = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Sales Transaction']"))
            )

        ActionChains(self.driver).move_to_element(sales_transaction).perform()
        time.sleep(1)

        sales_invoice = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sales Tax Invoice")))
        self.driver.execute_script("arguments[0].click();", sales_invoice)
        print("✅ Opened 'Sales Tax Invoice' page.")
        time.sleep(4)

        # --- Fill Reference Number ---
        ref_no_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='refnoInput']")))
        ref_no_input.clear()
        ref_no_input.send_keys(f"REF-{random.randint(1000, 9999)}")
        print("✅ Reference number added.")

        # --- Select Customer ---
        customer_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='customerselectid']")))
        customer_input.click()
        customer_input.send_keys(Keys.ENTER)
        time.sleep(2)
        customer = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Carti']")))
        ActionChains(self.driver).move_to_element(customer).double_click(customer).perform()
        print("✅ Customer 'Carti' selected.")
        time.sleep(3)

        # --- Enter Remarks ---
        remarks_field = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='remarksid']")))
        remarks_field.click()
        remarks_field.send_keys("Regular customer.")
        print("✅ Remarks entered.")
        time.sleep(6)
        # --- Add 5 Products by Barcode ---
        for barcode in barcodes:
            barcode_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='barcodeField']")))
            barcode_field.clear()
            barcode_field.send_keys(barcode)
            barcode_field.send_keys(Keys.ENTER)
            print(f"📦 Added product with barcode: {barcode}")
            time.sleep(3)

            # Quantity field (dynamic)
            quantity_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='quantityBarcode']")))
            quantity_field.clear()
            quantity_field.send_keys("10")
            quantity_field.send_keys(Keys.ENTER)

        time.sleep(5)

        # --- Click SAVE ---
        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'SAVE')]")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        self.driver.execute_script("arguments[0].click();", save_button)
        print("💾 Clicked Save button.")
        time.sleep(2)

        # --- Click Balance Amount Button ---
        balance_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Balance Amount']")))
        self.driver.execute_script("arguments[0].click();", balance_btn)
        print("💰 Clicked Balance Amount button.")
        time.sleep(2)

        # --- Click Add Button ---
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']")))
        self.driver.execute_script("arguments[0].click();", add_btn)
        print("➕ Clicked Add button.")
        time.sleep(2)

        # --- Final Save [End] ---
        final_save_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@title='Save' and normalize-space(text())='SAVE [End]']")
            )
        )
        self.driver.execute_script("arguments[0].click();", final_save_btn)
        print("✅ Final SAVE [End] clicked.")
        time.sleep(2)

        # --- Print Button ---
        try:
            print_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Print']")))
            self.driver.execute_script("arguments[0].click();", print_btn)
            print("🖨️ Print button clicked successfully.")
        except TimeoutException:
            print("⚠️ Print button not found — continuing.")

        allure.attach("✅ Sales invoice generated for 5 products", name="Sales Invoice", attachment_type=allure.attachment_type.TEXT)
