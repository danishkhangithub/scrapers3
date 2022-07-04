import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json
import os
import time

#url = 'https://www.airbnb.co.uk/s/Ljubljana--Slovenia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=Ljubljana%2C%20Slovenia&place_id=ChIJ0YaYlvUxZUcRIOw_ghz4AAQ&checkin=2020-11-01&checkout=2020-11-08&source=structured_search_input_header&search_type=autocomplete_click'
class ImageScraper:
    results = []
    url = 'https://www.daraz.pk/products/tecno-pop-5-61-inches-display-2-gb-ram-32-gb-rom-dual-sim-fingerprint-li-po-5000-mah-1-year-warranty-i232268198-s1451732679.html?spm=a2a0e.searchlistcategory.list.4.39fdc414JLxydV&search=1'
    def Parsed_html(self):

        with sync_playwright() as p:
          browser = p.chromium.launch(headless = False)
          page = browser.new_page()
          page.goto(self.url)
          #page.set_default_timeout(10000)
          page.wait_for_load_state('networkidle')
          page_source = page.content()
          time.sleep(2)

          browser.close()
        return page_source

    def imagedown(self, page_source):
        response = Selector(text = page_source)
        features = {
            'Product Url' : response.url,
            'Name' : response.css('div[class= "pdp-product-title"] span::text').get(),
            'Price' : response.css('div[class= "pdp-product-price"] span::text').get(),
            'Rating' : response.css('div[class= "score"] span::text').get(),
            'Reviews' : response.css('div[class= "pdp-review-summary"] a::text').get().strip(' Ratings')

        }

        self.results.append(features)
        print(self.results)



    def run(self):
        parsed_html = self.Parsed_html()
        self.imagedown(parsed_html)

        self.csv()

    def csv(self):
        headers = self.results[0].keys()
        with open('phones.csv','w') as csv_file:
             writer = csv.DictWriter(csv_file,fieldnames = headers)
             writer.writeheader()
             writer.writerows(features)




# Run main driver
if __name__ == '__main__':
   scraper = ImageScraper()
   scraper.run()
