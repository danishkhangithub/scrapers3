import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from scrapy.selector import Selector
import json
import os
import time

#url = 'https://www.airbnb.co.uk/s/Ljubljana--Slovenia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=Ljubljana%2C%20Slovenia&place_id=ChIJ0YaYlvUxZUcRIOw_ghz4AAQ&checkin=2020-11-01&checkout=2020-11-08&source=structured_search_input_header&search_type=autocomplete_click'
class ImageScraper:
    url = 'https://www.airbnb.co.uk/s/Ljubljana--Slovenia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=Ljubljana%2C%20Slovenia&place_id=ChIJ0YaYlvUxZUcRIOw_ghz4AAQ&checkin=2020-11-01&checkout=2020-11-08&source=structured_search_input_header&search_type=autocomplete_click'
    folder = 'bratislava'
    def imagedown(self):


        folder = 'bratislava'
        try:
            os.mkdir(os.path.join(os.getcwd(), folder))
        except:
            pass
        os.chdir(os.path.join(os.getcwd(), folder))
        with sync_playwright() as p:
          browser = p.chromium.launch(headless = False)
          page = browser.new_page()
          page.goto(self.url,timeout = 0)

          #page.wait_for_load_state('networkidle')
          page_source = page.content()

          browser.close()
        return page_source

    def imagedown2(self):
        page_source  = self.imagedown()
#        content = ''
#        with open('res.html','r') as html_file:
#            for line in html_file.read():
#                content += line
        response = Selector(text = page_source)

        try:
          images = response.css('picture')
          for i in images:
              links = i.css('source::attr(srcset)').get()
              #for link in links:
#              filename  = self.folder + '/' + links.strip('pictures/')[1]
#              with open(filename, 'wb') as f:
#                    im = requests.get(links)
#                    f.write(im.content)
#                    print('Writing: ',links)


        except Exception as e:
           print(e)
#                with open(name.replace(' ', '-').replace('/', '') + '.jpg', 'wb') as f:
#                    im = requests.get(link)
#                    f.write(im.content)
#                    print('Writing: ', name)
#
# Run main driver
if __name__ == '__main__':
   scraper = ImageScraper()
   scraper.imagedown2()