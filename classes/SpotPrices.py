import requests
import moment
import sys

class SpotPrices:
    __spot_price_area = None
    __spot_price_area_object = None
    __current_hour_spot_price = 0.00

    def __init__(self, spotPriceArea):
         self.__spot_price_area = spotPriceArea

    #
    # Look up the current spot price from the provided area
    #
    def find_spot_price_area(self):
        request = requests.get('https://prod-publicservices.azurewebsites.net/api/spotprices/ts/auto')
        if(request.status_code != 200):
            sys.exit('Was not able to get spot prices from external API')
        response = request.json()
        spotPriceArea = list(filter(lambda x:x["Area"]==self.get_spot_price_area(),response))
        if not spotPriceArea:
            sys.exit('Given response did not contain the spot price area')
        self.set_spot_price_area_object(spotPriceArea[0])

    #
    # Look for any hour that match the current local time and return the object.
    #
    def find_spot_price_by_hour(self):
        current_spot_price = list(filter(lambda x:x["Date"]==self.get_current_local_time(),self.get_spot_price_area_object()['SpotPrice']))
        if not current_spot_price:
            sys.exit('There was no spot price for the given time')
        self.set_current_hour_spot_price(current_spot_price[0]['Value'])

    #
    # Clean up the date to display current date and the active hour for spot price 
    # Also round up the spot price to two decimals
    #
    def modify_spot_price_area_object_date(self):
        for item in self.get_spot_price_area_object()['SpotPrice']:
            item['Date'] = moment.date(item['Date']).format("YYYY-M-D H")
            item['Value'] = round(item['Value'], 2)

    def get_spot_price_area(self):
        return self.__spot_price_area

    def set_spot_price_area(self, spotPriceArea):
        self.__spot_price_area = spotPriceArea

    def get_spot_price_area_object(self):
        return self.__spot_price_area_object

    def set_spot_price_area_object(self, spotPriceAreaObject):
        self.__spot_price_area_object = spotPriceAreaObject

    def get_current_hour_spot_price(self):
        return self.__current_hour_spot_price
    
    def set_current_hour_spot_price(self, currentHourSpotPrice):
        self.__current_hour_spot_price = currentHourSpotPrice
    
    def get_current_local_time(self):
        return moment.now().locale("Europe/Oslo").format("YYYY-M-D H")