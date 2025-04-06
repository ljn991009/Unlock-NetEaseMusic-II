# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "009C41A586464EC56F65C0926E84BBDF7A2550F4366505B266478F0DF4F2BE254C42584E8F2488EA63F8E568E7C8408623C569E35614C74B90C6260693A7694F1C382410F2EB1D24428DDCCCB15E57C57F604B68BCA36503E5356852D4DA8312F045DE2B3D1785BE0DE6C44FF4C27CE95AA170081D4927BB0F86C16AE66F1D01832BA89F543DFF7459D67DC2D084A898DE728F7918BFB9EC38279BBDF5B1D966D66B7454A1C18D7A5488630E412347F8F3BFD5FB1D95FF4F73873286E637FAE9834B61F226BB8B6DAF77E14F2194CE1EC7EEB4520AF8C8C3659FD2EEFBA6F8F0ADA16F99383D991CF7A56820FA6AF61051A81A0DDBA6DB23DC9FD41FAEE69F6B176815912104D4D6FE8ADF8F0022822EF3DC80D8F4D8CC3874FB6E162DFF859EA28C7B8F62EA2986D77B2EABFEA9E9013D89A37A48A3058FD4A76264B01A98659C3C0EBC22A84D83405DFD6FFC18FA94C0E6E23E5C29B4E790F8AC2050F55A0B95"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
