from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# --- Initialize Chrome driver ---
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

# --- Helper functions ---
def scroll_and_click(element):
    """Scroll element into view and click using JavaScript."""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.execute_script("arguments[0].click();", element)

def hover_and_click(element):
    """Hover over the element and click using ActionChains."""
    ActionChains(driver).move_to_element(element).click().perform()

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

# --- Wait for dashboard to load ---
time.sleep(5)

# --- Logout if exists ---
try:
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
    )
    scroll_and_click(logout_button)
    driver.find_element(By.CLASS_NAME, "btn-auth").click()
    time.sleep(5)
except TimeoutException:
    print("No logout button found")

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

# --- Click on "Customer Master" ---
customer_master = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Customer Master"))
)
customer_master.click()

# --- Click on "Create Customer" ---
try:
    create_customer = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='create']"))
    )
    scroll_and_click(create_customer)
    print("✅ Clicked 'Create Customer'")
    time.sleep(2)
except TimeoutException as e:
    print("❌ Could not click 'Create Customer':", e)
    driver.quit()
    exit()

# --- Fill Customer Details ---
try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='customerName']"))).send_keys("Rahul Pade")
    driver.find_element(By.XPATH, "//input[@id='address']").send_keys("Jhapa Nepal")
    driver.find_element(By.XPATH, "//input[@id='vatNo']").send_keys("220011")
    driver.find_element(By.XPATH, "//input[@id='email']").send_keys("paderahul@gmail.com")
    driver.find_element(By.XPATH, "//input[@id='Mobile']").send_keys("9812321611")
    print("✅ Filled all customer details")
except TimeoutException as e:
    print("❌ Failed to fill customer details:", e)
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
time.sleep(300)
driver.quit()
