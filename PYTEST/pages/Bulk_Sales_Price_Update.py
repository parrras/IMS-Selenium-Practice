import time
import allure
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Bulk Sales Price Update")
class BulkSalesPriceUpdatePage:

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

    # --- Navigate to Bulk Sales Price Update page ---
    @allure.step("Navigate to Bulk Sales Price Update page")
    def navigate_to_bulk_sales_price(self):
        try:
            sales_price_info = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sales Price Info")))
        except TimeoutException:
            sales_price_info = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Sales Price Info')]")))
        ActionChains(self.driver).move_to_element(sales_price_info).perform()
        time.sleep(2)

        bulk_price_change = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Bulk Price Change")))
        bulk_price_change.click()
        print("✅ Navigated to Bulk Price Change page.")
        time.sleep(3)

    # --- Select Item Group (Chocolate) and Category (Chocolate) ---
    @allure.step("Select Item Group and Category: Chocolate")
    def select_item_group(self):
        try:
            # Step 1: Select Category as Chocolate
            category_dropdown = self.wait.until(
                EC.visibility_of_element_located((By.ID, "Category"))
            )
            category_dropdown.click()
            time.sleep(5)

            chocolate_category_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//select[@id='Category']/option[text()='Chocolate']"))
            )
            chocolate_category_option.click()
            print("✅ Selected Category: Chocolate")
            time.sleep(5)

            # Step 2: Attach screenshot to Allure
            allure.attach(self.driver.get_screenshot_as_png(), name="Item_Group_and_Category_Selected",
                          attachment_type=allure.attachment_type.PNG)
            print("📸 Screenshot attached: Item Group and Category selected successfully.")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Item_Group_Select_Error",
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"❌ Failed to select Item Group or Category due to: {e}")

    # --- Update prices for 4 items ---
    @allure.step("Update Prices for 4 Items with Random Values")
    def update_prices(self):
        try:
            # IDs of the 4 input fields
            price_fields = [
                "newSpriceInc0",  # Milk Chocolate
                "newSpriceInc1",  # Milk Chocolate variant
                "newSpriceInc2",  # Dark Chocolate
                "newSpriceInc3",  # Prod Test / White Chocolate
                "newSpriceInc4"
            ]

            for field_id in price_fields:
                price_input = self.wait.until(
                    EC.visibility_of_element_located((By.ID, field_id))
                )
                price_input.clear()  # Clear existing value
                random_price = random.randint(500, 1000)
                price_input.send_keys(str(random_price))
                print(f"✅ Updated {field_id} with price: {random_price}")

            # --- Click Save button ---

            save_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Save' and contains(@class,'btn-info')]")
            ))
            # Scroll into view if necessary
            self.driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
            time.sleep(1)
            try:
                save_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", save_button)
            print("✅ Clicked Save button after updating prices")
            time.sleep(5)

            # Attach screenshot after updating prices
            allure.attach(self.driver.get_screenshot_as_png(), name="Prices_Updated",
                          attachment_type=allure.attachment_type.PNG)
            print("📸 Screenshot attached: Prices updated successfully.")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Price_Update_Error",
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"❌ Failed to update prices due to: {e}")
