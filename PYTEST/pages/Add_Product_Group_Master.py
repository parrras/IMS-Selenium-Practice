import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@allure.feature("Add Product Group Master")
class AddProductGroupMasterPage:

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

    # --- Navigate to Add Product Group page ---
    @allure.step("Navigate to Add Product Group Master page")
    def navigate_to_add_product(self):
        try:
            inventory_info = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Inventory Info")))
        except TimeoutException:
            inventory_info = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Inventory Info')]")))
        ActionChains(self.driver).move_to_element(inventory_info).perform()
        time.sleep(2)

        product_master = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Product Group Master")))
        product_master.click()
        time.sleep(3)

        add_product_group_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='create' and contains(., 'Add Product Group')]")))
        add_product_group_button.click()
        print("✅ Clicked on Add Product Group button.")
        time.sleep(2)

    # --- Select Parent Group ---
    @allure.step("Select Item Group as BODY CARE")
    def select_item_group(self):
        item_group_icon = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-icon[normalize-space(text())='open_in_new']")))
        item_group_icon.click()
        time.sleep(1)

        main_group_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-autocomplete='list' and @type='text']")))
        main_group_input.send_keys("B")
        body_care_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='BODY CARE']")))
        body_care_option.click()
        ok_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Ok']")))
        ok_button.click()
        print("✅ Selected parent group: BODY CARE.")
        time.sleep(2)

    # --- Fill Group Details ---
    @allure.step("Fill group details and save Product Group")
    def fill_group_details_and_save(self):
        print("🧾 Filling Product Group details...")

        # --- Group Name ---
        group_name_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='groupName']")))
        group_name_field.clear()
        group_name_field.send_keys("Hygiene")
        print("✅ Entered Group Name: Hygiene")

        # --- Recommended Margin ---
        margin_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='recommendedMargin']")))
        margin_field.clear()
        margin_field.send_keys("10")
        print("✅ Entered Recommended Margin: 10%")

        # --- Shelf Life ---
        shelf_life_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='shelfLife']")))
        shelf_life_field.clear()
        shelf_life_field.send_keys("30")
        print("✅ Entered Shelf Life: 30 days")

        # --- Click Save Button ---
        save_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='save' and normalize-space(text())='SAVE']")))
        save_button.click()
        print("💾 Clicked Save button.")
        time.sleep(2)

        # --- Check for success or duplicate popup ---
        try:
            # Wait for alert/toast message
            message_element = self.wait.until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "//*[contains(text(), 'success') or contains(text(), 'exists') or contains(text(), 'Duplicate') or contains(text(), 'added')]"))
            )
            message_text = message_element.text.strip()
            print(f"📢 System message: {message_text}")

            # Attach screenshot
            allure.attach(self.driver.get_screenshot_as_png(), name="Product_Group_Result",
                          attachment_type=allure.attachment_type.PNG)

            # --- Validation: Fail test on duplicate or error ---
            if any(word in message_text.lower() for word in ["duplicate", "exist", "error", "failed", "already"]):
                print("❌ Duplicate or error message detected.")
                raise AssertionError(f"Product Group not added successfully — System message: {message_text}")
            else:
                print("✅ Product Group added successfully.")
                print("🎉 Test passed!")

        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="Product_Group_Timeout",
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError("❌ No confirmation message appeared after clicking SAVE — possible system issue.")


