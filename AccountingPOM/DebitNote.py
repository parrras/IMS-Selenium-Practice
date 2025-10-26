import time
import random
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# noinspection PyBroadException
class DebitNotePage:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 25)
        self.actions = ActionChains(self.driver)

    # --- LOGIN SECTION ---
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

    # --- HANDLE DUPLICATE LOGOUT ---
    def handle_duplicate_logout(self):
        try:
            # Define the locators directly inside the function
            logout_button_locator = (By.XPATH, "//span[normalize-space(text())='Logout']")
            login_button_locator = (By.XPATH, "//button[normalize-space(text())='Sign In']")

            # Wait for and click the Logout button from popup
            popup_logout_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(logout_button_locator)
            )
            popup_logout_button.click()
            print("✅ Detected previous session popup and clicked Logout.")
            time.sleep(5)

            # Wait for and click the Sign In button again
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(login_button_locator)
            )
            login_button.click()
            print("✅ Login button clicked again after logout.")

        except Exception as e:
            print(f"⚠ No previous session popup detected or unable to locate elements: {e}")


        time.sleep(5)

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

    # --- OPEN DEBIT NOTE ENTRY ---
    def open_debit_note(self):
        try:
            # Step 1: Click Transactions
            transaction_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Transactions')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", transaction_btn)
            self.driver.execute_script("arguments[0].click();", transaction_btn)
            print("✅ Clicked 'Transactions'")
            time.sleep(5)

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
            self.actions.move_to_element(voucher_entries).pause(0.5).perform()
            print("✅ Hovered over 'Voucher Entries'")
            time.sleep(5)

            # Step 3: Click Debit Note
            debit_note = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Debit Note - AC Base"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", debit_note)
            self.driver.execute_script("arguments[0].click();", debit_note)
            print("✅ Clicked on 'Debit Note - AC Base'")
            time.sleep(5)

            # Step 4: Enter Ref Number & Remarks
            random_ref_dr = f"REF-{random.randint(100000, 999999)}"

            ref_number_field_dr = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='refno']"))
            )
            ref_number_field_dr.clear()
            ref_number_field_dr.send_keys(random_ref_dr)
            print(f"✅ Entered Ref Number: {random_ref_dr}")
            time.sleep(5)

            remarks_field_dr = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='REMARKS']"))
            )
            remarks_field_dr.click()
            remarks_field_dr.send_keys("This is a test.")
            print("✅ Entered Remarks")
            time.sleep(5)

            # Step 5: Select Debit Account
            debit_input = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='press ENTER to Select A/C']"))
            )
            self.driver.execute_script("arguments[0].click();", debit_input)
            debit_input.send_keys(Keys.ENTER)
            debit_ac1 = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='TheTestCustom']"))
            )
            self.actions.move_to_element(debit_ac1).double_click(debit_ac1).perform()
            print("✅ Selected Debit Account")
            time.sleep(5)

            # Step 6: Select Ledger Account 1
            ledger_input_dr = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_0']"))
            )
            self.driver.execute_script("arguments[0].click();", ledger_input_dr)
            ledger_input_dr.send_keys(Keys.ENTER)
            ledger_ac_dr = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='Siddhartha Bank']"))
            )
            self.actions.move_to_element(ledger_ac_dr).double_click(ledger_ac_dr).perform()
            print("✅ Selected Ledger Account 1")
            time.sleep(5)

            # Step 7: Enter Amount 1
            random_amount = random.randint(1000, 50000)  # generates random amount between 1000–50000

            amount_field = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='CrAmtInput_0']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amount_field)
            amount_field.clear()
            amount_field.send_keys(str(random_amount))
            print(f"✅ Entered Amount: {random_amount}")
            time.sleep(5)

            # Step 8: Enter Narration 1
            narration_field_dr = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='narration_0']"))
            )
            narration_field_dr.send_keys("Test Narration\n")
            print("✅ Entered Narration 1")
            time.sleep(5)

            # Step 9: Select Ledger Account 2
            ledger_input_dr1 = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_1']"))
            )
            self.driver.execute_script("arguments[0].click();", ledger_input_dr1)
            ledger_input_dr1.send_keys(Keys.ENTER)
            ledger_ac_dr1 = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='Test Account']"))
            )
            self.actions.move_to_element(ledger_ac_dr1).double_click(ledger_ac_dr1).perform()
            print("✅ Selected Ledger Account 2")
            time.sleep(5)

            # Step 10: Enter Amount 2
            random_amount2 = random.randint(1000, 50000)  # generates random amount between 1000–50000

            amount_field1 = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='CrAmtInput_1']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amount_field1)
            amount_field1.clear()
            amount_field1.send_keys(str(random_amount2))
            print(f"✅ Entered Amount: {random_amount2}")
            time.sleep(5)

            # Step 11: Enter Narration 2
            narration_field_dr1 = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='narration_1']"))
            )
            narration_field_dr1.send_keys("Test Narration\n")
            print("✅ Entered Narration 2")
            time.sleep(5)

            # Step 12: Save & Confirm Debit Note
            save_button_dnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F6 SAVE']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button_dnote)
            self.driver.execute_script("arguments[0].click();", save_button_dnote)
            print("✅ Clicked Save button")
            time.sleep(5)

            yes_button_dnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", yes_button_dnote)
            self.driver.execute_script("arguments[0].click();", yes_button_dnote)
            print("✅ Clicked Yes on confirmation modal")
            time.sleep(5)

            cancel_button_dnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cancel_button_dnote)
            self.driver.execute_script("arguments[0].click();", cancel_button_dnote)
            print("✅ Clicked Cancel on confirmation modal")
            time.sleep(10)

        except Exception as e:
            print("❌ Could not open Debit Note:", e)

    def edit_debit_note(self):
        try:
            # --- Step 13: Click EDIT button ---
            edit_button_dr = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'F5 EDIT')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_button_dr)
            self.driver.execute_script("arguments[0].click();", edit_button_dr)
            print("✅ Clicked on 'F5 EDIT' button")
            time.sleep(5)

            # --- Step 14: Double-click on the voucher to edit ---
            dnote_to_edit = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='10/26/2025']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dnote_to_edit)
            self.actions.move_to_element(dnote_to_edit).double_click(dnote_to_edit).perform()
            print("✅ Double-clicked on the voucher dated 10/26/2025 for editing")
            time.sleep(5)

            # Step 6: Edit Ledger Account 1 and 2
            edit_ledger_input1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_0']")))
            self.driver.execute_script("arguments[0].click();", edit_ledger_input1)
            edit_ledger_input1.send_keys(Keys.ENTER)
            edit_ledger_ac1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='ROUNDING A/C']")))
            self.actions.move_to_element(edit_ledger_ac1).double_click(edit_ledger_ac1).perform()
            print("✅ Edited Ledger Account 1")
            time.sleep(5)

            edit_ledger_input2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ACCODEInput_1']")))
            self.driver.execute_script("arguments[0].click();", edit_ledger_input2)
            edit_ledger_input2.send_keys(Keys.ENTER)
            edit_ledger_ac2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='PETTY CASH A/C']")))
            self.actions.move_to_element(edit_ledger_ac2).double_click(edit_ledger_ac2).perform()
            print("✅ Edited Ledger Account 2")
            time.sleep(5)

            # --- Step 15: Edit the amount fields of Debit Note ---
            random_amount_edit1 = random.randint(1000, 30000)
            amount_field_edit1 = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='CrAmtInput_0']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amount_field_edit1)
            amount_field_edit1.clear()
            amount_field_edit1.send_keys(str(random_amount_edit1))
            print(f"💰 Updated Amount 1 to: {random_amount_edit1}")
            time.sleep(5)

            random_amount_edit2 = random.randint(1000, 30000)
            amount_field_edit2 = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='CrAmtInput_1']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amount_field_edit2)
            amount_field_edit2.clear()
            amount_field_edit2.send_keys(str(random_amount_edit2))
            print(f"💰 Updated Amount 2 to: {random_amount_edit2}")
            time.sleep(5)

            # --- Step 8: Edit Narration Fields of Debit Note ---
            narration_field1 = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='narration_0']"))
            )
            narration_field1.clear()
            narration_field1.send_keys("Updated Nar for Acc 1")
            print("Updated Narration 1")
            time.sleep(5)

            narration_field2 = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='narration_1']"))
            )
            narration_field2.clear()
            narration_field2.send_keys("Updated Nar for Acc 2")
            print("Updated Narration 2")
            time.sleep(5)

            # Step 12: Save & Confirm Edited Debit Note
            save_dnote_edit = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F6 SAVE']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_dnote_edit)
            self.driver.execute_script("arguments[0].click();", save_dnote_edit)
            print("✅ Clicked Save button")
            time.sleep(5)

            yes_dnote_edit = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Yes']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", yes_dnote_edit)
            self.driver.execute_script("arguments[0].click();", yes_dnote_edit)
            print("✅ Clicked Yes on confirmation modal")
            time.sleep(5)

            cancel_dnote_edit = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cancel_dnote_edit)
            self.driver.execute_script("arguments[0].click();", cancel_dnote_edit)
            print("✅ Clicked Cancel on confirmation modal")
            time.sleep(10)

        except Exception as e:
            print("❌ Could not open Debit Note:", e)

    def view_debit_note(self):
        try:
            # --- Step 13: Click VIEW button ---
            view_button_dnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'F4 VIEW')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", view_button_dnote)
            self.driver.execute_script("arguments[0].click();", view_button_dnote)
            print("✅ Clicked on 'F4 VIEW' button")
            time.sleep(5)

            # --- Step 14: Double-click on the Debit Note to view ---
            dnote_to_view = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='10/26/2025']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dnote_to_view)
            self.actions.move_to_element(dnote_to_view).double_click(dnote_to_view).perform()
            print("✅ Double-clicked on the voucher dated 10/26/2025 for viewing")
            time.sleep(10)

            # --- Step 15: Click the Back button to exit view mode ---
            back_button_dnote = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='F10 BACK']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", back_button_dnote)
            self.driver.execute_script("arguments[0].click();", back_button_dnote)
            print("✅ Clicked on 'F10 BACK' button to exit view mode")

            time.sleep(500)

        except Exception as e:
            print(f"❌ Error while deleting contra voucher: {e}")




