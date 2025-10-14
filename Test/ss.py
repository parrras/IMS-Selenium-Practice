from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By


# Setup Chrome
options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.youtube.com/")

# ---------------------------
# Search for FaZe Rug
# ---------------------------
search_bar_xpath = "//input[@name='search_query' and contains(@class, 'yt-searchbox-input')]"
search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, search_bar_xpath))
)
search_bar.send_keys("FaZe Rug")
search_bar.send_keys(Keys.RETURN)
time.sleep(3)

# -----------------------------
# Take a screenshot
# -----------------------------
driver.save_screenshot("screenshot.png")   # saves screenshot in current folder
print("Screenshot saved as screenshot.png")

# Close browser
driver.quit()
