import streamlit as st
from flask import Flask, jsonify

app = Flask(__name__)

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
    response = requests.get(f"{url}&start={start}&select[]=ID&count=1", allow_redirects=False)
    total_records = response.json()['total']
    print(f"Total records for {url}: {total_records}")

    while start < total_records:
        url_with_params = f"{url}&start={start}"
        response = requests.get(url_with_params, allow_redirects=False)
        response_json = response.json()
        print(f"Response for {url_with_params}: {response_json}")

        data.extend(response_json['result'])
        start += 50  # update start parameter to retrieve next 50 records


# Serve the data as a JSON API
@app.route('/data')
def serve_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8000)

