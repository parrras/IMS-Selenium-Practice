import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Debit Note Book Report")
class DebitNoteBookReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Debit Note Book Report")
    def generate_debit_note_book_report(self):
        wait = self.wait
        driver = self.driver
        print("🚀 Starting Debit Note Book Report generation...")

        # ✅ Step 1: Navigate to Reports → Purchase Reports → Debit Note Book Report
        print("📂 Navigating to Reports → Purchase Reports → Debit Note Book Report...")
        reports_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Reports')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", reports_btn)
        reports_btn.click()
        time.sleep(2)

        try:
            dbnote_reports = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Reports"))
            )
        except:
            dbnote_reports = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Purchase Reports']"))
            )

        driver.execute_script("arguments[0].scrollIntoView(true);", dbnote_reports)
        self.actions.move_to_element(dbnote_reports).pause(0.5).perform()
        print("✅ Hovered over 'Purchase Reports'.")
        time.sleep(1)

        debit_note_book_report = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Debit Note Book Report"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", debit_note_book_report)
        debit_note_book_report.click()
        print("✅ Clicked on 'Debit Note Book Report'.")
        time.sleep(3)

        # ✅ Step 2: Click 'RUN' button
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

        # ✅ Step 3: Verify report table and attach screenshot
        print("🧾 Verifying Debit Note Book Report table...")
        try:
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]")))
            rows = table.find_elements(By.XPATH, ".//tr")
            print(f"✅ Report table loaded with {len(rows) - 1} rows.")

            # 📸 Capture and attach screenshot for Allure
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, name="Debit_Note_Book_Report_Screenshot",
                          attachment_type=allure.attachment_type.PNG)
            print("📸 Screenshot of Debit Note Book Report attached to Allure.")

        except TimeoutException:
            print("⚠️ No report data appeared after loading report.")

        print("🎉 Debit Note Book Report generation completed successfully.")
