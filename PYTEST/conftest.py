import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def setup():
    """Setup Chrome driver for tests"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-allow-origins=*")  # fix for Selenium 4.35+
    # chrome_options.add_argument("--headless")  # Uncomment for CI/CD

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.implicitly_wait(15)  # slightly higher for slower pages
    yield driver
    print("🔹 Quitting browser after test")
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot to Allure on test failure"""
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        driver = item.funcargs.get("setup", None)
        if driver:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"Screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                print(f"📸 Screenshot attached for failed test: {item.name}")
            except Exception as e:
                print(f"[Allure Screenshot Error] {e}")
