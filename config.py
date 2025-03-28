from random import choice
class VoidexConfiguration:

    API_KEY = 'VDX-SHA2X-NZ0RS-O7HAM' # Voidex API key

    BOT_TOKEN = '7754882999:AAEpyYJ81G8w6x41xTQ08RamAb9LAmZf5xQ' # Optional: Telegram bot token
    CHAT_ID = 123 # Optional: Enter your Telegram USER ID

    # Required: Proxy must required
    PROXY = "proxy.speedproxies.net:12321:Indexui184a999e:4fba9e5235e8"

    # Auto Shopify Configuration

    SHOPIFY_PRODUCT_LINKS = [
        "http://smallbizshippingco.com/products/tiktok-live-focal-sale"
    ]
    SHOPIFY_PRODUCT_URL = choice(SHOPIFY_PRODUCT_LINKS) # product url
    SHOPIFY_SHIPPABLE = True # optional: is product shippable
    SHOPIFY_LOCALIZE = False # optional: is product localized
    SHOPIFY_EMAIL = None # optional: customer email
    SHOPIFY_SHIP_ADDRESS = None # optional: ship address in JSON format



    