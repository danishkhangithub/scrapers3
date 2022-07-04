 import libraries
import requests
import json
import time

 reverse ReverseGeocoder
class ReverseGeocoder:

    results = []

    # base url
    base_url = 'https://nominatim.openstreetmap.org/reverse?'

    def fetch(self, lat, lon):

       # headers
       headers = {
          'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
       }

       # parameters
       params = {
          'format' : 'geojson',
          'lat' : lat,
          'lon' : lon
       }

       # HTTP GET Request
       res = requests.get(url = self.base_url, params = params,headers = headers)
       print('HTTP GET Request to URL : %s |  STATUS CODE %s ' %(res.url, res.status_code))

       if res.status_code == 200:
          return res
       else:
          return None

    def parse(self, res):
      self.results.append(res['features'][0]['properties'])


    def store_results(self):
      with open('results2.json', 'w') as f:
         f.write(json.dumps(self.results, indent = 2))

    def run(self):
       # load coordinates
       content = ''

       with open('coordinates.txt', 'r') as f:
           for line in f.read():
               content +=line

       coordinates = content.split('\n')

       for coordinate in coordinates:
         try:
            # extract lat and lon
            lon = coordinate.split(',')[0].strip()
            lat = coordinate.split(',')[1].strip()

            # make HTTP Request
            res = self.fetch(lat,lon)

            self.parse(res.json())

            # respect crawling policies
            time.sleep(2)

         except:
            pass

       # store results
       self.store_results()
 main driver
if __name__ == '__main__':
    geocoder = ReverseGeocoder()
    geocoder.run()
