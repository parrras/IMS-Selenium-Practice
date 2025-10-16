from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class PomLogin:
    def __init__(self , driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.actions = ActionChains(driver)


        # Locators
        self.username_field =(By.XPATH,"//input[@formcontrolname='username']")
        self.password_field =(By.XPATH,"//input[@formcontrolname='password']")
        self.sign_field =(By.XPATH,"//button[normalize-space(text())='Sign In']")
        self.re_login = (By.XPATH,"//span[normalize-space(text())='Logout']")
        self.account_click = (By.XPATH , "//span[text()='Accounting Module']")
        self.account_Transaction = (By.XPATH , "//span[normalize-space(text())='Transactions']")
        self.opening_entries = (By.XPATH ,"//a[@title='Opening Entries']")

        #Actions

    def enter_username(self, username):
            self.wait.until(EC.visibility_of_element_located(self.username_field)).send_keys(username)

    def enter_password(self, password):
        self.wait.until(EC.visibility_of_element_located(self.password_field)).send_keys(password)

    def enter_sign_in (self):
        self.wait.until(EC.visibility_of_element_located(self.sign_field)).click()

    def entered_login(self):
        self.wait.until(EC.visibility_of_element_located(self.re_login)).click()

    def account_clicked(self):
        self.wait.until(EC.visibility_of_element_located(self.account_click)).click()

    def switch_to_new_window(self):
        # Switch Selenium focus to the newly opened window
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def account_transaction_click(self):
        self.wait.until(EC.visibility_of_element_located(self.account_Transaction)).click()

    def opening_entry_click(self):
        element = self.wait.until(EC.element_to_be_clickable(self.opening_entries))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        ActionChains(self.driver).move_to_element(element).click().perform()
        print("Hovered and clicked on Opening Entries successfully")
        time.sleep(300)

# def account_t_c(self):
    #    self.wait.until(EC.visibility_of_element_located(self.account_Transaction)).click()