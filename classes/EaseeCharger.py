import requests
import pickle
import moment
import sys
import os

class EaseeCharger:

    __site_id = None
    __current_price = 0.00
    __price_currency_id = None
    __bearer_token = None
    __refresh_token = None

    def __init__(self, siteId):
         self.__site_id = siteId

    def set_easee_charging_price(self):
        config = self.get_config_details();

        headers = { 
            "Authorization" : "Bearer "+config['bearer_token']+"", 
            "accept": "application/json" 
        }

        data = {
            "currencyId": self.get_price_currency_id(),
            "costPerKWh": self.get_current_price(),
        }

        request = requests.post("https://api.easee.cloud/api/sites/"+self.get_site_id()+"/price", headers=headers, json=data)

        if(request.status_code != 200):
            sys.exit('Something went wrong when setting the current price to easee charger')

        print("Charger with site id " + self.get_site_id() + " with current price of: " + str(self.get_current_price()))

    def create_access_token_if_expired(self):
        config = self.get_config_details();

        current_time = moment.now().locale("Europe/Oslo").add(hours=1).format("YYYY-M-D H")
        expires_time = config['expires'];
        if(expires_time <= current_time):
            self.request_new_bearer_token()


    def request_new_bearer_token(self):
        config = self.get_config_details()
        headers = { 
            "Authorization" : "Bearer "+config['bearer_token']+"", 
            "accept": "application/json" 
        }

        data = {
            "accessToken": config['bearer_token'],
            "refreshToken": config['refresh_token'],
        }

        request = requests.post("https://api.easee.cloud/api/accounts/refresh_token", headers=headers, json=data)
        if(request.status_code != 200):
            sys.exit('Could not generate new access token')

        response = request.json()

        self.set_config_details(response['accessToken'], response['refreshToken'], response['expiresIn'])


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
    
    def get_config_details(self):
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rel_path = "config.py"
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, 'rb') as pickle_file:
            data = pickle.load(pickle_file)

        return data;

    def set_config_details(self, bearerToken, refreshToken, expiresIn):
        expires = moment.now().locale("Europe/Oslo").add(seconds=expiresIn).format("YYYY-M-D H")
        data = {
            "bearer_token": bearerToken,
            "refresh_token": refreshToken,
            "expires": expires,
        }
        file = open('config.py', 'wb')
        pickle.dump(data, file)
        file.close()

    