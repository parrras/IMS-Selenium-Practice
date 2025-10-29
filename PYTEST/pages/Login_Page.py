# PYTEST/Login.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


class Login:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 25)
        self.actions = ActionChains(self.driver)


    def perform_login(self, username, password):
        self.driver.get("https://redmiims.webredirect.himshang.com.np/#/login")
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Username']")  # safer placeholder/XPath
        )).send_keys(username)
        self.driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[normalize-space(text())='Sign In']").click()

    def perform_logout(self):
        try:
            logout_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
            )
            logout_button.click()
            print("Logged out successfully.")

            # ok_button = self.wait.until(
            #     EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
            # )
            # ok_button.click()
            # print("Clicked OK on confirmation dialog.")

        except TimeoutException:
            print("Logout button or login page not found, skipping logout.")

    def perform_ok(self):
        ok_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and normalize-space(text())='OK']"))
        )
        ok_button.click()
        print("Clicked OK on confirmation dialog.")


    def click_signin(self):
        signin_button = self.driver.find_element(
            By.XPATH, "//button[normalize-space(text())='Sign In']"
        )
        signin_button.click()
        print("login bhayo")

