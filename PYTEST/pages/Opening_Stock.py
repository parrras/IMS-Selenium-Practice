import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# noinspection PyBroadException
@allure.feature("Opening Stock")
class OpeningStockPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.actions = ActionChains(driver)

    # noinspection PyBroadException
    @allure.step("Generate Opening Stock")
    def generate_opening_stock(self):
        print("🚀 Starting Opening Stock generation...")

        # Step 1: Navigate to Transactions → Opening Stock
        print("📂 Navigating to Transactions → Opening Stock...")

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

        opening_stock = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Opening Stock"))
        )
        opening_stock.click()
        print("✅ Opening Stock page opened.")
        time.sleep(2)

        # STEP 2 → ENTER REMARKS
        print("📝 Adding remark...")
        remark_field = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@type='text']"))
        )
        remark_field.click()
        remark_field.send_keys("Opening stock entry added automatically.")

        time.sleep(1)

        # STEP 3 → SELECT FIRST ITEM
        print("📦 Selecting first item...")
        item_field = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='itemDesc0']"))
        )
        item_field.click()
        item_field.send_keys(Keys.ENTER)
        time.sleep(1)

        first_item = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='33333']"))
        )
        self.actions.double_click(first_item).perform()
        time.sleep(1)

        # ENTER QUANTITY FOR FIRST ITEM
        qty_field_1 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='alternateQty0']"))
        )
        qty_field_1.click()
        qty_field_1.clear()
        qty_field_1.send_keys("20")

        # TAB from QTY → RATE
        qty_field_1.send_keys(Keys.TAB)
        time.sleep(0.5)

        # Now RATE field is active — TAB to MFG DATE
        rate_field = self.driver.switch_to.active_element
        rate_field.send_keys(Keys.TAB)
        time.sleep(0.5)

        # Now MFG DATE (id=mfgdate0) is active — TAB to EXP DATE
        mfg_date_field = self.driver.switch_to.active_element
        mfg_date_field.send_keys(Keys.TAB)
        time.sleep(0.5)

        # Now EXP DATE (id=expdate0) is active — TAB to next ITEM FIELD
        exp_date_field = self.driver.switch_to.active_element
        exp_date_field.send_keys(Keys.TAB)
        time.sleep(1)

        # STEP 4 → SELECT SECOND ITEM
        print("📦 Selecting second item...")
        item_field_2 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='itemDesc1']"))
        )
        item_field_2.click()
        item_field_2.send_keys(Keys.ENTER)
        time.sleep(1)

        second_item = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='Amigo Nepal 2345']"))
        )
        self.actions.double_click(second_item).perform()
        time.sleep(1)

        # ENTER QUANTITY FOR SECOND ITEM
        qty_field_2 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='alternateQty1']"))
        )
        qty_field_2.click()
        qty_field_2.clear()
        qty_field_2.send_keys("20")

        # TAB from QTY → RATE
        qty_field_2.send_keys(Keys.TAB)
        time.sleep(0.5)

        # Now RATE field is active — send TAB again
        rate_field1 = self.driver.switch_to.active_element
        rate_field1.send_keys(Keys.TAB)
        time.sleep(1)

        # STEP 5 → CLICK SAVE
        print("💾 Saving Opening Stock...")
        save_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='SAVE [End]']")
            )
        )
        save_btn.click()

        print("🎉 Opening Stock entry completed successfully!")

