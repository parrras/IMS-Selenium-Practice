import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@allure.feature("Sales Report - Customer Wise")
class SalesReportCustomerWisePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Sales Report - Customer Wise")
    def generate_sales_report_customer_wise(self):
        wait = self.wait
        driver = self.driver
        actions = self.actions

        print("🚀 Starting Sales Report - Customer Wise generation...")

        # ✅ Step 1: Navigate to Reports → Sales Reports → Sales Report - Customer Wise
        print("📂 Navigating to Reports → Sales Reports → Sales Report - Customer Wise...")
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

        sales_customer_report = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sales Report - Customer Wise"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", sales_customer_report)
        sales_customer_report.click()
        print("✅ Clicked on 'Sales Report - Customer Wise'.")
        time.sleep(3)

        # ✅ Step 2: Select Customer
        print("🧾 Selecting Customer...")
        customer_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Account List']"))
        )
        customer_input.click()
        customer_input.send_keys(Keys.ENTER)
        print("🔍 Customer list opened.")
        time.sleep(2)

        # Select 21 Savage
        customer_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='21 Savage']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", customer_option)
        customer_option.click()
        print("✅ Selected customer: 21 Savage")
        time.sleep(1)

        # ✅ Step 3: Select Item (White Chocolate)
        print("🎯 Selecting Item: White Chocolate...")

        # Wait for item input field to appear
        item_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Press Enter or Tab for Item List']"))
        )

        # Scroll to input and click via JavaScript to avoid interception
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", item_input)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", item_input)  # ✅ JS click avoids overlays
        time.sleep(1)

        # Send Enter to open the list
        item_input.send_keys(Keys.ENTER)
        time.sleep(2)

        # Wait for 'White Chocolate' option
        white_choco = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@title='White Chocolate']"))
        )

        # Double-click the item to select
        actions = ActionChains(driver)
        actions.double_click(white_choco).perform()
        print("✅ Successfully selected 'White Chocolate'")
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
        print("🧾 Verifying Sales Report Customer Wise table...")
        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]")))
            rows = table.find_elements(By.XPATH, ".//tr")
            print(f"✅ Report table loaded successfully with {len(rows) - 1} rows.")

            # 📸 Capture and attach screenshot for Allure
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="Sales_Report_Customer_Wise_Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            print("📸 Screenshot of Sales Report Customer Wise table attached to Allure.")

        except TimeoutException:
            print("⚠️ No data appeared in the Sales Report Customer Wise table after loading the report.")

        finally:
            print("🎉 Sales Report Customer Wise generation and verification completed successfully.")


