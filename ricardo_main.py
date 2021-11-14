#!/usr/bin/python
from logging import lastResort, log
from selenium import webdriver
import selenium
#from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.common.action_chains import ActionChains
import numpy
from pushbullet import PushBullet

from time import sleep
from selenium.common.exceptions import NoSuchElementException
API_KEY = "o.vFmaJ46t3msllT0UPbjlyjAckdKIV6fV"
BUY_NOW_PRICE = 850
FOUND = False
KEYWORD = "3070"
SEEN_PRODS =[]

class Product_Price():
    def __init__(self, prod, price):
        self.prod = prod
        self.price = price

def truncate_price(price):
    number = price.replace("'", "")
    return number
def main():
    print("coucou")
    chrome_setup()

def list_search_items():
    pair_list = []
    rtx_3070 = Product_Price("3070", 850)
    rtx_3060 = Product_Price("3060", 650)
    rtx_3080 = Product_Price("3080", 1200)
    rtx_3090 = Product_Price("3090", 2000)
    rtx_2070 = Product_Price("2070", 750)
    rtx_2060 = Product_Price("2060", 550)
    rtx_2080 = Product_Price("3070", 850)
    #rtx_3070 = Product_Price("3070", 850)
    pair_list.append(rtx_2060)
    pair_list.append(rtx_3060)
    pair_list.append(rtx_3070)
    pair_list.append(rtx_2070)
    pair_list.append(rtx_2080)
    pair_list.append(rtx_3080)
    pair_list.append(rtx_3090)

    return pair_list

def chrome_setup():
    user_agent = 'Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    chrome_options = webdriver.ChromeOptions(); 
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    #chrome_options.debugger_address="127.0.0.1:9222"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option ( 'excludeSwitches', [ 'enable-automation']) # parameters added in the form of key-value pairs
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome( executable_path="/usr/local/bin/chromedriver",options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    looping(driver)
    
def looping(driver):
    try:    
        while(True):
            driver.get("https://www.ricardo.ch/en/s/grafikkarte?sort=newest")
            search(driver)
            print("looping")
            sleep(1)
    except KeyboardInterrupt:
        print("crtl-d'ed")
        driver.close()
        driver.quit()

def send_notification(element, pb):
    pb.push_link(element.text, element.get_attribute('href'))   
    print("sent_notif")


def search(driver):
    pb = PushBullet(API_KEY)
    pair_list = list_search_items()
    #sleep(10)
    #driver.get_screenshot_as_file("screenshot.png")
    for i in range(1,60):
        for j in pair_list:
            
            try:                                      
                element = driver.find_element_by_xpath("/html/body/div[1]/div/section/div/div/div[2]/div[1]/main/div[5]/div/a["+str(i)+"]/div/div[2]/p")
                if j.prod in element.text:
                    print(element.text)
                    try:
                        buy_now_price = driver.find_element_by_xpath("/html/body/div[1]/div/section/div/div/div[2]/div[1]/main/div[5]/div/a["+str(i)+"]/div/div[2]/div[2]/div[2]/div/div[2]/p")
                        print(buy_now_price.text)
                        if(float(truncate_price(buy_now_price.text)) < j.price):
                            send_notification(element, pb)
                            FOUND = True
                    except NoSuchElementException:
                        print("nope")
            except NoSuchElementException:
                print("second try")
                element = driver.find_element_by_xpath("/html/body/div[1]/div/section/div/div/div[2]/div[1]/main/div[6]/div/a["+str(i)+"]")
    
                if j.prod in element.text:
                    print(element.text)
                    try:
                        buy_now_price = driver.find_element_by_xpath("/html/body/div[1]/div/section/div/div/div[2]/div[1]/main/div[6]/div/a["+str(i)+"]/div/div[2]/div[2]/div[2]/div/div[2]/p")
                        #print(buy_now_price.text)
                        if(float(truncate_price(buy_now_price.text)) < j.price):
                            if "Waterblock" not in element.text and "Offer ended" not in element.text and element not in SEEN_PRODS:
                                send_notification(element, pb)
                                SEEN_PRODS.append(element)
                                FOUND = True
                    except NoSuchElementException:
                        print("nope")
                
                                            

main()          
# try:
#     main()
# except Exception as e:
#     print(e)
#     with open("logs.txt", "w") as f:
#         f.write(str(e))













