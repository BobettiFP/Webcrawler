from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
from urllib import parse
import pandas as pd
import time
import openpyxl
import requests

webpage = input("Address:")
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('C:\\Users\\user200518\\Desktop\\chromedriver.exe')
driver.implicitly_wait(10)
driver.get(webpage)

def bts_crawler(i):
    driver = webdriver.Chrome('C:\\Users\\user200518\\Desktop\\chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get(webpage)
    time.sleep(random.randint(10,30))
    
    driver.find_element_by_xpath('//*[@id="frm"]/div/table/tbody/tr['+str(i)+']/td[3]/div/div/a').send_keys(Keys.ENTER)

#공통
    try:
        driver.find_element_by_xpath('//*[@id="lyricArea"]/button').click()
        driver.implicitly_wait(10)
        time.sleep(random.randint(10,30))
        lyric = driver.find_element_by_xpath('//*[@id="d_video_summary"]').text

        title_loc = lyric.find('\n')
        time.sleep(random.randint(10,30))
        title = driver.find_element_by_xpath('//*[@id="downloadfrm"]/div/div/div[2]/div[1]/div[1]').text
        artist = driver.find_element_by_xpath('//*[@id="downloadfrm"]/div/div/div[2]/div[1]/div[2]/a/span[1]').text
        composer = driver.find_element_by_xpath('//*[@id="conts"]/div[3]').text
        try:
            f = open(title+ ".txt", 'w')
            f.write(artist+'\n\n')
            
            f.write(lyric)
            f.close()
            g = open("작사_"+title+".txt",'w')
            g.write(composer.replace("작곡","").replace("작사","").replace("편곡",""))
            g.close()
        except UnicodeEncodeError:
            pass
    except NoSuchElementException:
        pass
    
        
    driver.quit()
for i in list(range(1,50)):
    try:
        bts_crawler(i)
        time.sleep(random.randint(10,30))
    except:
        pass
