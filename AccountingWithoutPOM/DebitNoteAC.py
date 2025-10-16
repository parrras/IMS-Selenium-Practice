import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# --- Initialize Chrome driver ---
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)

# --- Navigate to login page ---
driver.get("https://redmiims.webredirect.himshang.com.np/#/login")

# --- LOGIN ---
wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[2]/input")
)).send_keys("Paras")

driver.find_element(By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[3]/input").send_keys("Ims@1234")
driver.find_element(By.XPATH, "//button[normalize-space(text())='Sign In']").click()
time.sleep(5)  # wait for dashboard to load

# --- Handle duplicate logout if exists ---
# noinspection PyBroadException
try:
    logout_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
    )
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

# --- Click Accounting Module button ---
accounting_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Accounting Module']"))
)
accounting_button.click()
print("✅ Clicked Accounting Module")
time.sleep(10)  # wait for new tab to open

# --- Switch to new tab opened by Accounting Module ---
original_tab = driver.current_window_handle
for handle in driver.window_handles:
    if handle != original_tab:
        driver.switch_to.window(handle)
        print("✅ Switched to Accounting Module tab")
        break
time.sleep(10)  # wait for Accounting Module to load

# --- Click Transactions ---
transactions = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Transactions']"))
)
transactions.click()
print("✅ Clicked Transactions in Accounting Module")
time.sleep(5)

# --- Hover over Voucher Entries ---
# noinspection PyBroadException
try:
    voucher_entries = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Voucher Entries")))
except:
    # noinspection PyBroadException
    try:
        voucher_entries = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Voucher Entries")))
    except:
        voucher_entries = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Voucher Entries']"))
        )

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", voucher_entries)
actions.move_to_element(voucher_entries).pause(0.5).perform()
print("✅ Hovered Voucher Entries")
time.sleep(5)

# --- Click Debit Note A/C ---
debit_note = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Debit Note - AC Base"))
)
debit_note.click()
print("✅ Clicked Debit Note A/C")
time.sleep(5)

# --- Step 4: Enter Ref Number & Remarks ---
ref_number_field_dr = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='refno']")))
ref_number_field_dr.clear()
ref_number_field_dr.send_keys("REF-10019800")
print("✅ Entered Ref Number")
time.sleep(5)

remarks_field_dr = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='REMARKS']")))
remarks_field_dr.click()
remarks_field_dr.send_keys("This is a test.")
print("✅ Entered Remarks")
time.sleep(5)

# --- Step 5: Debit Account ---
debit_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='press ENTER to Select A/C']")))
driver.execute_script("arguments[0].click();", debit_input)
debit_input.send_keys(Keys.ENTER)
debit_ac1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='TheTestCustom']")))
actions.move_to_element(debit_ac1).double_click(debit_ac1).perform()
print("✅ Selected debit Account")
time.sleep(5)

# --- Step 5: Ledger Account 1 ---
ledger_input_dr = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_0']")))
driver.execute_script("arguments[0].click();", ledger_input_dr)
ledger_input_dr.send_keys(Keys.ENTER)
ledger_ac_dr = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Siddhartha Bank']")))
actions.move_to_element(ledger_ac_dr).double_click(ledger_ac_dr).perform()
print("✅ Selected Ledger Account 1")
time.sleep(5)

# --- Step 6: Amount 1 ---
amount_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='CrAmtInput_0']")))
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amount_field)
amount_field.send_keys("200000")
print("✅ Entered amount: 200000")
time.sleep(5)

# --- Step 7: Narration 1 ---
narration_field_dr = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='narration_0']")))
narration_field_dr.send_keys("Test Narration\n")
print("✅ Entered Narration 1")
time.sleep(5)

# --- Step 8: Ledger Account 2 ---
ledger_input_dr1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_1']")))
driver.execute_script("arguments[0].click();", ledger_input_dr1)
ledger_input_dr1.send_keys(Keys.ENTER)
ledger_ac_dr1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Test Account']")))
actions.move_to_element(ledger_ac_dr1).double_click(ledger_ac_dr1).perform()
print("✅ Selected Ledger Account 2")
time.sleep(5)

# --- Step 9: Amount 2 ---
amount_field1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='CrAmtInput_1']")))
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amount_field1)
amount_field1.send_keys("500000")
print("✅ Entered amount: 500000")
time.sleep(5)

# --- Step 10: Narration 2 ---
narration_field_dr1 = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='narration_1']")))
narration_field_dr1.send_keys("Test Narration\n")
print("✅ Entered Narration 2")
time.sleep(5)

# --- Step 11: Save & Confirm Debit Note ---
save_button_dnote = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F6 SAVE']"))
)
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button_dnote)
driver.execute_script("arguments[0].click();", save_button_dnote)
print("✅ Clicked Save button")
time.sleep(5)

yes_button_dnote = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']")))
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", yes_button_dnote)
driver.execute_script("arguments[0].click()", yes_button_dnote)
print("✅ Clicked Yes on confirmation modal")
time.sleep(5)

cancel_button_dnote = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cancel_button_dnote)
driver.execute_script("arguments[0].click();", cancel_button_dnote)
print("✅ Clicked Cancel on confirmation modal")
time.sleep(5)

print("✅ Debit Note automation completed successfully!")

time.sleep(500)
