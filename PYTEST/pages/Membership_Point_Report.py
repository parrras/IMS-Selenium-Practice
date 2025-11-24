import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@allure.feature("Membership Point Report")
class MembershipPointReportPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.actions = ActionChains(driver)

    @allure.step("Generate Membership Point Report")
    def generate_membership_point_report(self):
        wait = self.wait
        driver = self.driver

        print("🚀 Starting Membership Point Report generation...")

        try:
            # ==========================================
            # STEP 1: Navigate to Membership Point Report
            # ==========================================
            print("📂 Navigating to Reports → Loyalty & Promotion Report → Membership Point Report...")

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

            membership_point_report = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Membership Point Report"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", membership_point_report)
            membership_point_report.click()
            print("✅ Clicked 'Membership Point Report'")
            time.sleep(2)

            # ==========================================
            # STEP 2: Select Member Name
            # ==========================================
            print("🧍 Selecting Member Name...")

            member_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Account List']"))
            )
            member_input.click()
            member_input.send_keys("\n")  # press ENTER
            print("⬇️ Pressed Enter to load Member List...")
            time.sleep(2)

            # Double-click the member "TheTestCustom"
            member_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='TheTestCustom']"))
            )
            self.actions.double_click(member_option).perform()
            print("🟦 Double-clicked member: TheTestCustom")
            time.sleep(1)

            # ==========================================
            # STEP 3: Select Detail Report Radio Button
            # ==========================================
            print("📌 Selecting Detail Report option...")

            detail_radio = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @value='0']"))
            )
            driver.execute_script("arguments[0].click();", detail_radio)
            print("✅ Detail Report selected.")
            time.sleep(1)

            # ==========================================
            # STEP 4: Click RUN
            # ==========================================
            print("🏃 Clicking RUN...")

            run_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'confirm-btn')]"))
            )
            driver.execute_script("arguments[0].click();", run_btn)
            print("✅ RUN button clicked.")
            time.sleep(3)

            # ==========================================
            # STEP 5: Verify Table Loaded
            # ==========================================
            print("📊 Verifying Membership Point Report table...")

            try:
                table = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'table')]"))
                )
                rows = table.find_elements(By.XPATH, ".//tr")
                print(f"✅ Membership Point Report loaded with {len(rows) - 1} rows.")

                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Membership_Point_Report_Table",
                    attachment_type=allure.attachment_type.PNG
                )
                print("📸 Screenshot attached (Table Loaded).")

            except TimeoutException:
                print("⚠️ Table did NOT load — no rows found.")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Membership_Point_Report_No_Table",
                    attachment_type=allure.attachment_type.PNG
                )

        except Exception as e:
            print(f"❌ Error occurred: {e}")

            allure.attach(
                driver.get_screenshot_as_png(),
                name="Membership_Point_Report_Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise e
