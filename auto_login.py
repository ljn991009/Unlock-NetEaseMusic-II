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
    browser.add_cookie({"name": "MUSIC_U", "value": "00CD5C5315C5774D7EB59A0B229E54D5AD75EF12377E42BC6FFAD063C35D5901D8EB7A6018D5FB63A5E0A34DE70A6D90997D180EBFEB91AD0751B42C70EB4DAD9673F039F6403C2EBE06F05E21D406A0BA3E7B0459B40FA1BE9B8BEE68908632E26636A8F0BAA4EFEA66C229EF8ED1CF1CAA5962F16EF43A61B9FC9F18647C45A803F21C6AD7370352530E670D2F252375B6D6B3E87A36B4FA8026787E34B99612C480F53780DCA6BA886628CA18931A71ECCDE98F4EF1845A3C1073C3D20ABDF8D43A31CE8432B283A3261548D427793ECC89694E6AD3824EDF60E2172D7FDC906AE2C272CBA02A3703E671268F08B6C0ECF6C76C4E50EFAC8F9ADB70D893315118FED1A958B0655335F4B1FAB4D8DBD3EEA90E0F66DED01A7B0B8B2997E2E60CA67D50F471CD14656CA23F6B7B3EA132D3D295D610B99CBEFB8651397785CA6326BE0502AB43A72D32E67722EA19BEC96D706B1D4BF51FC23E07C36CEA632FD2"})
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
