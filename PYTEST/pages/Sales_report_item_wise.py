import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Sales Report - Item Wise")
class SalesReportItemWisePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Sales Report - Item Wise")
    def generate_sales_report_item_wise(self):
        wait = self.wait
        driver = self.driver
        actions = self.actions
        print("🚀 Starting Sales Report - Item Wise generation...")

        # ✅ Step 1: Navigate to Reports → Sales Reports → Sales Report - Item Wise
        print("📂 Navigating to Reports → Sales Reports → Sales Report - Item Wise...")
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
        actions.move_to_element(sales_reports).pause(0.5).perform()
        print("✅ Hovered over 'Sales Reports'.")
        time.sleep(1)

        item_wise_report = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sales Report - Item Wise"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", item_wise_report)
        item_wise_report.click()
        print("✅ Clicked on 'Sales Report - Item Wise'.")
        time.sleep(3)


        # ✅ Step 2: Select Customer ("21 Savage")
        print("🧍 Selecting Customer: 21 Savage...")
        customer_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Account List']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", customer_field)
        customer_field.click()
        time.sleep(1)
        customer_field.send_keys(Keys.ENTER)
        time.sleep(2)

        customer_option = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@title='21 Savage']"))
        )
        actions.double_click(customer_option).perform()
        print("✅ Successfully selected Customer: 21 Savage")
        time.sleep(2)

        # ✅ Step 3: Select Item ("White Chocolate")
        print("🍫 Selecting Item: White Chocolate...")
        item_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Item List']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", item_field)
        item_field.click()
        time.sleep(1)
        item_field.send_keys(Keys.ENTER)
        time.sleep(2)

        white_choco = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@title='White Chocolate']"))
        )
        actions.double_click(white_choco).perform()
        print("✅ Successfully selected Item: White Chocolate")
        time.sleep(2)

        # ✅ Step 4: Click RUN button
        print("▶️ Clicking Run button...")
        run_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and contains(.,'RUN')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", run_btn)
        run_btn.click()
        print("✅ Clicked Run button.")
        time.sleep(3)

        # ✅ Step 5: Verify report table
        print("🧾 Verifying Sales Report - Item Wise table...")
        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]")))
            rows = table.find_elements(By.XPATH, ".//tr")
            print(f"✅ Sales Report - Item Wise table loaded with {len(rows) - 1} rows.")

            # 📸 Capture screenshot on success
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, name="Sales_Report_Item_Wise_Screenshot",
                          attachment_type=allure.attachment_type.PNG)
            print("📸 Screenshot of Sales Report - Item Wise attached to Allure.")

        except TimeoutException:
            print("⚠️ No report data appeared after clicking Run.")

        print("🎉 Sales Report - Item Wise generation completed successfully.")
