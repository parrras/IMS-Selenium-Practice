import time
import random
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# noinspection PyBroadException
class CreditNotePage:
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
            # Try to find Logout button (if duplicate session alert appears)
            logout_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Logout']]"))
            )
            logout_button.click()
            print("✅ Logged out from duplicate session")

            # Click OK to confirm logout
            ok_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='OK']"))
            )
            ok_button.click()
            time.sleep(2)

            # Re-login button
            re_login_btn = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-auth"))
            )
            re_login_btn.click()
            time.sleep(3)
            print("✅ Re-logged in successfully")

        except Exception:
            # If no duplicate login found, assume normal login
            print("✅ No duplicate session found — proceeding normally")


    # --- OPEN ACCOUNTING MODULE ---
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

    # --- Open Credit Note ---
    def open_credit_note(self):
        try:
            # --- Step 1: Click Transaction ---
            transaction_menu = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Transaction')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", transaction_menu)
            self.driver.execute_script("arguments[0].click();", transaction_menu)
            print("✅ Clicked Transaction menu")
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

            # --- Step 3: Click Credit Note ---
            credit_note = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Credit Note - AC Base"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", credit_note)
            self.driver.execute_script("arguments[0].click();", credit_note)
            print("✅ Clicked 'Credit Note - AC Base'")
            time.sleep(5)

            # Step 4: Generate a random reference number
            random_ref = f"REF-{random.randint(100000, 999999)}"

            # Locate and enter the reference number
            ref_number_cr = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='refno']"))
            )
            ref_number_cr.send_keys(random_ref)
            print(f"✅ Entered Ref Number: {random_ref}")
            time.sleep(5)

            remarks_field_cr = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='REMARKS']"))
            )
            remarks_field_cr.click()
            remarks_field_cr.send_keys("Remarks for Credit Note")
            print("✅ Entered Remarks")
            time.sleep(5)

            # Step 5: Select Debit Account
            credit_input = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='press ENTER to Select A/C']"))
            )
            self.driver.execute_script("arguments[0].click();", credit_input)
            credit_input.send_keys(Keys.ENTER)
            credit_ac1 = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='TheTestCustom']"))
            )
            self.actions.move_to_element(credit_ac1).double_click(credit_ac1).perform()
            print("✅ Selected Debit Account")
            time.sleep(5)

            # Step 6: Ledger Account 1
            ledger_input_cr = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_0']"))
            )
            self.driver.execute_script("arguments[0].click();", ledger_input_cr)
            ledger_input_cr.send_keys(Keys.ENTER)
            ledger_ac_cr = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='Siddhartha Bank']"))
            )
            self.actions.move_to_element(ledger_ac_cr).double_click(ledger_ac_cr).perform()
            print("✅ Selected Ledger Account 1")
            time.sleep(5)

            # Step 7: Amount 1
            random_amount_cr1 = random.randint(1000, 50000)
            amount_input_cr = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='DrAmtInput_0']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amount_input_cr)
            amount_input_cr.send_keys(str(random_amount_cr1))
            print(f"✅ Entered Amount 1: {random_amount_cr1}")
            time.sleep(5)

            # Step 8: Narration 1
            narration_field_cr = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='narration_0']"))
            )
            narration_field_cr.send_keys("Credit Note Narration 1\n")
            print("✅ Entered Narration 1")
            time.sleep(5)

            # Step 9: Ledger Account 2
            ledger_input_cr1 = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_1']"))
            )
            self.driver.execute_script("arguments[0].click();", ledger_input_cr1)
            ledger_input_cr1.send_keys(Keys.ENTER)
            ledger_ac_cr1 = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='Test Account']"))
            )
            self.actions.move_to_element(ledger_ac_cr1).double_click(ledger_ac_cr1).perform()
            print("✅ Selected Ledger Account 2")
            time.sleep(5)

            # Step 10: Amount 2
            random_amount_cr2 = random.randint(1000, 50000)
            amount_input_cr1 = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='DrAmtInput_1']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amount_input_cr1)
            amount_input_cr1.send_keys(str(random_amount_cr2))
            print(f"✅ Entered Amount 2: {random_amount_cr2}")
            time.sleep(5)

            # Step 11: Narration 2
            narration_field_cr1 = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='narration_1']"))
            )
            narration_field_cr1.send_keys("Credit Note Narration 2\n")
            print("✅ Entered Narration 2")
            time.sleep(5)

            # Step 12: Save and Confirm Credit Note Entry
            save_button_cnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F6 SAVE']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button_cnote)
            self.driver.execute_script("arguments[0].click();", save_button_cnote)
            print("✅ Clicked Save button")
            time.sleep(5)

            yes_button_cnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", yes_button_cnote)
            self.driver.execute_script("arguments[0].click();", yes_button_cnote)
            print("✅ Confirmed Credit Note entry")
            time.sleep(5)

            cancel_button_cnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cancel_button_cnote)
            self.driver.execute_script("arguments[0].click();", cancel_button_cnote)
            print("✅ Clicked Cancel on confirmation modal")
            time.sleep(10)

        except Exception as e:
            print("❌ An error occurred while creating Credit Note:", e)

    def view_credit_note(self):
        try:
            # --- Step 13: View the Credit Note ---
            view_button_cnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F4 VIEW']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", view_button_cnote)
            self.driver.execute_script("arguments[0].click();", view_button_cnote)
            print("✅ Clicked View button")
            time.sleep(5)

            # --- Step 14: Double-click on the Credit Note to view ---
            cnote_to_view = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='10/26/2025']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cnote_to_view)
            self.actions.move_to_element(cnote_to_view).double_click(cnote_to_view).perform()
            print("✅ Opened Credit Note for viewing")
            time.sleep(10)

            # --- Step 15: Click the back button after viewing ---
            back_button_cnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F10 BACK']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", back_button_cnote)
            self.driver.execute_script("arguments[0].click();", back_button_cnote)
            print("✅ Clicked Back button after viewing Credit Note")

            time.sleep(500)

        except Exception as e:
            print("❌ An error occurred while viewing Credit Note:", e)

























