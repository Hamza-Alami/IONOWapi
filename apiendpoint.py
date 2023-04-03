import requests
import streamlit as st
import json

# Base URLs for Bitrix API

# Retrieve data from Bitrix API
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


# Save data to a file
with open("data.json", "w") as f:
    f.write(json.dumps(data))

# Add a download button for the data.json file
with open("data.json", "r") as f:
    file_data = f.read()

st.download_button(
    label="Download data.json",
    data=file_data,
    file_name="data.json",
    mime="application/json"
)

# Print success message
st.success("Data saved to data.json")

