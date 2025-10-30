# test_login.py
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PYTEST.pages.Login_Page import Login  # the Page Object class
from selenium import webdriver

@allure.title("Login to IMS Application")
@allure.description("This test logs into the IMS application using valid credentials and verifies the dashboard.")
def test_login_to_ims(setup):
    driver= setup
    login = Login(driver)
    login.perform_login("Paras", "Ims@1234")
    print("Login process completed.")
    login.perform_logout()
    print("logged out from the prev session")
    login.perform_ok()
    login.click_signin()
    # Wait for dashboard to load safely
    wait = WebDriverWait(driver, 30)
    date_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='date' and @id='Date']"))
    )
    print("Dashboard page loaded successfully!")

    assert date_input, "Date input not found"







