import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@allure.feature("Add Product Category")
class AddProductCategoryPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.actions = ActionChains(driver)

    # --- Login ---
    @allure.step("Login to IMS application")
    def login(self, username, password):
        self.driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[2]/input"))).send_keys(username)
        self.driver.find_element(By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[3]/input").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[normalize-space(text())='Sign In']").click()
        time.sleep(5)

    # --- Navigate to Product Category page ---
    @allure.step("Navigate to Product Category page")
    def navigate_to_add_product(self):
        try:
            inventory_info = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Inventory Info")))
        except TimeoutException:
            inventory_info = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Inventory Info')]")))
        ActionChains(self.driver).move_to_element(inventory_info).perform()
        time.sleep(2)

        product_category = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Product Category")))
        product_category.click()
        time.sleep(3)

    # --- Add Product Category ---
    @allure.step("Add new product category")
    def add_product_category(self, category_name="ToothPaste"):
        try:
            # Click "Add Category" button
            add_category_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Add Category')]")
            ))
            add_category_btn.click()
            time.sleep(2)

            # Enter Category Name
            category_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@id='catName']")
            ))
            category_input.clear()
            category_input.send_keys(category_name)
            time.sleep(1)

            # Click "Save" button
            save_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Save')]")
            ))
            save_btn.click()
            time.sleep(2)

            # Click "OK" button on confirmation
            ok_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'OK')]")
            ))
            ok_btn.click()
            time.sleep(2)

            allure.attach(self.driver.get_screenshot_as_png(), name="Add_Product_Category_Success", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Add_Product_Category_Error", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"❌ Failed to add product category. Error: {e}")
