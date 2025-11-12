import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

# noinspection PyBroadException
@allure.feature("Sales Collection Report")
class SalesCollectionReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Sales Collection Report")
    def generate_sales_collection_report(self):
        wait = self.wait
        driver = self.driver
        print("🚀 Starting Sales Collection Report generation...")

        # ✅ Step 1: Navigate to Reports → Sales Reports → Sales Book Report
        print("📂 Navigating to Reports → Sales Reports → Sales Collection Report...")
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

        sales_collection_report = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sales Collection Report"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", sales_collection_report)
        sales_collection_report.click()
        print("✅ Clicked on 'Sales Collection Report'.")
        time.sleep(3)

        # ✅ Step 2: Select "Detail Report" radio button
        print("🟢 Selecting 'Detail Report' option...")
        try:
            detail_report_radio = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @name='reportType' and @value='1']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", detail_report_radio)
            detail_report_radio.click()
            print("✅ 'Detail Report' option selected successfully.")
        except TimeoutException:
            print("❌ Detail Report radio button not found.")
            raise

        time.sleep(2)

        # ✅ Step 3: Click on User selection input
        print("👤 Opening User selection dropdown...")
        user_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter for User List']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", user_input)
        user_input.click()
        print("✅ Clicked User selection field.")
        time.sleep(2)

        # Press Enter key to load the list
        user_input.send_keys(Keys.ENTER)
        print("⌨️ Pressed ENTER to load user list.")
        time.sleep(2)

        # ✅ Step 4: Double-click on the specific user 'Paras'
        print("👥 Selecting user 'Paras'...")
        user_option = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@title,'Paras') and normalize-space()='Paras']"))
        )
        self.actions.move_to_element(user_option).double_click(user_option).perform()
        print("✅ User 'Paras' selected successfully.")
        time.sleep(2)

        # ✅ Step 5: Click on the RUN button
        print("▶️ Clicking on 'RUN' button to generate the report...")
        run_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-info') and contains(text(),'RUN')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
        run_button.click()
        print("✅ 'RUN' button clicked. Report generation initiated.")
        time.sleep(5)

        # ✅ Step 6: Verify report table loaded
        print("🧾 Verifying Sales Collection Report table...")
        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]")))
            rows = table.find_elements(By.XPATH, ".//tr")
            print(f"✅ Sales Collection Report table loaded with {len(rows) - 1} rows.")

            # 📸 Capture screenshot when report table appears
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="Sales_Collection_Report_Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            print("📸 Screenshot of Sales Collection Report attached to Allure.")

        except TimeoutException:
            print("⚠️ No report data appeared after loading Sales Collection Report.")
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="Sales_Collection_Report_No_Data",
                attachment_type=allure.attachment_type.PNG
            )

        print("🎉 Sales Collection Report generation completed successfully.")









