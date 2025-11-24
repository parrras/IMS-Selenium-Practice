import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# noinspection PyBroadException
@allure.feature("Sales Report Membership Wise")
class SalesReportMembershipWisePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Sales Report Membership Wise")
    def generate_sales_report_membership_wise(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Sales Report Membership Wise generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Sales Report Membership Wise
            # ==========================================
            print("📂 Navigating to Reports → Loyalty & Promotion Report → Sales Report Membership Wise...")

            reports_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Reports')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", reports_btn)
            reports_btn.click()
            time.sleep(1)

            try:
                loyalty_and_promotion_report = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Loyalty & Promotion Report"))
                )
            except:
                loyalty_and_promotion_report = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Loyalty & Promotion Report']"))
                )

            driver.execute_script("arguments[0].scrollIntoView(true);", loyalty_and_promotion_report)
            self.actions.move_to_element(loyalty_and_promotion_report).pause(0.4).perform()
            print("✅ Hovered over 'Loyalty & Promotion Report'.")
            time.sleep(1)

            sales_report_membership = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Sales Report - Membership Wise"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", sales_report_membership)
            sales_report_membership.click()
            print("✅ Clicked 'Sales Report - Membership Wise'")
            time.sleep(2)

            # ==========================================
            # STEP 2: Select Member
            # ==========================================
            print("🧍 Selecting member input...")

            member_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Member List']"))
            )
            member_input.click()
            time.sleep(0.5)
            member_input.send_keys("\n")  # Press ENTER to load list
            print("✅ Member list opened")
            time.sleep(1)

            # ==========================================
            # STEP 3: Double-click Member "TheTestCustom"
            # ==========================================
            print("🖱️ Selecting member 'TheTestCustom'...")

            member_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='TheTestCustom']"))
            )
            self.actions.double_click(member_option).perform()
            print("✅ Double-clicked member 'TheTestCustom'")
            time.sleep(1)

            # ==========================================
            # STEP 4: Select Detail Report Radio
            # ==========================================
            print("📌 Selecting 'Detail Report'...")

            detail_report_radio = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @name='reportType' and @value='1']"))
            )
            driver.execute_script("arguments[0].click();", detail_report_radio)
            print("✅ Detail Report selected")
            time.sleep(1)

            # ==========================================
            # STEP 5: Click RUN Button
            # ==========================================
            print("🏃 Clicking RUN button...")

            run_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'confirm-btn') and text()='RUN']"))
            )
            run_button.click()
            print("✅ RUN button clicked")
            time.sleep(4)

            # ==========================================
            # STEP 6: Verify Table Loaded
            # ==========================================
            print("📊 Verifying Sales Report Membership Wise table...")

            try:
                table = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]"))
                )
                rows = table.find_elements(By.XPATH, ".//tr")
                print(f"✅ Report table loaded with {len(rows) - 1} rows.")

                # Attach screenshot
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Sales_Report_Membership_Wise_Table",
                    attachment_type=allure.attachment_type.PNG
                )
                print("📸 Screenshot attached to Allure.")

            except TimeoutException:
                print("⚠️ Table did NOT load — no rows found.")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Sales_Report_Membership_Wise_No_Table",
                    attachment_type=allure.attachment_type.PNG
                )

        except Exception as e:
            print(f"❌ Error occurred: {e}")

            # Attach failure screenshot
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Sales_Report_Membership_Wise_Error",
                attachment_type=allure.attachment_type.PNG
            )

            raise e
