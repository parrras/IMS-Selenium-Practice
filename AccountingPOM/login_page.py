import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
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
            EC.presence_of_element_located((By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[2]/input"))
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

    # noinspection PyBroadException
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

    # --- Journal Voucher ---
    # noinspection PyBroadException
    def open_journal_voucher(self,):
        # Step 1: Click Transactions
        try:
            transaction_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Transactions')]"))
            )
            self.driver.execute_script("arguments[0].click();", transaction_btn)
            print("✅ Clicked 'Transactions'")
            time.sleep(2)
        except Exception as e:
            print("❌ Couldn't click 'Transactions':", e)
            return

        # Step 2: Hover over Voucher Entries
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
        self.actions.move_to_element(voucher_entries).pause(0.3).perform()
        print("✅ Hovered over 'Voucher Entries'")
        time.sleep(1)

        # Step 3: Click Journal Voucher
        try:
            journal_voucher = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Journal Voucher"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", journal_voucher)
            journal_voucher.click()
            print("✅ Clicked on 'Journal Voucher'")
            time.sleep(3)  # wait for form to render
        except Exception as e:
            print("❌ Could not click 'Journal Voucher':", e)
            return

        try:
            # Step 1: Ref Number
            ref_number_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='refno']"))
            )
            ref_number_field.clear()
            ref_number_field.send_keys("REF12345")
            print("✅ Entered Ref Number")
            time.sleep(2)

            # Step 2: Remarks
            remarks_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='REMARKS']"))
            )
            remarks_field.click()
            remarks_field.send_keys("This is a test remark.")
            print("✅ Entered Remarks")
            time.sleep(2)

            # Step 3: Ledger Account Selection
            try:
                ledger_input = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_0']"))
                )
                self.driver.execute_script("arguments[0].click();", ledger_input)
                ledger_input.send_keys(Keys.ENTER)
                ledger_ac_to_select = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@title='vendormastest']"))
                )
                time.sleep(2)
                self.actions.move_to_element(ledger_ac_to_select).double_click(ledger_ac_to_select).perform()
                print("✅ Selected Ledger Account")
            except Exception as e:
                print("❌ Failed to select ledger account:", e)
            time.sleep(2)

            # Step 4: Debit Amount
            debit_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='DrAmtInput_0']"))
            )
            debit_field.clear()
            debit_field.send_keys("1000")
            debit_field.send_keys("\n")  # press enter
            print("✅ Entered Debit Amount")
            time.sleep(2)

            # Step 5: Narration
            narration_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='narration_0']"))
            )
            narration_field.send_keys("Test Narration")
            narration_field.send_keys("\n")
            print("✅ Entered Narration")


            # Step 6: 2nd Ledger Account Selection
            try:
                ledger_input2 = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_1']"))
                )
                self.driver.execute_script("arguments[0].click();", ledger_input2)
                ledger_input2.send_keys(Keys.ENTER)
                ledger_ac_to_select2 = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@title='TheTestCustom']"))
                )
                time.sleep(2)
                self.actions.move_to_element(ledger_ac_to_select2).double_click(ledger_ac_to_select2).perform()
                print("✅ Selected Ledger Account")
            except Exception as e:
                print("❌ Failed to select ledger account:", e)
            time.sleep(2)

            # Step 7: Credit Amount
            credit_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='CrAmtInput_1']"))
            )
            credit_field.clear()
            credit_field.send_keys("1000")
            credit_field.send_keys("\n")  # press enter
            print("✅ Entered Credit Amount")

            # Step 8: 2nd Narration
            narration_field1 = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='narration_1']"))
            )
            narration_field1.send_keys("Test Narration")
            narration_field1.send_keys("\n")
            print("✅ Entered Narration1")

        except Exception as e:
            print("❌ Error filling Journal Voucher fields:", e)

        try:
            # --- Click Save button ---
            save_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F6 SAVE']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button)
            self.driver.execute_script("arguments[0].click();", save_button)
            print("✅ Clicked Save button")
            time.sleep(3)

            # --- Click 'Yes' on confirmation modal ---
            yes_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", yes_button)
            self.driver.execute_script("arguments[0].click();", yes_button)
            print("✅ Clicked Yes on confirmation modal")
            time.sleep(3)

            # --- Click 'Print' on confirmation modal ---
            print_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Print']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", print_button)
            self.driver.execute_script("arguments[0].click();", print_button)
            print("✅ Clicked Print on confirmation modal")
        except Exception as e:
            print("❌ Error during save/confirm/print steps:", e)

        time.sleep(500) # Keep the browser open for a while to observe the result
