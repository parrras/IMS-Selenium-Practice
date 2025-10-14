from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- Initialize Chrome driver ---
driver = webdriver.Chrome()
driver.maximize_window()

# --- Explicit wait (single instance) ---
wait = WebDriverWait(driver, 30)  # <-- Line 9: only one wait object

# --- Helper functions ---
def scroll_and_click(element):
    """Scroll element into view and click using JavaScript."""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.execute_script("arguments[0].click();", element)

def hover_and_click(element):
    """Hover over the element and click using ActionChains."""
    ActionChains(driver).move_to_element(element).click().perform()

def wait_for_overlay_to_disappear():
    """Wait until any overlay/backdrop is gone."""
    try:
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, "cdk-overlay-backdrop")))
    except TimeoutException:
        pass  # Overlay not present or already gone

# --- Navigate to the site ---
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

# --- Wait for dashboard to load and handle logout ---
try:
    logout_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
    )
    scroll_and_click(logout_button)

    # Wait for any overlay to disappear before clicking btn-auth
    wait_for_overlay_to_disappear()
    scroll_and_click(driver.find_element(By.CLASS_NAME, "btn-auth"))
except TimeoutException:
    print("No logout button found or btn-auth not clickable")

# --- Hover over "Customer & Vendor Info" ---
try:
    customer_vendor_info = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Customer & Vendor Info"))
    )
    hover_and_click(customer_vendor_info)
except Exception as e:
    print("❌ Failed to hover over 'Customer & Vendor Info':", e)
    driver.quit()
    exit()

# --- Click on "Vendor Master" ---
vendor_master = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Vendor Master"))
)
vendor_master.click()

# --- Click on "Create Vendor" ---
try:
    create_vendor = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='create']"))
    )
    scroll_and_click(create_vendor)
    print("✅ Clicked 'Create Vendor'")
except TimeoutException as e:
    print("❌ Could not click 'Create Vendor':", e)
    driver.quit()
    exit()

# --- Fill Vendor Details ---
try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='vendorName']"))).send_keys("Rookie Samuel")
    driver.find_element(By.XPATH, "//input[@id='address']").send_keys("Texas States")
    driver.find_element(By.XPATH, "//input[@id='vatNo']").send_keys("111122998")
    driver.find_element(By.XPATH, "//input[@id='email']").send_keys("Tektek@gmail.com")
    driver.find_element(By.XPATH, "//input[@id='Mobile']").send_keys("9211334411")
    print("✅ Filled all vendor details")
except TimeoutException as e:
    print("❌ Failed to fill vendor details:", e)
    driver.quit()
    exit()

# --- Click Save ---
try:
    save_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='save']"))
    )
    scroll_and_click(save_button)
    print("✅ Clicked 'SAVE' button")
except TimeoutException as e:
    print("❌ Could not click 'SAVE':", e)

# --- Keep browser open for inspection ---
driver.implicitly_wait(5)
driver.quit()
