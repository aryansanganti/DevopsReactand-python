import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def driver():
    options = Options()

    # Use headless mode for Jenkins/CI
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    driver.implicitly_wait(10)

    yield driver

    driver.quit()


def test_google_title(driver):
    driver.get("https://www.google.com")

    assert "Google" in driver.title


def test_search_interaction(driver):
    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")

    search_box.send_keys(
        "Continuous Integration with Jenkins"
    )

    assert len(search_box.get_attribute("value")) > 0
    