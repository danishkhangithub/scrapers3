import requests
from bs4 import BeautifulSoup
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import os

class ImageScraper:
    url = 'https://www.airbnb.co.uk/s/Ljubljana--Slovenia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=Ljubljana%2C%20Slovenia&place_id=ChIJ0YaYlvUxZUcRIOw_ghz4AAQ&checkin=2020-11-01&checkout=2020-11-08&source=structured_search_input_header&search_type=autocomplete_click'

    def __init__(self):

        chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'

        chrome_options = Options()
        #chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(
          executable_path=chrome_driver_path, options=chrome_options
        )

    def imagedown(self, folder):
        try:
            os.mkdir(os.path.join(os.getcwd(), folder))
        except:
            pass
        os.chdir(os.path.join(os.getcwd(), folder))
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup.select('._15tommw'))
        try:
          images = soup.find_all('picture img', attrs = {'class' : '_6tbg2q'})
          print(images)
        except Exception as e:
           print(e)

#        for image in images:
#            print(image)
#

# run main driver
if __name__ == '__main__':
    scraper = ImageScraper()
    scraper.imagedown('airnb_images')
