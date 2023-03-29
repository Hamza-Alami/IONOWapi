import requests
import streamlit as st
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def get_data():
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

    try:
        st.write(f"Retrieved {len(data)} records")
        return jsonify(data)
    except Exception as e:
        st.write(f"Error: {e}")
        return "Failure"

# Start the Flask app using Streamlit's magic command
if __name__ == '__main__':
    from streamlit.hashing import CryptoProtocol
    from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
    from streamlit.server.Server import Server
    
    server = Server()
    server._is_running = True
    server._crypto = CryptoProtocol()
    setattr(
        st,
        REPORT_CONTEXT_ATTR_NAME,
        st.ReportThread.get_or_create_report_ctx()
    )
    app.run(debug=False, port=8080)
