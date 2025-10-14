from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# ✅ Helper: scroll and click
def scroll_and_click(element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", element)

# ✅ Initialize driver
driver = webdriver.Chrome()
driver.set_window_size(1400, 900)
wait = WebDriverWait(driver, 25)
actions = ActionChains(driver)

# --- Navigate to site ---
driver.get("https://grn.variantqa.himshang.com.np/#/login")

# --- LOGIN ---
wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[2]/input"))
).send_keys("Paras")

driver.find_element(
    By.XPATH, "/html/body/app/div/ng-component/div/form/div/div[3]/input"
).send_keys("Ims@12345")

driver.find_element(
    By.XPATH, "//button[normalize-space(text())='Sign In']"
).click()
print("✅ Logged in successfully.")

# --- Wait for dashboard to load ---
time.sleep(5)

# --- Optional: logout handling ---
# noinspection PyBroadException
try:
    logout_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
    )
    logout_button.click()
    print("🔄 Logged out successfully.")

    ok_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and normalize-space(text())='OK']"))
    )
    ok_button.click()
    print("✅ Clicked OK on the confirmation dialog.")

    time.sleep(5)
    driver.find_element(By.CLASS_NAME, "btn-auth").click()
    print("✅ Re-logged in.")
except:
    print("➡️ Logout button not found, continuing...")

# --- Click on 'Reports' ---
try:
    report_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(normalize-space(),'Reports')]"))
    )
    scroll_and_click(report_button)
    print("✅ Clicked 'Reports'.")
    time.sleep(3)
except TimeoutException:
    print("❌ Could not find 'Reports' button.")
    driver.quit()
    exit()

# --- Hover or click 'Purchase Reports' safely ---
# noinspection PyBroadException
try:
    # Try locating by exact LINK_TEXT first
    purchase_reports = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Reports"))
    )
except:
    # Fallback to PARTIAL_LINK_TEXT
    # noinspection PyBroadException
    try:
        purchase_reports = wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Purchase Reports"))
        )
    except:
        # Last fallback: XPATH
        purchase_reports = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Purchase Reports']"))
        )

# 🪄 FIXED: Scroll into view before hovering
driver.execute_script("arguments[0].scrollIntoView(true);", purchase_reports)
ActionChains(driver).move_to_element(purchase_reports).pause(0.3).perform()
print("✅ Hovered over 'Purchase Reports'.")
time.sleep(1)  # wait for dropdown to appear

# --- Click on 'Purchase Book Report' ---
purchase_book_report = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Book Report"))
)
# 🪄 FIXED: ensure visibility before click
driver.execute_script("arguments[0].scrollIntoView(true);", purchase_book_report)
wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Book Report"))).click()
print("✅ Clicked on 'Purchase Book Report'.")
time.sleep(10)

# ============================
# 🧾 FILLING THE REPORT FORM
# ============================

# --- Select Cost Center -> Test QA ---
try:
    # Wait for the dropdown to be present
    dropdown = wait.until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@class, 'form-control input-text')]"))
    )

    dropdown.click()
    # Initialize Select object
    select = Select(dropdown)
    time.sleep(5)

    # Select by visible text
    select.select_by_visible_text("Test QA")
    print("✅ Selected 'Test QA' from the dropdown.")

except Exception as e:
    print("❌ Failed to select 'Test QA':", e)

# --- Select Warehouse -> Main Warehouse ---
try:
    # Wait for the dropdown to appear
    warehouse_dropdown = wait.until(
        EC.presence_of_element_located((By.XPATH, "//select[@class='form-control input-text ng-untouched ng-pristine ng-valid']"))
    )
    warehouse_dropdown.click()
    # Initialize Select object
    select_warehouse = Select(warehouse_dropdown)
    time.sleep(5)


    # Select by visible text
    select_warehouse.select_by_visible_text("Main Warehouse")
    print("✅ Selected 'ALL' from the dropdown.")

except Exception as e:
    print("❌ Failed to select 'ALL':", e)

# --- Supplier Selection ---
try:
    supplier_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Press Enter or Tab for Account List']"))
    )
    scroll_and_click(supplier_input)
    supplier_input.send_keys("\n")  # press Enter to open supplier list
    print("✅ Opened Supplier List.")
    time.sleep(2)

    supplier_to_select = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='ABC SUPPLIER PVT. LTD.']"))
    )
    actions.move_to_element(supplier_to_select).double_click().perform()
    print("✅ Selected Supplier: ABC SUPPLIER PVT. LTD.")
except Exception as e:
    print("❌ Failed to select Supplier:", e)
    driver.quit()
    exit()

try:
    run_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='RUN']"))
    )
    scroll_and_click(run_button)
    print("✅ Clicked on 'Run' button.")
except Exception as e:
    print("❌ Failed to click 'Run' button:", e)

# --- Click 'Load Report' ---
try:
    load_report = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='option-card']//span[text()='Load Report']"))
    )
    scroll_and_click(load_report)
    print("✅ Clicked on 'Load Report' button.")
except Exception as e:
    print("❌ Failed to click 'Load Report':", e)


# --- Keep browser open to verify ---
time.sleep(300)
driver.quit()
