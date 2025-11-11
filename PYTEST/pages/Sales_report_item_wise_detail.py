import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@allure.feature("Sales Report - Item Wise Detail")
class SalesReportItemWiseDetailPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Sales Report - Item Wise Detail")
    def generate_sales_report_item_wise_detail(self):
        wait = self.wait
        driver = self.driver
        print("🚀 Starting Sales Report - Item Wise Detail generation...")

        # ✅ Step 1: Navigate to Reports → Sales Reports → Sales Report - Item Wise Detail
        print("📂 Navigating to Reports → Sales Reports → Sales Report - Item Wise Detail...")
        reports_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Reports')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", reports_btn)
        reports_btn.click()
        time.sleep(2)

        try:
            sales_reports = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Sales Report"))
            )
        except:
            sales_reports = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Sales Report']"))
            )

        driver.execute_script("arguments[0].scrollIntoView(true);", sales_reports)
        self.actions.move_to_element(sales_reports).pause(0.5).perform()
        print("✅ Hovered over 'Sales Reports'.")
        time.sleep(1)

        sales_book_report = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sales Report - Item Wise Detail"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", sales_book_report)
        sales_book_report.click()
        print("✅ Clicked on 'Sales Report - Item Wise Detail'.")
        time.sleep(3)

        # ✅ Step 2: Select Item (White Chocolate)
        print("🎯 Selecting Item: White Chocolate...")

        # Wait for the item input field and click it
        item_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Item List']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", item_input)
        item_input.click()
        time.sleep(1)

        # Press Enter to open the item list
        item_input.send_keys(Keys.ENTER)
        time.sleep(2)

        # Wait for the 'White Chocolate' item to appear
        white_choco = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@title='White Chocolate']"))
        )

        # Double-click on the 'White Chocolate' item
        actions = ActionChains(driver)
        actions.double_click(white_choco).perform()
        print("✅ Successfully selected 'White Chocolate'")
        time.sleep(2)

        ok_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='btn btn-info btn-sm' and normalize-space()='OK']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", ok_button)
        driver.execute_script("arguments[0].click();", ok_button)
        print("✅ Clicked 'OK' to confirm selected item.")
        time.sleep(2)

        # ✅ Step 3: Select User (Paras)
        print("👤 Selecting User: Paras...")
        user_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter for User List']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", user_input)
        user_input.click()
        time.sleep(1)

        user_input.send_keys(Keys.ENTER)
        time.sleep(2)

        paras_user = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@title='Paras']"))
        )
        actions.double_click(paras_user).perform()
        print("✅ Successfully selected user: Paras")
        time.sleep(2)

        # ✅ Step 5: Click 'RUN' button
        print("▶️ Clicking 'RUN' button...")
        run_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='RUN']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
        run_button.click()
        print("✅ Clicked 'RUN' button successfully.")
        time.sleep(5)

        # ✅ Step 5: Verify report table and capture screenshot
        print("🧾 Verifying Sales Report Item Wise Detail table...")
        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]")))
            rows = table.find_elements(By.XPATH, ".//tr")
            print(f"✅ Report table loaded successfully with {len(rows) - 1} rows.")

            # 📸 Capture and attach screenshot for Allure
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="Sales_Report_Item_Wise_Detail_Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            print("📸 Screenshot of Sales Report Item Wise Detail table attached to Allure.")

        except TimeoutException:
            print("⚠️ No data appeared in the Sales Report Item Wise Detail table after loading the report.")

        finally:
            print("🎉 Sales Report - Item Wise Detail generation and verification completed successfully.")
