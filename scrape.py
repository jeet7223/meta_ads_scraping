# Code By dev1
import csv
import re
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

option_ans = input("Do you want to start fresh output Y/N  -: ")

if option_ans == "Y" or option_ans == "y":
    filename = "output.csv"
    # writing to csv file
    with open(filename, 'w', newline='', encoding="utf8") as csvfile:
        # creating a csv writer object,
        csvwriter = csv.writer(csvfile)
        # writing the data rows
        csvwriter.writerows([["Page Name","Page Address","Email","Contact","Website Address"]])


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
counter = 1
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

        # Code to open About us in new Tab
        driver.execute_script('''window.open("{}","_blank");'''.format(card_url))
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)

        phone_number_string = ""
        site_url = ""
        try:
            link_data = driver.find_element_by_xpath(
                "//div[@class='rq0escxv l9j0dhe7 du4w35lb hpfvmrgz buofh1pr g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5 o387gat7 qmfd67dx rek2kq2y']").find_elements_by_xpath(
                "//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 "
                "p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr "
                "f1sip0of lzcic4wl gpro0wi8 py34i1dx']")
            email = None
            for _item in link_data:
                website_data_string = _item.text
                if "http" in website_data_string or "https" in website_data_string:
                    site_url = website_data_string
                    break
                else:
                    site_url = None
        except:
            site_url = None

        try:
            link_data = driver.find_element_by_xpath(
                "//div[@class='rq0escxv l9j0dhe7 du4w35lb hpfvmrgz buofh1pr g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5 o387gat7 qmfd67dx rek2kq2y']").find_elements_by_xpath(
                "//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 "
                "p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr "
                "f1sip0of lzcic4wl gpro0wi8 py34i1dx']")
            email = None
            for _item in link_data:
                email_html = _item.get_attribute('href')
                if "mailto:" in email_html:
                    email = email_html.replace("mailto:", "")
                    break
                else:
                    pass
        except:
            email = None

        try:
            link_data = driver.find_element_by_xpath(
                "//div[@class='rq0escxv l9j0dhe7 du4w35lb hpfvmrgz buofh1pr g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5 o387gat7 qmfd67dx rek2kq2y']").find_elements_by_xpath(
                "//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v b1v8xokw oo9gr5id hzawbc8m']")

            for _item in link_data:
                text_content = _item.text.replace(" ","")
                if "+" in text_content:
                    phone_number_string = phone_number_string + str(text_content)
        except:
            pass

        phone_regex = re.compile(
            r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))")
        try:
            contact_number = phone_regex.findall(phone_number_string)[0]
        except:
            contact_number = None

        print("Counter -: {}".format(counter))
        if email is None and contact_number is None and site_url is None:
            pass
        else:
            filename = "output.csv"
            # writing to csv file
            with open(filename, 'a', newline='', encoding="utf8") as csvfile:
                # creating a csv writer object,
                csvwriter = csv.writer(csvfile)
                # writing the data rows
                csvwriter.writerow([name, card_url, email, contact_number, site_url])
        counter = counter + 1
        driver.close()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)


