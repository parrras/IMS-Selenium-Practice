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
time.sleep(10)  #wait for Accounting Module to load

# --- Click Transactions ---
transactions = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Transactions']"))
)
transactions.click()
print("✅ Clicked Transactions in Accounting Module")

# --- Hover over Voucher Entries ---
# noinspection PyBroadException
try:
    voucher_entries = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voucher Entries"))
    )
except:
    # noinspection PyBroadException
    try:
        voucher_entries = wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Voucher Entries"))
        )
    except:
        voucher_entries = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Voucher Entries']"))
        )

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", voucher_entries)
ActionChains(driver).move_to_element(voucher_entries).pause(0.5).perform()
print("✅ Hovered Voucher Entries")
time.sleep(5)

# --- Click Contra Voucher ---
contra_voucher = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Contra Voucher"))
)
contra_voucher.click()
print("✅ Clicked Contra Voucher")
time.sleep(5)

# --- Enter Ref Number ---
ref_number_field = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='refno']"))
)
ref_number_field.clear()
ref_number_field.send_keys("REF-9999")
print("✅ Entered Ref Number")
time.sleep(5)

# --- Enter Remarks ---
remarks_field = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@name='REMARKS']"))
)
remarks_field.click()
remarks_field.send_keys("This is a test.")
print("✅ Entered Remarks")
time.sleep(5)

# --- Ledger Account Selection ---
try:
    ledger_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_0']")))
    driver.execute_script("arguments[0].click();", ledger_input)
    ledger_input.send_keys(Keys.ENTER)
    ledger_ac_to_select = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@title='PETTY CASH A/C']"))
    )
    time.sleep(5)
    ActionChains(driver).move_to_element(ledger_ac_to_select).double_click(ledger_ac_to_select).perform()
except Exception as e:
    print("❌ Failed to select ledger ac:", e)
time.sleep(5)

# --- Enter Debit Amount ---
debit_field = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='DrAmtInput_0']"))
)
debit_field.clear()
debit_field.send_keys("1000")
debit_field.send_keys("\n")  # press enter
print("✅ Entered Debit Amount")
time.sleep(5)

# --- Enter Narration ---
narration_field = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='narration_0']"))
)
narration_field.send_keys("Test Narration")
narration_field.send_keys("\n")
print("✅ Entered Narration")
time.sleep(5)

# --- Select TRN Mode (Cheque) ---
try:
    trn_mode_dropdown = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//select[@id='transactionType_0']"))
    )
    select = Select(trn_mode_dropdown)
    select.select_by_visible_text("Cheque")
    print("✅ Selected TRN Mode: Cheque")
except Exception as e:
    print("❌ Failed to select TRN mode:", e)

time.sleep(2)

# --- Enter Cheque Number ---
try:
    cheque_number_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='ChequeNo_0']"))
    )
    cheque_number_field.click()
    cheque_number_field.send_keys("CHQ-" + str(int(time.time()) % 10000))  # random cheque no
    cheque_number_field.send_keys(Keys.TAB)  # move to the date field
    print("✅ Entered Cheque Number and moved to Date field")
except Exception as e:
    print("❌ Failed to enter cheque number:", e)

time.sleep(2)

# --- Enter Today's Date (mmddyyyy format) ---
try:
    from datetime import date
    today = date.today()
    formatted_date = today.strftime("%m%d%Y")

    # directly type date after tab from number field
    actions = ActionChains(driver)
    actions.send_keys(formatted_date)
    actions.perform()

    print(f"✅ Entered Date: {formatted_date[:2]}/{formatted_date[2:4]}/{formatted_date[4:]}")
except Exception as e:
    print("❌ Failed to enter date:", e)
time.sleep(3)

# --- Handle "Invalid Transaction Date" Alert ---
# noinspection PyBroadException
try:
    error_ok_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='OK']"))
    )
    print("⚠️ Detected 'Invalid Transaction Date' alert.")
    error_ok_button.click()
    print("✅ Clicked OK on 'Invalid Transaction Date' popup.")
    time.sleep(2)
except Exception:
    print("✅ No 'Invalid Transaction Date' popup appeared.")


# --- Ledger Account Selection 2 ---
try:
    ledger_input1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_1']")))
    driver.execute_script("arguments[0].click();", ledger_input1)
    ledger_input1.send_keys(Keys.ENTER)
    ledger_ac_to_select1 = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@title='CASH IN HAND A/C']"))
    )
    time.sleep(5)
    ActionChains(driver).move_to_element(ledger_ac_to_select1).double_click(ledger_ac_to_select1).perform()
except Exception as e:
    print("❌ Failed to select ledger ac:", e)
time.sleep(5)

# --- Enter Credit Amount ---
credit_field = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='CrAmtInput_1']"))
)
credit_field.clear()
credit_field.send_keys("1000")
credit_field.send_keys("\n")  # press enter
print("✅ Entered Credit Amount")
time.sleep(5)

# --- Enter Narration2 ---
narration_field1 = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='narration_1']"))
)
narration_field1.send_keys("Test Narration")
narration_field1.send_keys("\n")
print("✅ Entered Narration1")
time.sleep(5)

# --- Select TRN Mode (Cheque) ---
try:
    trn_mode_dropdown1 = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//select[@id='transactionType_1']"))
    )
    select = Select(trn_mode_dropdown1)
    select.select_by_visible_text("Cheque")
    print("✅ Selected TRN Mode: Cheque")
except Exception as e:
    print("❌ Failed to select TRN mode:", e)

time.sleep(2)

# --- Enter Cheque Number ---
try:
    cheque_number_field1 = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='ChequeNo_1']"))
    )
    cheque_number_field1.click()
    cheque_number_field1.send_keys("CHQ-" + str(int(time.time()) % 10000))  # random cheque no
    cheque_number_field1.send_keys(Keys.TAB)  # move to the date field
    print("✅ Entered Cheque Number and moved to Date field")
except Exception as e:
    print("❌ Failed to enter cheque number:", e)

time.sleep(2)

# --- Enter Today's Date (mmddyyyy format) ---
try:
    from datetime import date
    today1 = date.today()
    formatted_date1 = today1.strftime("%m%d%Y")

    # directly type date after tab from number field
    actions = ActionChains(driver)
    actions.send_keys(formatted_date1)
    actions.perform()

    print(f"✅ Entered Date: {formatted_date1[:2]}/{formatted_date1[2:4]}/{formatted_date1[4:]}")
except Exception as e:
    print("❌ Failed to enter date:", e)
time.sleep(3)

# --- Handle "Invalid Transaction Date" Alert ---
# noinspection PyBroadException
try:
    error_ok_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='OK']"))
    )
    print("⚠️ Detected 'Invalid Transaction Date' alert.")
    error_ok_button.click()
    print("✅ Clicked OK on 'Invalid Transaction Date' popup.")
    time.sleep(2)
except Exception:
    print("✅ No 'Invalid Transaction Date' popup appeared.")

# --- Click Save button ---
save_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F6 SAVE']"))
)
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button)
driver.execute_script("arguments[0].click();", save_button)
print("✅ Clicked Save button")
time.sleep(3)

# --- Click 'Yes' on confirmation modal ---
yes_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']"))
)
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", yes_button)
driver.execute_script("arguments[0].click();", yes_button)
print("✅ Clicked Yes on confirmation modal")
time.sleep(3)

# --- Click 'Print' on confirmation modal ---
print_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Print']"))
)
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", print_button)
driver.execute_script("arguments[0].click();", print_button)
print("✅ Clicked Print on confirmation modal")

time.sleep(500)


