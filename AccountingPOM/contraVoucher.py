import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import date


# noinspection PyBroadException
class ContraVoucherPage:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 25)
        self.actions = ActionChains(self.driver)

    # --- Login ---
    def open(self):
        self.driver.get("https://redmiims.webredirect.himshang.com.np/#/login")

    def enter_username(self, username):
        username_field = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[2]/input")
            )
        )
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.driver.find_element(
            By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[3]/input"
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_signin(self):
        signin_button = self.driver.find_element(
            By.XPATH, "//button[normalize-space(text())='Sign In']"
        )
        signin_button.click()

    # --- Handle duplicate logout ---
    def handle_duplicate_logout(self):
        try:
            logout_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
            )
            logout_button.click()
            print("✅ Logged out from duplicate session")
            ok_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='OK']"))
            )
            ok_button.click()
            time.sleep(2)
            re_login_btn = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-auth"))
            )
            re_login_btn.click()
            print("✅ Clicked re-login button")
        except Exception:
            print("⚠ No duplicate session found")

    # --- Accounting Module ---
    def open_accounting_module(self):
        try:
            accounting_module = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Accounting Module')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", accounting_module)
            self.driver.execute_script("arguments[0].click();", accounting_module)
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            print("✅ Clicked Accounting Module")
            time.sleep(5)
        except Exception as e:
            print("❌ Could not click Accounting Module:", e)

    # --- Contra Voucher ---
    def open_contra_voucher(self):
        try:
            # --- Step 1: Click Transactions ---
            transaction_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Transactions')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", transaction_btn)
            self.driver.execute_script("arguments[0].click();", transaction_btn)
            print("✅ Clicked 'Transactions'")
            time.sleep(2)

            # --- Step 2: Hover over Voucher Entries ---
            try:
                voucher_entries = self.wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Voucher Entries"))
                )
            except:
                try:
                    voucher_entries = self.wait.until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Voucher Entries"))
                    )
                except:
                    voucher_entries = self.wait.until(
                        EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Voucher Entries']"))
                    )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", voucher_entries)
            self.actions.move_to_element(voucher_entries).pause(0.5).perform()
            print("✅ Hovered over 'Voucher Entries'")
            time.sleep(1)

            # --- Step 3: Click Contra Voucher ---
            contra_voucher = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Contra Voucher"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", contra_voucher)
            self.driver.execute_script("arguments[0].click();", contra_voucher)
            print("✅ Clicked on 'Contra Voucher'")
            time.sleep(3)

            # Step 4: Enter Ref Number & Remarks
            ref_number_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='refno']")))
            ref_number_field.clear()
            ref_number_field.send_keys("REF-9900")
            print("✅ Entered Ref Number")
            time.sleep(1)

            remarks_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='REMARKS']")))
            remarks_field.click()
            remarks_field.send_keys("This is a test.")
            print("✅ Entered Remarks")
            time.sleep(1)

            # Step 5: Ledger Account 1
            ledger_input1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_0']")))
            self.driver.execute_script("arguments[0].click();", ledger_input1)
            ledger_input1.send_keys(Keys.ENTER)
            ledger_ac1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='PETTY CASH A/C']")))
            self.actions.move_to_element(ledger_ac1).double_click(ledger_ac1).perform()
            print("✅ Selected Ledger Account 1")
            time.sleep(1)

            # Debit Amount
            debit_field1 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='DrAmtInput_0']")))
            debit_field1.clear()
            debit_field1.send_keys("1000\n")
            print("✅ Entered Debit Amount")
            time.sleep(1)

            # Narration 1
            narration_field1 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='narration_0']")))
            narration_field1.send_keys("Test Narration\n")
            print("✅ Entered Narration 1")
            time.sleep(1)

            # TRN Mode 1
            trn_mode1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='transactionType_0']")))
            Select(trn_mode1).select_by_visible_text("Cheque")
            print("✅ Selected TRN Mode: Cheque")

            # Cheque Number & Date 1
            cheque1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ChequeNo_0']")))
            cheque1.click()
            cheque1.send_keys("CHQ-" + str(int(time.time()) % 10000))
            cheque1.send_keys(Keys.TAB)
            today_date = date.today().strftime("%m%d%Y")
            self.actions.send_keys(today_date).perform()
            print(f"✅ Entered Cheque Number and Date: {today_date[:2]}/{today_date[2:4]}/{today_date[4:]}")
            time.sleep(1)

            # Handle Invalid Date Alert
            try:
                alert_ok = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='OK']"))
                )
                alert_ok.click()
                print("✅ Closed 'Invalid Transaction Date' popup")
            except Exception:
                pass

            # Step 6: Ledger Account 2
            ledger_input2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_1']")))
            self.driver.execute_script("arguments[0].click();", ledger_input2)
            ledger_input2.send_keys(Keys.ENTER)
            ledger_ac2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='CASH IN HAND A/C']")))
            self.actions.move_to_element(ledger_ac2).double_click(ledger_ac2).perform()
            print("✅ Selected Ledger Account 2")
            time.sleep(1)

            # Credit Amount
            credit_field2 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='CrAmtInput_1']")))
            credit_field2.clear()
            credit_field2.send_keys("1000\n")
            print("✅ Entered Credit Amount")
            time.sleep(1)

            # Narration 2
            narration_field2 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='narration_1']")))
            narration_field2.send_keys("Test Narration\n")
            print("✅ Entered Narration 2")
            time.sleep(1)

            # TRN Mode 2
            trn_mode2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='transactionType_1']")))
            Select(trn_mode2).select_by_visible_text("Cheque")
            print("✅ Selected TRN Mode 2: Cheque")

            # Cheque Number & Date 2
            cheque2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ChequeNo_1']")))
            cheque2.click()
            cheque2.send_keys("CHQ-" + str(int(time.time()) % 10000))
            cheque2.send_keys(Keys.TAB)
            self.actions.send_keys(today_date).perform()
            print(f"✅ Entered Cheque Number and Date 2: {today_date[:2]}/{today_date[2:4]}/{today_date[4:]}")
            time.sleep(1)

            # Handle Invalid Date Alert 2
            try:
                alert_ok2 = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='OK']"))
                )
                alert_ok2.click()
                print("✅ Closed 'Invalid Transaction Date' popup 2")
            except Exception:
                pass

            # Step 7: Save & Confirm Contra Voucher
            save_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F6 SAVE']")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button)
            self.driver.execute_script("arguments[0].click();", save_button)
            print("✅ Clicked Save button")
            time.sleep(1)

            yes_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", yes_button)
            self.driver.execute_script("arguments[0].click();", yes_button)
            print("✅ Clicked Yes on confirmation modal")
            time.sleep(1)

            cancel_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cancel_button)
            self.driver.execute_script("arguments[0].click();", cancel_button)
            print("✅ Clicked Cancel on confirmation modal")

            # Keep browser open to observe
            time.sleep(500)

        except Exception as e:
            print("❌ Error in Contra Voucher:", e)
