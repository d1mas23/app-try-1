import streamlit as st
st.caption("Dimas Fernandez Advanced HW")
st.title("Crypto Streamlit Web App")


crypto = st.text_input("Enter Crpyto Name Abbreviation (eg BTC)")

currency = st.text_input("Enter Currency Name Abbreviation (eg EUR)")

threshold = st.number_input("Enter threshold for price alert",
                                    min_value = -1,
                                    max_value = 999999999)


import requests
import json

headers = {
'Accepts': 'application/json',
'X-CMC_PRO_API_KEY': st.secrets["API_KEY"],
}
if crypto and currency and threshold:
    response = requests.get(f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?symbol={crypto}&convert={currency}",headers=headers)

    if response.status_code in [200,201]:
        print("success")
        print(json.dumps(response.json(),indent=4))
    else:
        print(f"error {response.status_code} with error: {response.text}")

    price = round(response.json()['data'][crypto][0]['quote'][currency]['price'],2)
else:
    st.info("Please fill all fields above.")



if st.button("Notify me!"):
    st.write(f"The currenct price for {crypto} is {price} in {currency}. We will notify you when price of {crypto} reaches {threshold} {currency}")