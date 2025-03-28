import requests, re
from config import VoidexConfiguration
from loguru import logger
import sys
logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)


class ColorfulLogger:
    def __init__(self):
        self.session_name = None
        
    def info(self, message):
        logger.info(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def debug(self, message):
        logger.info(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def warning(self, message):
        
        logger.error(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def error(self, message):
        logger.error(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def critical(self, message):
        logger.error(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def success(self, message):
        # from bot.utils import success
        logger.success(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

console =  ColorfulLogger()

class VDXUtils:
    @staticmethod
    def parse_proxies():
     while True:
        proxy = input("Enter proxy: ")
        if proxy != "":
            proxies = re.findall(r'(\S+:\d+:\S+:\S+)', proxy)
            if not proxies:
                console.error("Invalid proxy format")
                continue
            else:
                return proxies
        else:
            return []
    
    @staticmethod
    def get_filename():
     while True:
        card = input("Enter filename: ")
        if not card.endswith(".txt"):
            console.error("Please enter a filename with .txt extension")
            continue
        else:
            return card
        
    @staticmethod
    def create_lista_(text: str):
      m = re.findall(r'\d{15,16}(?:/|:|\|)\d+(?:/|:|\|)\d{2,4}(?:/|:|\|)\d{3,4}', text)
      lis = list(filter(lambda num: num.startswith(("5", "6", "3", "4")), [*set(m)]))
      return [xx.replace("/", "|").replace(":", "|") for xx in lis]

class VoidexClient(VDXUtils):
    def __init__(self, api_key: str, proxy:str = None, bot_token: str = None, chat_id: int = None):
        self.api_key = api_key
        self.base_url = "https://beta.voidapi.xyz/v2/{}"
        self.proxy = proxy or ""
        self.chat_id = chat_id
        self.bot_token = bot_token or ""
        self.config = VoidexConfiguration
    
    def ping(self):
     try:
        url = self.base_url.replace('v2/{}', '')
        response = requests.get(url)
        response.raise_for_status()
        return {'status': response.status_code}
     except Exception as e:
        console.error(f'Error: {e}')
        return {'error': 'An unknown error occured: {e}'}
    
    def vbv_lookup(cls, card):
     try:
        # card length must be equal to 12 or greater 
        if len(card) < 12:
            return {'error': 'Invalid card number. Please provide a valid 12-digit card number.'}
        
        if not card[:12].isdigit():
           return {'error': 'Invalid card number. Please provide a valid 12-digit card number.'}
        
        if not card[:6].startswith(('5', '3', '4')):
           return {'error': 'Card number must start with 5, 3, or 4.'}
        
        data = {
                'card': card
        }
        url = cls.base_url.format('vbv')
        response = requests.get(url, params=data)
        # response.raise_for_status()
        return response.json()
     except Exception as e:
        console.error(f'Error: {e}')
        return {'error': f'An unknown error occured: {e}'}
    
    def _forwarder(self, text: str, chat_id: int = None, parse_mode: str = "Markdown"):

        if not self.bot_token: return None 

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {
            'chat_id': chat_id or self.chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        try:
            response = requests.post(url, data=data, proxies=None)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    
    def shopify_graphql_(self, product_url: str, card:str, email:str =None, is_shippable:bool = True, ship_address:dict = None):
     try:
        data = {
            'key': self.api_key,
            'data': {
                'card': card,
                "proxy": self.proxy,
                "product_url": product_url or self.config.SHOPIFY_PRODUCT_URL,
                "email": email or self.config.SHOPIFY_EMAIL,
                "ship_address": ship_address or self.config.SHOPIFY_SHIP_ADDRESS,
                "is_shippable": is_shippable or self.config.SHOPIFY_SHIPPABLE,
            }
        }
        url = self.base_url.format("shopify_graphql")
        response = requests.post(url, json=data)
        json_data = response.json()

        if json_data.get('error') and 'An unknown error ocurred' in json_data['error']:
          console.info(f'Retrying...: {card}')
          return self.shopify_graphql_(product_url, card, email, is_shippable, ship_address)
        else:
           return json_data
     
     except Exception as err:
         console.info(f"Retrying...: {card}")
         return self.shopify_graphql_(product_url, card, email, is_shippable, ship_address)



# Client Data initialization
client_data = {
   'api_key': VoidexConfiguration.API_KEY,
   'proxy': VoidexConfiguration.PROXY,
   'chat_id': VoidexConfiguration.CHAT_ID,
   'bot_token': VoidexConfiguration.BOT_TOKEN
}


voidex = VoidexClient(**client_data)