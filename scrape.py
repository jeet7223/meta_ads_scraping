# Code By dev1
import sys
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import configuration

# TO customize Browser Capablities The bellow codes "options"
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("window-size=1920,1080")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('ignore-certificate-errors')
if configuration.headless_mode:
    options.add_argument('--headless')

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.implicitly_wait(5)

df = pd.read_csv("keywords.csv")
keyword = df.values
for item in keyword:
    driver.get("https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q={}&search_type=keyword_unordered&media_type=all".format(item[0]))

    p = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "_9cb_")))
    time.sleep(2)
    if not configuration.testing_mode:
        _len = driver.find_element(By.CLASS_NAME, "_9cb_").find_elements(By.CLASS_NAME, "_99s5")
        previous_height = len(_len)

        while True:
            print("Please wait scrolling down to get all results......")
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(4)

            new_height = driver.find_element(By.CLASS_NAME, "_9cb_").find_elements(By.CLASS_NAME, "_99s5")
            new_height = len(new_height)
            if new_height == previous_height:
                break

            previous_height = new_height
    else:
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(4)


    try:
        data = driver.find_element(By.CLASS_NAME, "_9cb_").find_elements(By.CLASS_NAME, "_99s5")
    except:
        data = []

    print("{} Data found".format(len(data)))

    for cards in data:
        try:
            name = cards.find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "span").text
        except:
            name = ""

        try:
            card_url = cards.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            card_url = ""

        print("Name : {}".format(name))
        print("URL : {}".format(card_url))

        # Code to open About us in new Tab
        driver.execute_script('''window.open("{}","_blank");'''.format(card_url))
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)
        # Code Here
        driver.close()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)


