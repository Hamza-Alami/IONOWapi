import streamlit as st
import requests
import time

@st.cache
def get_bitrix_data():
    base_urls = [
        'https://valead.bitrix24.com/rest/2593/1qypbfjokvl3q7n9/crm.deal.list.json?Filter[STAGE_ID]=C51:WON&',
        'https://valead.bitrix24.com/rest/2593/0yy34uz3ome8hk4o/crm.deal.list.json?Filter[STAGE_ID]=C51:NEW&',
        'https://valead.bitrix24.com/rest/2593/rg46gyrl6kfedteu/crm.deal.list.json?Filter[STAGE_ID]=C51:LOSE&',
        'https://valead.bitrix24.com/rest/2593/tcdo9l8bdswx5t2t/crm.deal.list.json?Filter[STAGE_ID]=C51:1&',
        'https://valead.bitrix24.com/rest/2593/2c0lhsi6b0biyo44/crm.deal.list.json?Filter[STAGE_ID]=C51:EXECUTING&',
        'https://valead.bitrix24.com/rest/2593/vjpem3zwd2k5tzff/crm.deal.list.json?Filter[STAGE_ID]=C51:FINAL_INVOICE&',
        'https://valead.bitrix24.com/rest/2593/tjp12j1b4wp8bap5/crm.deal.list.json?Filter[STAGE_ID]=C51:PREPARATION&'
    ]

    data = []
    for url in base_urls:
        start = 0
        count = 50

        # Retrieve the total number of records
        response = requests.get(f"{url}&start={start}&select[]=ID&count=1")
        total_records = response.json()['total']

        while start < total_records:
            url_with_params = f"{url}&start={start}"
            response = requests.get(url_with_params)
            response_json = response.json()

            data.extend(response_json['result'])
            start += 50  # update start parameter to retrieve next 50 records

    return data

# Get Bitrix data
bitrix_data = get_bitrix_data()

# Create API endpoint
@st.cache
def get_api_data():
    return bitrix_data

api_data = get_api_data()

# Define API endpoint route and response format
@st.cache
def api_endpoint():
    return {
        "/get_data": api_data
    }

# Display API endpoint URL on Streamlit app
# Display API endpoint URL on Streamlit app
if "origin" in st.experimental_get_query_params():
    st.write("API endpoint URL: ", st.experimental_get_query_params()["origin"][0] + "/get_data")
else:
    st.write("API endpoint URL: N/A")

# Run Streamlit app
if __name__ == "__main__":
    app = st.create_web_app(api_endpoint)
    app.run()
