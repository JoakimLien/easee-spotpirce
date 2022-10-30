import requests


class EaseeCharger:

    __site_id = None
    __current_price = 0.00
    __price_currency_id = None
    __bearer_token = None

    def __init__(self, siteId):
         self.__site_id = siteId

    def set_easee_charging_price(self):
        headers = { 
            "Authorization" : "Bearer "+self.get_bearer_token()+"", 
            "accept": "application/json" 
        }

        data = {
            "currencyId": self.get_price_currency_id(),
            "costPerKWh": self.get_current_price(),
        }

        request = requests.post("https://api.easee.cloud/api/sites/"+self.get_site_id()+"/price", headers=headers, json=data)
        if(request.status_code != 200):
            sys.exit('Something went wrong when setting the current price to easee charger')

    def get_site_id(self):
        return self.__site_id
    
    def set_site_id(self, siteId):
        self.__site_id = siteId

    def get_current_price(self):
        return self.__current_price
    
    def set_current_price(self, currentPrice):
        self.__current_price = currentPrice

    def get_price_currency_id(self):
        return self.__price_currency_id
    
    def set_price_currency_id(self, priceCurrencyId):
        self.__price_currency_id = priceCurrencyId
    
    def get_bearer_token(self):
        return self.__bearer_token

    def set_bearer_token(self, bearerToken):
        self.__bearer_token = bearerToken

    