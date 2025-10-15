import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date


# noinspection PyBroadException
class DebitNotePage:
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
            accounting_module = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Accounting Module')]")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", accounting_module)
            self.driver.execute_script("arguments[0].click();", accounting_module)
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            print("✅ Clicked Accounting Module")
            time.sleep(5)
        except Exception as e:
            print("❌ Could not click Accounting Module:", e)

    # --- Debit Note A/C ---
    def open_debit_note(self):
        try:
            # --- Step 1: Click Transactions ---
            transaction_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Transactions')]")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", transaction_btn)
            self.driver.execute_script("arguments[0].click();", transaction_btn)
            print("✅ Clicked 'Transactions'")
            time.sleep(5)

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
            time.sleep(5)

            # --- Step 3: Click Debit Note ---
            debit_note = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Debit Note - AC Base")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", debit_note)
            self.driver.execute_script("arguments[0].click();", debit_note)
            print("✅ Clicked on 'Debit Note - AC Base'")
            time.sleep(5)

            # Step 4: Enter Ref Number & Remarks
            ref_number_field_dr = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='refno']")))
            ref_number_field_dr.clear()
            ref_number_field_dr.send_keys("REF-10019800")
            print("✅ Entered Ref Number")
            time.sleep(5)

            remarks_field_dr = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='REMARKS']")))
            remarks_field_dr.click()
            remarks_field_dr.send_keys("This is a test.")
            print("✅ Entered Remarks")
            time.sleep(5)

            # Step 5: Debit Account
            debit_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='press ENTER to Select A/C']")))
            self.driver.execute_script("arguments[0].click();", debit_input)
            debit_input.send_keys(Keys.ENTER)
            debit_ac1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='TheTestCustom']")))
            self.actions.move_to_element(debit_ac1).double_click(debit_ac1).perform()
            print("✅ Selected debit Account ")
            time.sleep(5)

            # Step 5: Ledger Account 1
            ledger_input_dr = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_0']")))
            self.driver.execute_script("arguments[0].click();", ledger_input_dr)
            ledger_input_dr.send_keys(Keys.ENTER)
            ledger_ac_dr = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Siddhartha Bank']")))
            self.actions.move_to_element(ledger_ac_dr).double_click(ledger_ac_dr).perform()
            print("✅ Selected Ledger Account 1")
            time.sleep(5)

            # Step 6: Amount 1
            amount_field = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='CrAmtInput_0']")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amount_field)
            amount_field.send_keys("10000")
            print("✅ Entered amount: 10000")
            time.sleep(5)

            # Step 7: Narration 1
            narration_field_dr = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='narration_0']")))
            narration_field_dr.send_keys("Test Narration\n")
            print("✅ Entered Narration 1")
            time.sleep(5)

            # Step 8: Ledger Account 2
            ledger_input_dr1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_1']")))
            self.driver.execute_script("arguments[0].click();", ledger_input_dr1)
            ledger_input_dr1.send_keys(Keys.ENTER)
            ledger_ac_dr1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Test Account']")))
            self.actions.move_to_element(ledger_ac_dr1).double_click(ledger_ac_dr1).perform()
            print("✅ Selected Ledger Account 2")
            time.sleep(5)

            # Step 9: Amount 2
            amount_field1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='CrAmtInput_1']")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amount_field1)
            amount_field1.send_keys("20000")
            print("✅ Entered amount: 20000")
            time.sleep(5)

            # Step 7: Narration 2
            narration_field_dr1 = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='narration_1']")))
            narration_field_dr1.send_keys("Test Narration\n")
            print("✅ Entered Narration 1")
            time.sleep(5)

            # Step 8: Save & Confirm Contra Voucher
            save_button_dnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F6 SAVE']")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button_dnote)
            self.driver.execute_script("arguments[0].click();", save_button_dnote)
            print("✅ Clicked Save button")
            time.sleep(5)

            yes_button_dnote = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", yes_button_dnote)
            self.driver.execute_script("arguments[0].click();", yes_button_dnote)
            print("✅ Clicked Yes on confirmation modal")
            time.sleep(5)

            cancel_button_dnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cancel_button_dnote)
            self.driver.execute_script("arguments[0].click();", cancel_button_dnote)
            print("✅ Clicked Cancel on confirmation modal")

        except Exception as e:
            print("❌ Could not open Debit Note:", e)

        time.sleep(500)