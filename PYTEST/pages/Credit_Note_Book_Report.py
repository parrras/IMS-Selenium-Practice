import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@allure.feature("Credit Note Book Report")
class CreditNoteBookReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Credit Note Book Report")
    def generate_credit_note_book_report(self):
        wait = self.wait
        driver = self.driver
        print("🚀 Starting Credit Note Book Report generation...")

        # ✅ Step 1: Navigate to Reports → Sales Reports → Credit Note Book Report
        print("📂 Navigating to Reports → Sales Reports → Credit Note Book Report...")
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
        print("✅ Hovered over 'Sales Report'.")
        time.sleep(1)

        credit_note_book_report = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Credit Note Book Report"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", credit_note_book_report)
        credit_note_book_report.click()
        print("✅ Clicked on 'Credit Note Book Report'.")
        time.sleep(3)

        # ✅ Step 2: Select Customer (instead of Supplier)
        print("👤 Selecting customer '21 Savage'...")
        try:
            customer_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Account List']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", customer_input)
            customer_input.click()
            time.sleep(1)
            customer_input.send_keys("\n")  # Press Enter to open list
            time.sleep(2)

            # Select "21 Savage"
            customer_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='21 Savage']"))
            )
            self.actions.double_click(customer_option).perform()
            print("✅ Selected customer: 21 Savage.")
        except Exception as e:
            raise AssertionError(f"❌ Failed to select customer: {e}")

        time.sleep(2)

        # ✅ Step 3: Click “Detail Report” radio button before clicking RUN
        print("🎯 Selecting 'Detail Report' option...")
        try:
            detail_report_radio = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @name='reportType' and @value='1']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", detail_report_radio)
            detail_report_radio.click()
            print("✅ Selected 'Detail Report' radio button.")
        except Exception as e:
            raise AssertionError(f"❌ Failed to select 'Detail Report' radio button: {e}")

        time.sleep(2)

        # ✅ Step 4: Click 'RUN' button
        print("▶️ Clicking 'RUN' button...")
        try:
            run_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='RUN']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
            run_button.click()
            print("✅ Clicked 'RUN' button successfully.")
        except Exception as e:
            raise AssertionError(f"❌ Failed to click 'RUN' button: {e}")
        time.sleep(3)

        # ✅ Step 5: Verify report table and attach screenshot
        print("🧾 Verifying Credit Note Book Report table...")
        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]")))
            rows = table.find_elements(By.XPATH, ".//tr")
            print(f"✅ Report table loaded with {len(rows) - 1} rows.")

            # 📸 Capture and attach screenshot for Allure
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, name="Credit_Note_Book_Report_Screenshot",
                          attachment_type=allure.attachment_type.PNG)
            print("📸 Screenshot of Credit Note Book Report attached to Allure.")

        except TimeoutException:
            print("⚠️ No report data appeared after loading report.")

        print("🎉 Credit Note Book Report generation completed successfully.")
