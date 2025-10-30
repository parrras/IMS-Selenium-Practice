# PYTEST/pages/Add_Customer.py
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Customer:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 25)
        self.actions = ActionChains(self.driver)

    # ---------------- CUSTOMER CREATION SECTION ----------------
    @allure.step("Hover and click an element")
    def hover_and_click(self, element):
        """Helper method to hover and click using ActionChains"""
        self.actions.move_to_element(element).click().perform()

    @allure.step("Scroll and click element")
    def scroll_and_click(self, element):
        """Helper method to scroll to an element and click"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        element.click()

    @allure.step("Create a new customer")
    def create_customer(self, name, address, vat_no, email, mobile):
        """Navigates to Customer Master and creates a new customer"""

        # --- Hover over "Customer & Vendor Info" ---
        customer_vendor_info = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Customer & Vendor Info"))
        )
        self.hover_and_click(customer_vendor_info)

        # --- Click on "Customer Master" ---
        customer_master = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Customer Master"))
        )
        customer_master.click()

        # --- Click on "Create Customer" ---
        create_customer_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='create']"))
        )
        self.scroll_and_click(create_customer_btn)
        time.sleep(1)  # small wait for form to load

        # --- Fill Customer Details ---
        self.wait.until(EC.presence_of_element_located((By.ID, "customerName"))).send_keys(name)
        self.driver.find_element(By.ID, "address").send_keys(address)
        self.driver.find_element(By.ID, "vatNo").send_keys(vat_no)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "Mobile").send_keys(mobile)

        # --- Click Save ---
        save_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "save"))
        )
        self.scroll_and_click(save_button)

        # --- Optional: wait for success message ---
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Customer saved successfully')]"))
        )
