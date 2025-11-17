import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# noinspection PyBroadException
@allure.feature("Stock Issue")
class StockIssuePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.actions = ActionChains(driver)

    # noinspection PyBroadException
    @allure.step("Generate Stock Issue")
    def generate_stock_issue(self):
        print("🚀 Starting Stock Issue generation...")

        # Step 1: Navigate to Transactions → Stock Issue
        print("📂 Navigating to Transactions → Stock Issue...")

        transaction_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Transactions']"))
        )
        transaction_btn.click()
        time.sleep(1)

        try:
            inventory_movement = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Inventory Movement"))
            )
        except:
            inventory_movement = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[normalize-space()='Inventory Movement']")
                )
            )

        ActionChains(self.driver).move_to_element(inventory_movement).pause(0.3).perform()
        time.sleep(2)

        stock_issue = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Stock Issue"))
        )
        stock_issue.click()
        print("✅ Stock Issue page opened.")
        time.sleep(2)

        # STEP 2: Select From Warehouse
        print("🏷 Selecting From Warehouse...")
        from_wh = self.wait.until(
            EC.element_to_be_clickable((By.ID, "stockissueFromWH"))
        )
        from_wh.click()
        time.sleep(1)

        main_wh = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@id='stockissueFromWH']/option[contains(text(),'Main Warehouse')]"))
        )
        main_wh.click()
        print("✅ Selected From Warehouse: Main Warehouse")
        time.sleep(3)

        # STEP 3: Enter Remark
        print("📝 Entering Remark...")
        remark_field = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//textarea"))
        )
        remark_field.click()
        remark_field.send_keys("Stock Issue Automation Entry")
        print("✅ Remark added.")
        time.sleep(3)

        # STEP 4: Select To Warehouse
        print("🏷 Selecting To Warehouse...")

        # Click the SECOND warehouse dropdown
        to_wh = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//select[@style='width: 70%;' and contains(@class,'ng-valid')])[2]")
            )
        )
        to_wh.click()
        time.sleep(2)

        # Select "Test" from second dropdown
        test_wh = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "(//select[@style='width: 70%;' and contains(@class,'ng-valid')])[2]/option[contains(text(),'Test')]")
            )
        )
        test_wh.click()
        print("✅ Selected To Warehouse: Test")
        time.sleep(2)

        # STEP 5: Select Item
        print("📦 Selecting Item...")

        select_item_field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "ITEMDESC0"))
        )
        select_item_field.click()
        select_item_field.send_keys(Keys.ENTER)
        time.sleep(2)

        # Double click item "Amigo Nepal 2345"
        item_to_select = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Amigo Nepal 2345')]"))
        )
        ActionChains(self.driver).double_click(item_to_select).perform()
        print("✅ Selected Item: Amigo Nepal 2345")
        time.sleep(2)

        # STEP 6: Enter Quantity
        print("🔢 Entering Quantity...")
        qty_field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "ALTERNATEQUANTIY0"))
        )
        qty_field.click()
        qty_field.send_keys("20")
        time.sleep(1)

        # TAB once → moves to rate field
        qty_field.send_keys(Keys.TAB)
        time.sleep(5)

        # STEP 7: Save
        print("💾 Saving Stock Issue...")
        save_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'SAVE [End]')]"))
        )

        try:
            save_button.click()
        except:
            self.driver.execute_script("arguments[0].click();", save_button)

        print("✅ Stock Issue Saved Successfully!")
        allure.attach(self.driver.get_screenshot_as_png(), name="Stock_Issue_Success",
                      attachment_type=allure.attachment_type.PNG)
