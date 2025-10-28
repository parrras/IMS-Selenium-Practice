import pytest
from selenium import webdriver
import allure

@pytest.fixture
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver

    if request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG
        )
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
