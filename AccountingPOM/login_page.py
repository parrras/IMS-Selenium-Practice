import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self):  # ✅ Proper constructor
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 25)

    def open(self):
        self.driver.get("https://redmiims.webredirect.himshang.com.np/#/login")

    def enter_username(self, username):
        username_field = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[2]/input")
            )
        )
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.driver.find_element(
            By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[3]/input"
        )
        password_field.send_keys(password)

    def click_signin(self):
        signin_button = self.driver.find_element(
            By.XPATH, "//button[normalize-space(text())='Sign In']"
        )
        signin_button.click()

    def handle_duplicate_logout(self):
        # noinspection PyBroadException
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
            time.sleep(8)

        except Exception as e:
            print("❌ Could not click Accounting Module:", e)

    def open_journal_voucher(self):
        actions = ActionChains(self.driver)

        # --- Step 1: Click Transactions ---
        try:
            transaction_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Transactions')]"))
            )
            self.driver.execute_script("arguments[0].click();", transaction_btn)
            print("✅ Clicked 'Transactions'")
            time.sleep(3)
        except Exception as e:
            print("❌ Couldn't click 'Transactions':", e)
            return

        # --- Step 2: Wait for Voucher Entries ---
        try:
            voucher_entries = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Voucher Entries')]"))
            )
            actions.move_to_element(voucher_entries).perform()
            print("✅ Hovered 'Voucher Entries'")
            time.sleep(2)
        except Exception as e:
            print("❌ 'Voucher Entries' not found or not visible:", e)
            return

        # --- Step 3: Click Journal Voucher ---
        try:
            journal_voucher = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space(text())='Journal Voucher']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", journal_voucher)
            self.driver.execute_script("arguments[0].click();", journal_voucher)
            print("✅ Clicked 'Journal Voucher'")
        except Exception as e:
            print("❌ Couldn't click 'Journal Voucher':", e)

        time.sleep(500) # Keep the browser open for a while to observe the result
