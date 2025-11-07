import time
import random
import string
import csv
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@allure.feature("Add Product and Generate Invoice")
class AddProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.csv_file = 'Added_Products.csv'

    # --- Login ---
    @allure.step("Login to IMS application")
    def login(self, username, password):
        self.driver.get("https://redmiims.variantqa.himshang.com.np/#/login")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[2]/input"))).send_keys(username)
        self.driver.find_element(By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[3]/input").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[normalize-space(text())='Sign In']").click()
        time.sleep(5)

    # --- Navigate to Add Product page ---
    @allure.step("Navigate to Add Product page")
    def navigate_to_add_product(self):
        try:
            inventory_info = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Inventory Info")))
        except TimeoutException:
            inventory_info = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Inventory Info')]")))
        ActionChains(self.driver).move_to_element(inventory_info).perform()
        time.sleep(2)

        product_master = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Product Master")))
        product_master.click()
        time.sleep(3)

        add_product_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='createDropdown']")))
        add_product_button.click()
        time.sleep(1)

        add_product_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Add Product']")))
        self.driver.execute_script("arguments[0].click();", add_product_option)
        time.sleep(2)

    # --- Select Item Group ---
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

    # --- Generate random data ---
    @staticmethod
    def generate_random_name(length=5):
        product= ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
        return "prd-" + product

    # --- Add multiple products ---
    @allure.step("Add 10 random products (first 5: inventory & ticked, next 5: service & unticked)")
    def add_multiple_products(self, count=10):
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['Product Name', 'HS Code', 'Stock Unit', 'Purchase Price', 'Sales Price', 'Barcode', 'Supplier']
            )

            for i in range(count):
                product_name = self.generate_random_name()
                hs_code = str(random.randint(100000, 999999))
                stock_unit = "Bottle"
                purchase_price = random.randint(10, 500)
                sales_price = random.randint(purchase_price + 150, purchase_price + 200)
                barcode = f"1.{324 + i}"
                supplier = "Sujata Vendor"

                # ✅ Logging product details
                allure.attach(
                    f"Adding product #{i + 1}: {product_name}",
                    name="Product Info",
                    attachment_type=allure.attachment_type.TEXT
                )

                # ✅ Determine checkbox and item type behavior
                untick_checkbox = (i >= 5)
                change_to_service = (i >= 5)

                self.add_single_product(
                    product_name, hs_code, stock_unit, purchase_price, sales_price,
                    barcode, supplier, untick_checkbox, change_to_service
                )

                writer.writerow([product_name, hs_code, stock_unit, purchase_price, sales_price, barcode, supplier])

    # --- Add single product ---
    def add_single_product(
            self, name, hs_code, stock_unit, purchase_price, sales_price, barcode,
            supplier, untick_checkbox=False, change_to_service=False
    ):
        wait = self.wait

        # Product Name
        name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Item Name']")))
        name_field.clear()
        name_field.send_keys(name)

        # HS Code
        hs_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter HS Code']")))
        hs_field.clear()
        hs_field.send_keys(hs_code)

        # Stock Unit
        unit_select = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='unit']")))
        Select(unit_select).select_by_visible_text(stock_unit)

        # Purchase & Sales Price
        purchase_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Purchase Price']")))
        purchase_input.clear()
        purchase_input.send_keys(str(purchase_price))

        sales_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='0' and @type='number'])[1]")))
        sales_input.clear()
        sales_input.send_keys(str(sales_price))

        # ✅ Handle Item Type Dropdown
        try:
            item_type_select = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='ptype']")))
            select = Select(item_type_select)
            if change_to_service:
                select.select_by_visible_text("SERVICE ITEM")
                print("🔄 Item Type changed to: SERVICE ITEM")
            else:
                print("🧾 Item Type kept as: INVENTORY ITEM")
        except Exception as e:
            print("⚠️ Item Type selection failed:", e)

        time.sleep(5)

        # ✅ Supplier selection (Fixed)
        try:
            supplier_field = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Press Enter to select']"))
            )
            # Scroll it into view to avoid interception by footer
            self.driver.execute_script("arguments[0].scrollIntoView(true);", supplier_field)
            time.sleep(1)

            # Use JS click instead of normal click
            self.driver.execute_script("arguments[0].click();", supplier_field)
            supplier_field.send_keys(Keys.ENTER)

            supplier_to_select = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//td[normalize-space(text())='Sujata Vendor']"))
            )
            ActionChains(self.driver).move_to_element(supplier_to_select).double_click(supplier_to_select).perform()
            print("✅ Supplier selected successfully: Sujata Vendor")

        except Exception as e:
            print("❌ Supplier selection failed:", e)

        time.sleep(5)

        # ✅ Handle checkbox tick/untick
        try:
            checkbox = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@type='checkbox' and contains(@class,'form-check-input')]"))
            )
            if untick_checkbox:
                if checkbox.is_selected():
                    checkbox.click()
                    print("☑️ Checkbox unticked for this product")
            else:
                print("✅ Checkbox left ticked for this product")
        except Exception as e:
            print("⚠️ Checkbox interaction failed:", e)

        # ✅ Save Product (Fixed)
        try:
            save_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='save']")))
            # Scroll into view in case footer or popup overlaps
            self.driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
            time.sleep(1)

            # Wait for it to be clickable
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='save']")))

            # Use JS click to avoid interception
            self.driver.execute_script("arguments[0].click();", save_btn)
            print("💾 Product saved successfully (via JS click).")
            time.sleep(3)

        except Exception as e:
            print("❌ Save button click failed:", e)

        # Handle alert
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            pass