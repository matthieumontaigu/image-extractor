def get_chrome_driver():
    """Set up Chrome options to run headless (= without opening a browser window)"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    # driver.implicitly_wait(0.5)
    driver.set_window_size(2560, 1080)
    return driver


def click_button(driver, button_xpath):
    from selenium.webdriver.common.by import By

    button = driver.find_element(By.XPATH, button_xpath)
    button.click()
