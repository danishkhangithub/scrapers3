#
#
#from pywebcopy import WebPage
#
#kwargs = {'project_name' : 'site folder'}
#
#wp = WebPage()
#wp.get('http://google.com')
#
#wp.save_html()
#'webpages'
#
#

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import pyautogui

#URL = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
#FILE_NAME = ''
#
# open page with selenium
# (first need to download Chrome webdriver, or a firefox webdriver, etc)
#chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'
#total = []
#chrome_options = Options()
#chrome_options.add_argument('--headless')
#
#driver = webdriver.Chrome(
#  executable_path=chrome_driver_path, options=chrome_options
#)
#
#driver.get(URL)
#
#
# wait until body is loaded
#WebDriverWait(driver, 60).until(visibility_of_element_located((By.TAG_NAME, 'body')))
#time.sleep(1)
# open 'Save as...' to save html and assets
#pyautogui.hotkey('ctrl', 's')
#time.sleep(1)
#if FILE_NAME != '':
#    pyautogui.typewrite(FILE_NAME)
#pyautogui.hotkey('enter')
#
#driver.quit()
#








# import libraries
#import scrapy
#from scrapy.crawler import CrawlerProcess
#from scrapy.selector import Selector
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.expected_conditions import presence_of_element_located
#from selenium.webdriver.support import expected_conditions as EC
#import pickle
#import time
#import csv
#import os
#
# create the main class
#class Hotels(scrapy.Spider):
#
#    name = "hotels"
#
#    headers = {
#        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
#    }
#
#    # remove csv file if already present
#    file = 'hotels.csv'
#
#    try:
#      if (os.path.exists(file)) and (os.path.isfile(file)):
#         os.remove(file)
#         print('file removed', file)
#      else:
#         print('file not found')
#    except OSError:
#       pass
#
#    results = []
#
#    custom_settings = {
#       'CONCURRENT_REQUEST_PER_DOMAIN': 6,
#       'CONCURRENT_REQUESTS_PER_IP' : 6,
#       'DOWNLOAD_DELAY': 1,
#       'DOWNLOAD_TIMEOUT' : 10,
#       'AUTO_THROTTLE' : False,
#       'COOKIES_ENABLED' : True,
#               # enable the middleware
#       'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
#
#        # enable crawlera
#        'CRAWLERA_ENABLED': False,
#
#        # the APIkey you get with your subscription
#        'CRAWLERA_APIKEY': '89d13c9b2dd6414aafd11e7952b0769b',
#
#        'CRAWLERA_URL'      : 'http://123compareme.crawlera.com:8010'
#
#    }
#
#    urls = []
#
#    def __init__(self):
#
#        chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'
#
#        chrome_options = Options()
#        #chrome_options.add_argument('--headless')
#
#        self.driver = webdriver.Chrome(
#          executable_path=chrome_driver_path, options=chrome_options
#        )
#
#
#
#    def start_requests(self):
#
#        with open('urls.txt', 'r') as text_file:
#            for line in text_file.read().split('\n'):
#                self.urls.append(line)
#
#        for url in self.urls:
#
#            yield scrapy.Request(
#               url = url,
#               headers = self.headers,
#               callback = self.parse
#            )
#            break
#    def parse(self, response):
#      content = ''
#
#      with open('hotel1.html', 'r') as html_file:
#          for line in html_file.read():
#              content +=line
#
#      response = Selector(text = content)
#
#      self.driver.get(response.url)
#
#      #pickle.dump( self.driver.get_cookies() , open("cookies.pkl","wb"))
#
#
#      time.sleep(2)
#
#      res = Selector(text = self.driver.page_source)
#
#      features = {
#         'Name' : res.css('div[class = "Box-sc-8h3cds-0 Flex-sc-1ydst80-0 gPRMGz"] h1::text').get(),
#         'Price' : res.css('span[class = "Text__Span-sc-1c7ae3w-1 jnGmZc"]::text').get(),
#         'Address' : res.css('div[class = "Text-sc-1c7ae3w-0 MapModalLink__HotelAddress-sc-1n5j1yb-3 kQzGjq"]::text').get()
#      }
#
#      print(features)
#
#      # append data to list
#      self.results.append(features)
#
#      header = self.results[0].keys()
#
#      # store all the scraped data into csv file
#      with open('hotels.csv', 'w+', newline = '') as csv_file:
#           writer = csv.DictWriter(csv_file, fieldnames = header)
#           writer.writerows(self.results)
#
#
# initialized the main driver
#if __name__  == '__main__':
#   scraper = CrawlerProcess()
#   scraper.crawl(Hotels)
#   scraper.start()
#   #Hotels.parse(Hotels,'')
#