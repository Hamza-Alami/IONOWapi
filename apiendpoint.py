import requests
import json
import streamlit as st

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

# convert data to JSON format
json_data = json.dumps(data)

# get the URL of the Streamlit app
streamlit_url = st.get_share_streamlit_url()

# print the URL on the Streamlit page
st.write("Use this URL to access the data in Power BI:")
st.write(streamlit_url)

# serve the data as a JSON file
response = requests.Response()
response.headers['Content-Type'] = 'application/json'
response.headers['Content-Disposition'] = 'attachment; filename=data.json'
response.content = json_data.encode('utf-8')

# return the response
st.write("Here is a sample of the data:")
st.json(data[:10])
st.write("To download the full data set, right-click the link below and select 'Save link as':")
st.markdown(f'<a href="data:application/json;base64,{response.content.decode("utf-8")}" download="data.json">Download data as JSON file</a>', unsafe_allow_html=True)
