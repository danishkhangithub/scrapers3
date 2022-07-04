# import modules
import urllib.request
import json

with urllib.request.urlopen("https://geolocation-db.com/jsonp/172.19.1.46") as url:
  data = (url.read())
  print(data)