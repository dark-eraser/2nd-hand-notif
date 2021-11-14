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
from string import digits
from time import sleep
from selenium.common.exceptions import NoSuchElementException
API_KEY = "o.vFmaJ46t3msllT0UPbjlyjAckdKIV6fV"
SEEN_PRODS =[]

class Product_Price():
    def __init__(self, prod, price):
        self.prod = prod
        self.price = price

def truncate_price(price, site):
    number = ''.join(c for c in price if c in digits)
    if(number == ''):
        number = numpy.infty
    return number

def main():
    print("coucou")
    chrome_setup()

def list_search_items():
    pair_list = []
    gtx_1060 = Product_Price("1060", 300)
    gtx_1070 = Product_Price("1070", 450)
    gtx_1080 = Product_Price("1080", 550)
    rx_5600 = Product_Price("5600", 550)
    rx_5700 = Product_Price("5700", 650)
    rx_6700 = Product_Price("6700", 900)
    rx_6800 = Product_Price("6800", 1000)
    rx_6900 = Product_Price("6900", 1200)
    rtx_3070 = Product_Price("3070", 950)
    rtx_3060 = Product_Price("3060", 850)
    rtx_3080 = Product_Price("3080", 1500)
    rtx_3090 = Product_Price("3090", 2300)
    rtx_2070 = Product_Price("2070", 850)
    rtx_2060 = Product_Price("2060",600)
    rtx_2080 = Product_Price("3070", 950)
    #rtx_3070 = Product_Price("3070", 850)
    pair_list.append(rtx_2060)
    pair_list.append(rtx_3060)
    pair_list.append(rtx_3070)
    pair_list.append(rtx_2070)
    pair_list.append(rtx_2080)
    pair_list.append(rtx_3080)
    pair_list.append(rtx_3090)
    pair_list.append(gtx_1060)
    pair_list.append(gtx_1070)
    pair_list.append(gtx_1080)
    pair_list.append(rx_5600)
    pair_list.append(rx_5700)
    pair_list.append(rx_6700)
    pair_list.append(rx_6800)
    pair_list.append(rx_6900)

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
    #chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option ( 'excludeSwitches', [ 'enable-automation']) # parameters added in the form of key-value pairs
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    pb = PushBullet(API_KEY)
    
    try:    
        while(True):
            search_ricardo(driver, pb)
            search_anibis(driver, pb)
            #search_ebay(driver,pb)
            #print("looping")
            
    except KeyboardInterrupt:
        print("crtl-d'ed")
        driver.close()
        driver.quit()

def send_notification(element, pb):
    pb.push_link(element.text, element.get_attribute('href'))
    #print(element.get_attribute('href'))   
    print("sent_notif")

def send_notification_ebay(element, pb):
    pb.push_link(element.text, element.get_attribute('href'))
    #print(element.get_attribute('href'))   
    print("sent_notif")

def check_list_items(name):  
    #print("prout")
    tmp = name + "\n"
    with open("listfile.txt", 'r') as f:
        for line in f.readlines():
            if tmp == line:
                return True
                
                        

def search_ricardo(driver, pb):
    print("--------------------------- ricardo --------------------------")
    driver.get("https://www.ricardo.ch/en/s/grafikkarte?sort=newest")
    pair_list = list_search_items()
    #sleep(10)
    for i in range(1,60):
        try:                                      
            element = driver.find_element_by_xpath("/html/body/div[1]/div/section/div/div/div[2]/div[1]/main/div[5]/div/a["+str(i)+"]/div/div[2]/p")
            #print(element.text)
            buy_now_price = driver.find_element_by_xpath("/html/body/div[1]/div/section/div/div/div[2]/div[1]/main/div[5]/div/a["+str(i)+"]/div/div[2]/div[2]/div[2]/div/div[2]/p")
            for j in pair_list:
                if j.prod in element.text:
                    if(float(truncate_price(buy_now_price.text, "ricardo")) <= j.price):
                        if not ("Waterblock" in element.text) and not("Offer ended" in element.text) and not(check_list_items(element.get_attribute('href'))):
                            print(element.get_attribute('href'))
                            with open('listfile.txt', 'a+') as filehandle:
                                filehandle.write(element.get_attribute('href')+"\n")
                            send_notification(element, pb)
        except NoSuchElementException:
            try:
                element = driver.find_element_by_xpath("/html/body/div[1]/div/section/div/div/div[2]/div[1]/main/div[6]/div/a["+str(i)+"]")
                #print(element.text)
                buy_now_price = driver.find_element_by_xpath("/html/body/div[1]/div/section/div/div/div[2]/div[1]/main/div[6]/div/a["+str(i)+"]/div/div[2]/div[2]/div[2]/div/div[2]/p")
                for j in pair_list:
                    if j.prod in element.text:
                        #print(element.text)
                       
                        #print(buy_now_price.text)
                        if(float(truncate_price(buy_now_price.text, "ricardo")) <= j.price):
                            print(j.price)
                            if "Waterblock" not in element.text and "Offer ended" not in element.text and not(check_list_items(element.get_attribute('href'))):
                                with open('listfile.txt', 'a+') as filehandle:
                                    filehandle.write(element.get_attribute('href')+"\n")
                                send_notification(element, pb)
                                print(element.get_attribute('href'))
            except NoSuchElementException as e:
                with open("logs.txt", "w") as f:
                        f.write(str(e)+"\n")

def search_anibis(driver, pb):
    print("--------------------------- anibis --------------------------")
    driver.get("https://www.anibis.ch/de/c/computer-buerotechnik-computer-komponenten/grafikkarten?sf=dpo&so=d")
    pair_list = list_search_items()
    #sleep(10)
    for i in range(2,23):
            try:
                element = driver.find_element_by_xpath("/html/body/div[1]/div/div[5]/div/div[1]/div[2]/div/div[6]/div[1]/article["+str(i)+"]/a")
                #print(element.text)
                href_element = driver.find_element_by_xpath("/html/body/div[1]/div/div[5]/div/div[1]/div[2]/div/div[6]/div[1]/article["+str(i)+"]/a")
                buy_now_price = driver.find_element_by_xpath("/html/body/div[1]/div/div[5]/div/div[1]/div[2]/div/div[6]/div[1]/article["+str(i)+"]/a/div[2]/div[4]")
                for j in pair_list:
                    if j.prod in element.text:
                            if(float(truncate_price(buy_now_price.text, "anibis")) <= j.price):
                                 if not ("Waterblock" in element.text) and not("Offer ended" in element.text) and not(check_list_items(href_element.get_attribute('href'))):
                                    
                                    with open('listfile.txt', 'a+') as filehandle:
                                        filehandle.write(href_element.get_attribute('href')+"\n")
                                    send_notification(href_element, pb)
                                    print(href_element.get_attribute('href'))
                    
            except NoSuchElementException as e:
                with open("logs.txt", "w") as f:
                            f.write(str(e)+"\n")

def search_ebay(driver, pb):
    print("--------------------------- ebay --------------------------")
    driver.get("https://www.ebay-kleinanzeigen.de/s-grafikkarte/k0 ")
    pair_list = list_search_items()
    #sleep(10)
    for i in range(1,32):
        
            try:
                element = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div[3]/div[2]/ul/li["+str(i)+"]/article")
                #print(element.get_attribute('data-href'))
                buy_now_price = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div[3]/div[2]/ul/li["+str(i)+"]/article/div[2]/div[2]/p[2]")
                href_element = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div[3]/div[2]/ul/li["+str(i)+"]/article/div[1]/a")
                for j in pair_list:
                    if j.prod in element.text:
                            if(float(truncate_price(buy_now_price.text, "anibis"))* 1.2 <= j.price):
                                if "Waterblock" not in element.text and "Offer ended" not in element.text and not(check_list_items(element.get_attribute('data-href')) ):
                                    
                                    with open('listfile.txt', 'a+') as filehandle:
                                        filehandle.write(href_element.get_attribute('data-href')+"\n")
                                    send_notification_ebay(href_element, pb)
                                    print(element.get_attribute('data-href'))
            except NoSuchElementException as e:
                with open("logs.txt", "w") as f:
                            f.write(str(e)+"\n")

                     
main()











