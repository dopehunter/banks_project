import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import logging
import sqlite3
from datetime import datetime

url = "https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks"
exchange_rates_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"

conn = sqlite3.connect('Banks.db')
table_name = 'Largest_banks'
table_attribs_initial = ['Name', 'MC_USD_Billion']
table_attribs_final = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
output_csv_path = './Largest_banks_data.csv'
log_file = './log.txt'

def log_progress(message):
    timestamp_format = '%Y-%h-%d %H:%M:%S,%f'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, 'a') as f:
        f.write(timestamp + ' : ' + message + '\n')
