from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ---------------------------
# Chrome options
# ---------------------------
options = Options()
options.add_experimental_option("detach", True)  # keeps browser open
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # suppress warnings

# Initialize ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

driver.get("https://www.neuralnine.com/")
driver.maximize_window()

# ---------------------------
# Click the "Books" link
# ---------------------------
try:
    links = driver.find_elements(By.XPATH, "//a[@href]")
    for link in links:
        if "Books" in link.text:
            driver.execute_script("arguments[0].scrollIntoView(true);", link)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", link)
            print("Clicked on 'Books' link successfully!")
            break
except Exception as e:
    print("Error clicking 'Books' link:", e)

# ---------------------------
# Wait for the book image "7 in 1" and click
# ---------------------------
try:
    book_image_xpath = "//img[@src='https://neuralnine.com/wp-content/uploads/2025/04/7in1.png']"

    book_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, book_image_xpath))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", book_image)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", book_image)
    print("Clicked on the '7 in 1' book image successfully!")

except Exception as e:
    print("Error clicking on the '7 in 1' book image:", e)

# ---------------------------
# Switch to the new tab/window
# ---------------------------
try:
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[1])
    print("Switched to the new window/tab successfully!")
except Exception as e:
    print("Error switching to new window/tab:", e)

# ---------------------------
# Optional: wait to see the new page
# ---------------------------
time.sleep(5)

# driver.quit()  # leave commented if you want browser to stay open
