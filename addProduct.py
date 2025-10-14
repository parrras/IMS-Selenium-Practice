import time
import random
import string
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- Initialize Chrome driver ---
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

# --- Navigate to login page ---
driver.get("https://grn.variantqa.himshang.com.np/#/login")

# --- LOGIN ---
wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[2]/input")
)).send_keys("Paras")

driver.find_element(By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[3]/input").send_keys("Ims@1234")
driver.find_element(By.XPATH, "//button[normalize-space(text())='Sign In']").click()

time.sleep(5)  # wait for dashboard to load

# --- Wait for dashboard load (no duplicate driver or sleep) ---
# noinspection PyBroadException
try:
    logout_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
    )
    # Click the Logout button
    logout_button.click()
    print("Logged out successfully.")

    ok_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and normalize-space(text())='OK']"))
    )
    ok_button.click()
    print("Clicked OK on the confirmation dialog.")

    time.sleep(5)
    driver.find_element(By.CLASS_NAME, "btn-auth").click()
    print("Clicked on re-login button.")
except:
    print("Logout button not found.")

# --- Hover over "Inventory Info" ---
try:
    inventory_info = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Inventory Info")))
except TimeoutException:
    try:
        inventory_info = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Inventory")))
    except TimeoutException:
        inventory_info = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Inventory Info')]"))
        )

ActionChains(driver).move_to_element(inventory_info).perform()
time.sleep(3)

# --- Click on "Product Master" ---
product_master = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Product Master")))
product_master.click()
time.sleep(3)

# --- Click "Add Product" dropdown ---
add_product_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='createDropdown']")))
add_product_button.click()
time.sleep(2)

# --- Click "Add Product" inside dropdown ---
second_add_product = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Add Product']")))
driver.execute_script("arguments[0].scrollIntoView(true);", second_add_product)
driver.execute_script("arguments[0].click();", second_add_product)
time.sleep(2)

# --- Select Item Group ---
item_group_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-icon[normalize-space(text())='open_in_new']")))
item_group_icon.click()
time.sleep(2)

main_group_input = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//input[@aria-autocomplete='list' and @type='text']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", main_group_input)
main_group_input.click()
main_group_input.send_keys("B")

body_care_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='BODY CARE']")))
driver.execute_script("arguments[0].scrollIntoView(true);", body_care_option)
body_care_option.click()

ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Ok']")))
driver.execute_script("arguments[0].scrollIntoView(true);", ok_button)
ok_button.click()
print("✅ BODY CARE selected successfully!")

# --- Function to generate random product name ---
def generate_random_name(length=5):
    letters_and_digits = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

# --- Prepare CSV to save product info ---
csv_file = 'products.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'HS Code', 'Stock Unit', 'Purchase Price', 'Sales Price', 'Barcode', 'Supplier'])

    # --- Add 5 random products ---
    for i in range(5):
        print(f"\n➡️ Adding product #{i+1}")

        # --- Generate product info ---
        random_product_name = generate_random_name()
        random_hs_code = str(random.randint(100000, 999999))
        stock_unit = "Bottle"
        purchase_price = random.randint(10, 500)
        sales_price = random.randint(purchase_price + 150, purchase_price + 200)
        barcode = f"1.{108 + i}"  # starting from 1.103
        supplier = "ABC SUPPLIER PVT. LTD."

        # --- Enter product details ---
        item_name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Item Name']")))
        item_name_input.clear()
        item_name_input.send_keys(random_product_name)
        time.sleep(1)

        hs_code_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter HS Code']")))
        hs_code_input.clear()
        hs_code_input.send_keys(random_hs_code)
        time.sleep(1)

        stock_unit_select = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='unit']")))
        Select(stock_unit_select).select_by_visible_text(stock_unit)
        time.sleep(1)

        purchase_price_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Purchase Price']")))
        purchase_price_input.clear()
        purchase_price_input.send_keys(str(purchase_price))

        sales_price_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0' and @type='number'][1]")))
        sales_price_input.clear()
        sales_price_input.send_keys(str(sales_price))

        # --- Supplier selection ---
        try:
            supplier_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter to select']")))
            driver.execute_script("arguments[0].click();", supplier_field)
            supplier_field.send_keys(Keys.ENTER)
            supplier_to_select = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//td[normalize-space(text())='ABC SUPPLIER PVT. LTD.']"))
            )
            ActionChains(driver).move_to_element(supplier_to_select).double_click(supplier_to_select).perform()
        except Exception as e:
            print("❌ Failed to select supplier:", e)

        # --- Save product ---
        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='save']")))
        save_button.click()
        time.sleep(5)

        # --- Handle JS alert ---
        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"⚡ Alert message: {alert.text}")
            alert.accept()
        except TimeoutException:
            pass

        print(f"✅ Added product: {random_product_name}, HS Code: {random_hs_code}, Barcode: {barcode}")

        # --- Save product info to CSV ---
        writer.writerow([random_product_name, random_hs_code, stock_unit, purchase_price, sales_price, barcode, supplier])

print("\n🎉 All 5 products added and saved to CSV successfully!")

# --- Now generate invoice from the CSV ---
barcodes = []
with open(csv_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        barcodes.append(row[5])  # barcode column

# --- Click Transactions button ---
transaction_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Transactions']")))
driver.execute_script("arguments[0].click();", transaction_button)
time.sleep(2)

# --- Hover over Purchase Transaction ---
# noinspection PyBroadException
try:
    purchase_transaction = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Transaction")))
except:
    purchase_transaction = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Purchase Transaction']")))

driver.execute_script("arguments[0].scrollIntoView(true);", purchase_transaction)
ActionChains(driver).move_to_element(purchase_transaction).pause(0.3).perform()
time.sleep(2)

# --- Click Purchase Invoice ---
purchase_invoice = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Invoice")))
driver.execute_script("arguments[0].scrollIntoView(true);", purchase_invoice)
purchase_invoice.click()
time.sleep(3)

# --- Enter random invoice number ---
invoice_number = str(random.randint(1000000, 9999999))
invoice_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='invoiceNO']")))
invoice_input.clear()
invoice_input.send_keys(invoice_number)

# --- Select Account ---
account_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='accountfield']")))
driver.execute_script("arguments[0].click();", account_field)
account_field.send_keys(Keys.ENTER)
abc_supplier = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='ABC SUPPLIER PVT. LTD.']")))
ActionChains(driver).move_to_element(abc_supplier).double_click(abc_supplier).perform()
time.sleep(2)

# --- Enter Barcodes and Quantities ---
for barcode in barcodes:
    barcode_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='barcodeField']")))
    barcode_field.clear()
    barcode_field.send_keys(barcode)
    barcode_field.send_keys(Keys.ENTER)
    time.sleep(1)

    quantity_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='quantityBarcode']")))
    quantity_field.clear()
    quantity_field.send_keys("20")
    quantity_field.send_keys(Keys.ENTER)
    time.sleep(1)
    print(f"✅ Added barcode {barcode} with quantity 20")

# --- Click Save for Invoice ---
save_invoice_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-info') and contains(text(),'SAVE')]")))
driver.execute_script("arguments[0].click();", save_invoice_button)

# --- Handle JS alert ---
try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print(f"⚡ Alert message: {alert.text}")
    alert.accept()
except TimeoutException:
    print("⚠️ No JS alert appeared after invoice save")

print("\n🎉 Invoice generated successfully from CSV!")

# Keep browser open for inspection
time.sleep(60)
driver.quit()
