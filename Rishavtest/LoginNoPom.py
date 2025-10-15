import time

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException

from LoginPom import PomLogin

driver = webdriver.Chrome()
driver.get("https://redmiims.webredirect.himshang.com.np/#/login")  # Replace with your login page URL
driver.maximize_window()

login = PomLogin(driver)
login.enter_username("Paras")  # Replace "admin" with your username
login.enter_password("Ims@1234")
login.enter_sign_in()
try:
    login.entered_login()
except (TimeoutException, NoSuchElementException):
    print("Login Not seen")

#login.entered_login()
time.sleep(5)
login.enter_sign_in()
login.account_clicked()
time.sleep(20)
#login.account_t_c()
login.switch_to_new_window()

# Click Transactions in the new window
login.account_transaction_click()
time.sleep(5)
login.opening_entry_click()
driver.quit()