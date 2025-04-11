from random import choice
class VoidexConfiguration:

    API_KEY = 'VDX-SHA2X-NZ0RS-O7HAM' # Voidex API key

    BOT_TOKEN = '7754882999:AAEpyYJ81G8w6x41xTQ08RamAb9LAmZf5xQ' # Optional: Telegram bot token
    CHAT_ID = -1002046472570 # Optional: Enter your Telegram USER ID

    # Required: Proxy must required
    PROXY = "proxy-jet.io:1010:250408Fvg3J-resi-any:JgYRMvcQrx4PdOu"

    # Auto Shopify Configuration

    SHOPIFY_PRODUCT_LINKS = [
        "https://racfmiracles.org/products/be-a-miracle-maker"
    ]
    SHOPIFY_PRODUCT_URL = choice(SHOPIFY_PRODUCT_LINKS) # product url
    SHOPIFY_SHIPPABLE = False # optional: is product shippable
    SHOPIFY_LOCALIZE = False # optional: is product localized
    SHOPIFY_EMAIL = None # optional: customer email
    SHOPIFY_SHIP_ADDRESS = None # optional: ship address in JSON format



    