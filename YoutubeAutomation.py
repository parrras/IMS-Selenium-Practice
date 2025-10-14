from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.youtube.com/")
driver.maximize_window()

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

# ---------------------------
# Click FaZe Rug's channel
# ---------------------------
channel_link_xpath = "//a[@id='main-link' and .//yt-formatted-string[normalize-space()='FaZe Rug']]"
channel_link = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, channel_link_xpath))
)
channel_link.click()
time.sleep(3)

# ---------------------------
# Click Videos tab
# ---------------------------
videos_tab_xpath = "//div[@class='yt-tab-shape__tab' and normalize-space()='Videos']"
videos_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, videos_tab_xpath))
)
videos_tab.click()
time.sleep(3)

# ---------------------------
# Gradual scrolling to target video
# ---------------------------
target_video_id = "ZHHtgsdRl7s"
scroll_pause = 1
max_scrolls = 50
video_clicked = False

for i in range(max_scrolls):
    # Get all currently loaded video links
    video_elements = driver.find_elements(By.XPATH, "//a[@id='thumbnail']")
    
    for video in video_elements:
        href = video.get_attribute("href")
        if href and target_video_id in href:
            # Scroll to the video visibly
            driver.execute_script("arguments[0].scrollIntoView(true);", video)
            time.sleep(1)
            # Click using JS
            driver.execute_script("arguments[0].click();", video)
            print("✅ Video clicked successfully!")
            video_clicked = True
            break
    
    if video_clicked:
        break
    
    # Scroll a bit more to load next set of videos
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(scroll_pause)

if not video_clicked:
    print("❌ Video not found after scrolling.")

time.sleep(10)
# driver.quit()
