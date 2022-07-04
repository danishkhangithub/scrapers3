import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome(executable_path=r'/home/danish-khan/scrapers/researchgate/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')

title_list = []
date_list  = []
genre_list = []

for page_num in range(1, 4):
    url = r"https://www.albumoftheyear.org/list/1500-rolling-stones-500-greatest-albums-of-all-time-2020/{}".format(page_num)
    driver.get(url)

    try:
        time.sleep(5)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "centerContent"))
        )
        albumlistrow = element.find_elements_by_class_name('albumListRow')
        for a in albumlistrow:
            title = a.find_element_by_class_name('albumListTitle')
            date = a.find_element_by_class_name('albumListDate')
            try:
                genre = a.find_element_by_class_name('albumListGenre')
            except NoSuchElementException:
                pass
            title_list.append(title.text)
            date_list.append(date.text)
            genre_list.append(genre.text)

    finally:
        driver.close()

df = pd.DataFrame(list(zip(title_list,date_list,genre_list)), columns=['title', 'data','genre'])
df.head()














#import scrapy
#from scrapy.selector import Selector
#from scrapy.crawler import CrawlerProcess
#from scrapy.http import FormRequest
#import csv
#import json
#
# init class
#class Mysql(scrapy.Spider):
#    # scraper name
#    name = "mysql_scraper"
#    start_urls = ['https://suvarnabhumi.airportthai.co.th/flight']
#    api_url = 'https://apis.airportthai.co.th/'
#
#    formdata =
#      {"query":"\n      query ($site: String, $type: FlightType, $search: String, $schedule_start: String, $schedule_end: String) {\n        flights(site: $site, type: $type, search: $search, schedule_start: $schedule_start, schedule_end: $schedule_end) {\n          flight_id\n          number\n          airline_id\n          aircraft_id\n          departure_scheduled_at\n          arrival_scheduled_at\n          flight_departure {\n            id\n            site_id\n            remark\n            terminal\n            gate\n            check_in_counter\n            status_color\n            estimated_at\n            actual_at\n            scheduled_at\n            updated_at\n            flight_shares\n            __typename\n          }\n          flight_arrival {\n            id\n            site_id\n            belt\n            terminal\n            remark\n            status_color\n            estimated_at\n            first_bag_at\n            last_bag_at\n            flight_shares\n            __typename\n          }\n          origin_airport {\n            id\n            name\n            city\n            iata_code\n            icao_code\n            __typename\n          }\n          destination_airport {\n            id\n            name\n            city\n            iata_code\n            icao_code\n            __typename\n          }\n          airline {\n            id\n            iata\n            icao\n            name\n            logo\n            __typename\n          }\n          aircraft {\n            id\n            name\n            iata\n            icao\n            __typename\n          }\n          updated_at\n          __typename\n        }\n      }\n      ","variables":{"site":"bkk","type":"A","search":"","schedule_start":"2021-08-29 11:51:00","schedule_end":"2021-08-29 23:59:59"}}
#
#
#    headers = {
#       'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
#       #'x-requested-with' : 'XMLHttpRequest'
#       "Content-Type": "application/json"
#       }
#
#    custom_settings = {'HTTPERROR_ALLOW_ALL': True}
#
#    # general crawler
#    def parse(self,response):
#
#            # initial HTTP request
#            yield scrapy.FormRequest(
#                url=self.api_url,
#                method = "POST",
#                formdata = json.dumps(self.formdata),
#                headers=self.headers,
#                callback=self.parse2
#                      )
#    def parse2(self, res):
#
#       data = json.loads(res.text)
#       print(json.dumps(data, indent = 2))
#
#
#       '''
#       content = ''
#
#       with open('mysql_live_customers.html', 'r') as html:
#            for line in html.read():
#                content += line
#
#       response = Selector(text = content)
#       print(response)
#
#       '''
#       '''
#       yield response.follow(
#             url = ,
#             headers = self.headers,
#             callback =
#       )
#
#       with open('qsranks.csv', 'a') as csv_file:
#             writer = csv.DictWriter(csv_file, fieldnames=items.keys())
#             writer.writerow(items)
#       '''
#
#
#
#
#
#if __name__ == '__main__':
#   process = CrawlerProcess()
#   process.crawl(Mysql)
#   process.start()
#   #Mysql.parse(Mysql, '')