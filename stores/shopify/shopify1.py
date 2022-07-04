# import libraries
import requests

# url 
url = 'https://979a98c1703bafd3ef5cc65a2afd225c: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@danish000.myshopify.com/admin/api/2021-04/'

# function for products
def get_products():
    endpoint = 'products.json'
    r = requests.get(url + endpoint)
    return r.json()
    
# function for updating products    
def change_status(product_id,status):
        endpoint = 'products/'
        payload = {
           "product": {
               "status" : status
                       }
                  }
        send_url = url + endpoint + str(product_id) + '.json'   
        r = requests.put(send_url, json= payload)
        print(r.json())
        return
        
    
products = get_products()

change_status(products['products'][0]['id'], 'active')     


