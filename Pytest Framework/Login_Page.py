import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# noinspection PyBroadException
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 25)
        self.actions = ActionChains(self.driver)

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

    def handle_duplicate_logout(self):
        try:
            logout_button_locator = (By.XPATH, "//span[normalize-space(text())='Logout']")
            popup_logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(logout_button_locator)
            )
            popup_logout_button.click()
            print("✅ Detected previous session popup and clicked Logout.")
            time.sleep(2)
        except Exception:
            print("⚠ No previous session popup detected.")

    # ✅ Updated: Verify login result
    def is_login_successful(self):
        """
        Returns True if login succeeded, False if failed.
        Waits for either Dashboard element (success) or error message (failure).
        """
        dashboard_locator = (By.XPATH, "//span[contains(text(), 'Dashboard')]")
        error_locator = (By.XPATH, "//div[contains(@class,'toast-message') or contains(text(),'Invalid')]")

        try:
            # Wait for either dashboard or error message
            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_elements(*dashboard_locator) or d.find_elements(*error_locator)
            )

            if self.driver.find_elements(*dashboard_locator):
                return True
            else:
                return False
        except:
            return False

    def get_error_message(self):
        try:
            error_message = self.driver.find_element(
                By.XPATH, "//div[contains(@class,'toast-message') or contains(text(),'Invalid')]"
            )
            return error_message.text
        except:
            return "Unknown error"
