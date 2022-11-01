from classes import SpotPrices
from classes import EaseeCharger
from dotenv import load_dotenv
import os;

load_dotenv()

EASEE_BEARER_TOKEN = os.getenv('EASEE_BEARER_TOKEN')
EASEE_SITE_ID = os.getenv('EASEE_SITE_ID')
EASEE_CURRENCY_ID = os.getenv('EASEE_CURRENCY_ID')

SPOT_PRICE_AREA = os.getenv('SPOT_PRICE_AREA')


spotPrices = SpotPrices.SpotPrices(SPOT_PRICE_AREA)
spotPrices.find_spot_price_area()
spotPrices.modify_spot_price_area_object_date()
spotPrices.get_spot_price_area_object()
spotPrices.find_spot_price_by_hour()


easeeCharger = EaseeCharger.EaseeCharger(EASEE_SITE_ID)
easeeCharger.create_access_token_if_expired()
easeeCharger.set_price_currency_id(EASEE_CURRENCY_ID)
easeeCharger.set_current_price(spotPrices.get_current_hour_spot_price())
easeeCharger.set_easee_charging_price()


