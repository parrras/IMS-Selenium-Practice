from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

# ✅ Initialize Chrome driver (only once)
driver = webdriver.Chrome()
driver.set_window_size(1400, 900)  # 🪟 fixed window size for consistent element visibility
wait = WebDriverWait(driver,20)

# --- Navigate to the site ---
driver.get("https://grn.variantqa.himshang.com.np/#/login")

# --- LOGIN ---
wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[2]/input"))).send_keys("Paras")
driver.find_element(By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[3]/input").send_keys("Ims@12345")
driver.find_element(By.XPATH, "//button[normalize-space(text())='Sign In']").click()
print("✅ Logged in successfully.")

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

# --- Click Transactions button ---
transaction_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Transactions']"))
)
driver.execute_script("arguments[0].click();", transaction_button)
print("✅ Clicked on 'Transactions' button.")
time.sleep(2)

# --- Hover over "Purchase Transaction" ---
# noinspection PyBroadException
try:
    purchase_transaction = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Transaction"))
    )
except:
    # noinspection PyBroadException
    try:
        purchase_transaction = wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Purchase Transaction"))
        )
    except:
        purchase_transaction = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Purchase Transaction']"))
        )

# 🪄 FIXED: safer hover using scrollIntoView before hover
driver.execute_script("arguments[0].scrollIntoView(true);", purchase_transaction)
ActionChains(driver).move_to_element(purchase_transaction).pause(0.3).perform()
print("✅ Hovered over 'Purchase Transaction'.")
time.sleep(1)

# --- Click on "Purchase Invoice" ---
purchase_invoice = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Invoice"))
)
# 🪄 FIXED: ensure visibility before click to prevent intercept
driver.execute_script("arguments[0].scrollIntoView(true);", purchase_invoice)
wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Invoice"))).click()
print("✅ Clicked on 'Purchase Invoice'.")

# --- Enter Invoice Number ---
invoice_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='invoiceNO']")))
invoice_input.clear()
invoice_input.send_keys("1112233")
print("✅ Entered Invoice Number: 1112233")
time.sleep(1)

# --- Account field: focus and press Enter ---
account_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='accountfield']")))
driver.execute_script("arguments[0].click();", account_field)
print("✅ Clicked Account field using JS.")
account_field.send_keys(Keys.ENTER)
print("⏎ Pressed Enter to open account list.")
time.sleep(1)

# --- Select 'ABC SUPPLIER PVT. LTD.' ---
abc_supplier = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='ABC SUPPLIER PVT. LTD.']")))
actions = ActionChains(driver)
actions.move_to_element(abc_supplier).double_click(abc_supplier).perform()
print("✅ Selected 'ABC SUPPLIER PVT. LTD.' account.")
time.sleep(1)

# --- Enter Barcode ---
barcode_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='barcodeField']")))
barcode_field.clear()
barcode_field.send_keys("130.67")
barcode_field.send_keys(Keys.ENTER)
print("✅ Entered barcode: 130.67 and added product.")
time.sleep(2)

# --- Update Quantity ---
quantity_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='quantityBarcode']")))
quantity_field.clear()
quantity_field.send_keys("20")
print("✅ Updated quantity to 20")

# --- Click Save button ---
save_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-info') and contains(text(),'SAVE')]"))
)
driver.execute_script("arguments[0].click();", save_button)
print("💾 Clicked Save button")

# --- Handle JS alert ---
try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print(f"⚡ Alert message: {alert.text}")
    alert.accept()
    print("✅ Alert accepted successfully!")
except TimeoutException:
    print("⚠️ No JS alert appeared after save")


time.sleep(400)  # Wait to observe result

