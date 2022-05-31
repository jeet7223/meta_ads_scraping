# Code By dev1
import time
from selenium import webdriver
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

driver.get(
    "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q=Stock%20Market&search_type=keyword_unordered&media_type=all")

p = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "_9cb_")))
time.sleep(2)

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
    print("===================================")
    time.sleep(1)

# Code by Jeet
