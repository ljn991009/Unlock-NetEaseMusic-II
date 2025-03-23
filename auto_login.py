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
    browser.add_cookie({"name": "MUSIC_U", "value": "0058FF11E544C8F6E3FF2D72BA7E9F4F67830008025BBE0A9E5A3564344DA89939CBE34565C54717A87783F0755E099693853F5F90CDA0F5E62A0B2C89EAB4B8D0F8C7D1F4AD4F5B630DA0A9A778D793B203A226F32F8B223C2609B0718DBD47B06FF1487C5E73EF8AE71F30449C391DE7BA3E4DFF0322DED6900E9FA0B85C6265A71526F5420FD2061E362E39F7FA91EDFCA256FB36157A7C09EDFCC8D4A7F0532DAE17C89745EFFF591154300ABC3572C790B2592898EB409A9D881E902944EF2F923BEA9E73C6328ADEE5E085A9098EE82F05DB9A1592C1B1BE933C0358AE74629164DD5D49C8C44CB4161C3547435247F9C8D5674959E0BCB1BEA695E51396BBBD4FCE6A5017271EFA24CC6202385DBAEF56135AE886A047244BB9A93E430DF4E3C51DEACC23436CAB9491CC31D92BF8198E1E9ED218CE977E9A8AECB2E8B86A83896CF447F49A89200D8C8FA5F32E6B70AEBDED866774CB27B5C87F4CA5FA"})
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
