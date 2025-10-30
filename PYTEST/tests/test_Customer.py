# PYTEST/tests/test_Customer.py
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from PYTEST.pages.Login_Page import Login
from PYTEST.pages.Add_Customer import Customer

@allure.title("Create Customer in IMS Application")
@allure.description("Logs in, navigates to Customer Master, and creates a new customer record.")
def test_create_customer(setup):
    driver = setup
    wait = WebDriverWait(driver, 30)

    # Login
    login = Login(driver)
    login.perform_login("Paras", "Ims@1234")
    print("✅ Logged in")

    # Wait for dashboard
    wait.until(EC.presence_of_element_located((By.ID, "Date")))
    print("✅ Dashboard loaded")

    # Create customer
    customer = Customer(driver)
    customer.create_customer(
        name="Hergfffh Khadka",
        address="Himl Nepal",
        vat_no="265565621",
        email="rjhjgl@gmail.com",
        mobile="9801121872"
    )
    print("✅ Customer created")

    # Verify success
    success_msg = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Customer saved successfully')]"))
    )
    assert success_msg.is_displayed()
    print("🎉 Customer creation verified")
