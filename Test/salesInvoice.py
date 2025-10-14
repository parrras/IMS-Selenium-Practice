from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Initialize Chrome driver
driver = webdriver.Chrome()
driver.maximize_window()

# Navigate to the site
driver.get("https://grn.variantqa.himshang.com.np/#/login")
wait = WebDriverWait(driver, 20)

# --- LOGIN ---
wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[2]/input"))).send_keys("Paras")
driver.find_element(By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[3]/input").send_keys("Ims@12345")
driver.find_element(By.XPATH, "//button[normalize-space(text())='Sign In']").click()

# Wait for dashboard to load
time.sleep(5)
# noinspection PyBroadException
try:
    logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]")))
    logout_button.click()
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, "btn-auth").click()
    time.sleep(5)
except:
    print("No logout button found")

# --- Click Transactions button ---
transaction_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Transactions']")))
driver.execute_script("arguments[0].scrollIntoView(true);", transaction_button)
driver.execute_script("arguments[0].click();", transaction_button)
print("✅ Clicked on 'Transactions' button.")
time.sleep(2)

# --- Hover over "Sales Transaction" ---
# noinspection PyBroadException
try:
    sales_transaction = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sales Transaction")))
except:
    # noinspection PyBroadException
    try:
        sales_transaction = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Sales Transaction")))
    except:
        sales_transaction = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Sales Transaction']")))

ActionChains(driver).move_to_element(sales_transaction).perform()
print("✅ Hovered over 'Sales Transaction'.")
time.sleep(2)

# --- Click on "Sales Invoice" ---
sales_tax_invoice = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sales Tax Invoice")))
driver.execute_script("arguments[0].scrollIntoView(true);", sales_tax_invoice)
driver.execute_script("arguments[0].click();", sales_tax_invoice)
print("✅ Clicked on 'Sales Invoice'.")
time.sleep(5)

# --- Fill the Sales Invoice form ---

# Fill Reference Number
ref_no_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='refnoInput']")))
ref_no_input.clear()
ref_no_input.send_keys("REF-002212")
print("✅ Filled Reference No: REF-002212")
time.sleep(1)

# Select Cost Center ("Test QA")
cost_center_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='costCenter']")))
select = Select(cost_center_dropdown)
select.select_by_value("2")  # value for 'Test QA'
print("✅ Selected Cost Center: Test QA (by value)")
time.sleep(1)

# Select Customer
customer_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='customerselectid']")))
customer_input.click()
print("✅ Clicked on Customer input field.")
time.sleep(1)
customer_input.send_keys(Keys.ENTER)
print("✅ Pressed ENTER to open customer list.")
time.sleep(3)

# Click on Bhavana Subedi
bhavana_customer = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Bhavana Subedi']")))
driver.execute_script("arguments[0].click();", bhavana_customer)
print("✅ Selected Customer: Bhavana Subedi")

print("🎉 Successfully filled Reference No, Cost Center, and Customer fields!")

# Double-click to select
actions = ActionChains(driver)
actions.double_click(bhavana_customer).perform()
print("✅ Double-clicked 'Bhavana Subedi.' account.")

# --- Enter Remarks ---
remarks_field = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='remarksid']")))
remarks_field.click()
remarks_field.send_keys("Good quality customer - regular buyer.")
print("✅ Entered remarks.")

# --- Enter Barcode ---
barcode_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='barcodeField']")))
barcode_field.click()
barcode_field.send_keys("135.62")
barcode_field.send_keys(Keys.ENTER)
print("✅ Entered barcode: 135.62 and pressed ENTER.")
time.sleep(3)

# Wait for the quantity field
quantity_field = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='alternateQty0']"))
)

# Scroll into view
driver.execute_script("arguments[0].scrollIntoView(true);", quantity_field)
time.sleep(1)

# Click, clear, and enter value 5
quantity_field.click()
time.sleep(0.5)
quantity_field.clear()
time.sleep(0.5)
quantity_field.send_keys("5")
time.sleep(0.5)
quantity_field.send_keys(Keys.ENTER)
print("✅ Quantity updated to 5 and Enter pressed.")
print("🎉 All fields filled successfully!")


# --- Click Save ---
save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'SAVE')]")))
driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
driver.execute_script("arguments[0].click();", save_button)
print("💾 Clicked Save button")

# --- Click Balance Amount Button ---
balance_amount_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Balance Amount']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", balance_amount_btn)
driver.execute_script("arguments[0].click();", balance_amount_btn)
print("💰 Clicked Balance Amount button.")
time.sleep(3)

# --- Click Add Button ---
add_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
driver.execute_script("arguments[0].click();", add_button)
print("➕ Clicked Add button.")
time.sleep(3)

# --- Click Final Save Button ---
final_save_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[@title='Save' and normalize-space(text())='SAVE [End]']")
    )
)
driver.execute_script("arguments[0].scrollIntoView(true);", final_save_button)
driver.execute_script("arguments[0].click();", final_save_button)
print("✅ Final SAVE [End] button clicked successfully!")

# --- Click Print Button ---
print_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Print']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", print_button)
driver.execute_script("arguments[0].click();", print_button)
print("🖨️ Print button clicked successfully!")

time.sleep(500)