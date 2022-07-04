# packages
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
import json
import string

class Urban(scrapy.Spider):
    name = 'urban'
    
    url = 'https://www.urbandictionary.com/popular.php?character='
    
    
    
    def start_requests(self):
       # clear output
       with open('urban.json','w') as f:
            f.write('')
    
       for letter in string.ascii_uppercase:
           nex_page = self.url + letter
           yield scrapy.Request(url = nex_page, callback = self.parse)
        
           break
        
    def parse(self, response):
       # extract data
       links = []
       
       for item in response.css('ul.no-bullet').css('li'):
           word = item.css('a::text').get()
           
           try:
             short_description = requests.get('https://api.urbandictionary.com/v0/tooltip?term='+ word + '&key=ab71d33b15d36506acf1e379b0ed07ee').json()['string'].replace('\r\n','').replace('<b>','').replace('</b>','')
              
           except:
              print('error')
              pass    
           
           
           
           short_description = short_description  
                       
           links.append({
               'word' : word,
               'short_description' : short_description,
               'link' : item.css('a::attr(href)').get()
           }) 
           
           # uncomment to craw only the first word within a page
           # break
           
           #print(json.dumps(items, indent = 2))
           
           
       for link in links:   
           yield response.follow(url = link['link'], meta = {'short_description': link['short_description'], 'word' : link['word']},callback = self.parse_cards)
           
    def parse_cards(self, response):
        print('\n\n RECURSIVE RESPONSE:' , response.status) 
        short_description = response.meta.get('short_description')
        word = response.meta.get('word')
        
        # extract full desciption
        full_description = ' '.join(response.css('div.def-panel').css('div.meaning::text').getall()) 
        
        items = {
           'word' : word,
           'short_description': short_description,
           'full_description' : full_description
        }
        
        #print(json.dumps(items, indent = 2))
        
        # write results
        with open('urban.json','a') as f:
            f.write(json.dumps(items, indent = 2) + '\n')    
             

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Urban)
    process.start()        
    
    
            
