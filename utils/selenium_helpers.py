from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_chrome_driver():
    """Set up Chrome options to run headless (= without opening a browser window)"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    # driver.implicitly_wait(0.5)
    driver.set_window_size(2560, 1080)
    return driver


def click_button(driver, button_xpath):
    button = driver.find_element(By.XPATH, button_xpath)
    button.click()
