#Code By dev1
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(5)

driver.get("https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q=Stock%20Market&search_type=keyword_unordered&media_type=all")
driver.maximize_window()

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



#Code by Jeet