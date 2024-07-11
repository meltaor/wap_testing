import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome options to use mobile emulator
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})

@pytest.fixture
def driver():
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    yield driver
    # Teardown: Quit WebDriver after each test
    driver.quit()

def test_twitch_streamer(driver):
    """
    Test case for searching and interacting with Twitch streamers on the mobile site.

    Steps:
    1. Go to https://m.twitch.tv/
    2. Handle modal dialogs if they appear
    3. Click on the search icon
    4. Input "StarCraft II" in the search field
    5. Scroll down 2 times
    6. Select the first streamer from the search results
    7. Take a screenshot
    """
    driver.get("https://m.twitch.tv/")  # Mobile site URL

    # Handle modal dialogs if they appear
    try:
        close_modal = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close"]'))
        )
        close_modal.click()
        print("Closed modal dialog successfully")
    except:
        print("No modal dialog to close")

    # Click on search icon
    search_icon_xpath = '//a[@aria-label="Search"]'
    search_icon = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, search_icon_xpath))
    )
    search_icon.click()

    # Input "StarCraft II" in the search field
    search_input_xpath = '//input[@type="search"][@placeholder="Search..."]'
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, search_input_xpath))
    )
    search_input.send_keys("StarCraft II")
    search_input.send_keys(Keys.RETURN)

    # Scroll down 2 times
    scroll_count = 2
    for i in range(scroll_count):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1)
    streamers = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/videos")]'))
    )
    if streamers:
        streamers[0].click()

    # Take a screenshot
    time.sleep(5)  # Wait for the page to load
    driver.save_screenshot("tests/screenshots/streamer_page.png")

# Ensure the test runs with pytest when executed directly
if __name__ == "__main__":
    pytest.main()
