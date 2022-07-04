# packages
import requests
import json
import time

class Geocoder:
    
    results = []

    # base url
    base_url = 'https://nominatim.openstreetmap.org/search'
   
    def fetch(self,address):
       # string query parameters
       params = {
          'q' :address,
          'format' : 'geocodejson',
       }
      
       res = requests.get(url = self.base_url,params = params)
       print('HTTP GET request to URL : %s | Status code %s' % (res.url,res.status_code))
      
       if res.status_code == 200:
          return res
          
       else: 
         return None   
      
    def parse(self, res):
        try:
    
           label = json.dumps(res['features'][0]['properties']['geocoding']['label'],indent = 2)
           coordinates = json.dumps(res['features'][0]['geometry']['coordinates'], indent = 2).replace('\n', '').replace('[', '').replace(']','').strip() 
           
           self.results.append({
             'address' : label,
             'coordinates' : coordinates
           
           })
           
           print(self.results)
        except:
           pass
    
    def store_results(self):
       with open('resuls.json', 'w') as json_file:
            json_file.write(json.dumps(self.results, indent = 2))
    
    
    def run(self):
       # addresses list
       addresses = ''
       
       with open('addresses.txt','r') as f:
          for line in f.read():
              addresses += line    
       
       # convert addresses to list
       addresses =  addresses.split('\n')
       
       # loop over addresses
       for address in addresses:
          res = self.fetch(address).json()
          self.parse(res) 
          
          # respect nomination crawling policies
          time.sleep(2)
          
          # store results
          self.store_results()
           


# main driver
if __name__ == '__main__':
    geocode = Geocoder()
    geocode.run()      
