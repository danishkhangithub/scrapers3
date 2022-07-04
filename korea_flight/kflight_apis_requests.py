import requests
from requests import session
import json
from pprint import pprint
from urllib import request

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    #"Accept": "*/*",
    #"Accept-Encoding": "gzip, deflate, br",
    #"Accept-Language": "en-US,en;q=0.9,bn;q=0.8,es;q=0.7,ar;q=0.6",
    #"Connection": "keep-alive",
    "Content-Length": "1843",
    "Content-Type": "application/json",
    #"Host": "apis.airportthai.co.th",
    #"Origin": "https://suvarnabhumi.airportthai.co.th",
    #"Referer": "https://suvarnabhumi.airportthai.co.th/",
    #"sec-ch-ua-mobile": "?0"

}

body = {"query":"\n      query ($site: String, $type: FlightType, $search: String, $schedule_start: String, $schedule_end: String) {\n        flights(site: $site, type: $type, search: $search, schedule_start: $schedule_start, schedule_end: $schedule_end) {\n          flight_id\n          number\n          airline_id\n          aircraft_id\n          departure_scheduled_at\n          arrival_scheduled_at\n          flight_departure {\n            id\n            site_id\n            remark\n            terminal\n            gate\n            check_in_counter\n            status_color\n            estimated_at\n            actual_at\n            scheduled_at\n            updated_at\n            flight_shares\n            __typename\n          }\n          flight_arrival {\n            id\n            site_id\n            belt\n            terminal\n            remark\n            status_color\n            estimated_at\n            first_bag_at\n            last_bag_at\n            flight_shares\n            __typename\n          }\n          origin_airport {\n            id\n            name\n            city\n            iata_code\n            icao_code\n            __typename\n          }\n          destination_airport {\n            id\n            name\n            city\n            iata_code\n            icao_code\n            __typename\n          }\n          airline {\n            id\n            iata\n            icao\n            name\n            logo\n            __typename\n          }\n          aircraft {\n            id\n            name\n            iata\n            icao\n            __typename\n          }\n          updated_at\n          __typename\n        }\n      }\n      ","variables":{"site":"bkk","type":"A","search":"","schedule_start":"2021-08-24 11:49:00","schedule_end":"2021-08-24 23:59:59"}}


url = " https://apis.airportthai.co.th/"

r = requests.post(url,  data = json.dumps(body), headers = headers)

data = r.json()['data']['flights']
for flight in data:
  features = {
    'name' : flight['aircraft']['name'],
    'number' : flight['number']


  }

  print(features)
