import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def setup():
    """Setup Chrome driver for tests"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.add_argument("--disable-gpu")  # sometimes helps Windows
    # chrome_options.add_argument("--headless")  # optional for CI/CD

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(10)  # increased for stability
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot on failure for Allure"""
    outcome = yield
    report = outcome.get_result()

    if report.failed:  # captures both "setup" and "call" phase failures
        driver = None

        if "setup" in item.funcargs:
            driver = item.funcargs["setup"]

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
