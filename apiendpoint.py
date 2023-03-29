import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import datetime as dt
from datetime import timedelta
import os, sys
import base64
import plost
import requests
import io
import xlsxwriter
from io import BytesIO
import lxml
import json
from datetime import date
import time

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


print(f"Retrieved {len(data)} records")
