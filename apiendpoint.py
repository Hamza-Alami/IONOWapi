import streamlit as st
import requests

@st.cache(suppress_st_warning=True)
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

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_data():
    return get_bitrix_data()

@st.experimental_memoization
def get_records():
    data = get_data()
    records = {"data": data}
    return records

@st.cache(suppress_st_warning=True)
def get_total_records():
    data = get_data()
    total_records = {"total_records": len(data)}
    return total_records

@st.cache(suppress_st_warning=True)
def get_filtered_records(filter_value):
    data = get_data()
    filtered_data = [d for d in data if d['STAGE_ID'] == filter_value]
    records = {"data": filtered_data}
    return records

# Define Streamlit app
def app():
    st.set_page_config(page_title="Bitrix24 Deals Data", page_icon=":money_with_wings:")

    st.header("Bitrix24 Deals Data API")
    st.subheader("All Deals")
    st.markdown("This endpoint returns all the deals data from Bitrix24.")

    records = get_records()
    total_records = get_total_records()

    st.write(records)
    st.write(total)
