# Code for ETL operations on Country-GDP data

# Importing the required libraries

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import logging
import sqlite3
from datetime import datetime

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
exchange_rates_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"

conn = sqlite3.connect('Banks.db')
table_name = 'Largest_banks'
table_attribs_initial = ['Name', 'MC_USD_Billion']
table_attribs_final = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
csv_path = './exchange_rate.csv'
output_path = './Largest_banks_data.csv'
log_file = './log.txt'



def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    timestamp_format = '%Y-%h-%d %H:%M:%S,%f'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, 'a') as f:
        f.write(timestamp + ' : ' + message + '\n')
    return message
     

def extract(url):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    
    print(log_progress('Preliminaries complete. Initiating ETL process'))
    
    html_page = requests.get(url).text # returns the HTML content of the page
    soup = BeautifulSoup(html_page, 'html.parser') 
    tables = soup.find_all('table') # returns a list of all the tables in the page
    print(log_progress(f"Number of tables fetched: {len(tables)}"))
    rows = tables[0].find_all('tr') # returns a list of all the rows in the table
    print(log_progress(f"Number of rows defined: {len(rows)}"))
    df = pd.DataFrame()
    for row in rows:
        columns = row.find_all('td') # returns a list of all the columns in the row
        if columns: # checks if the row has columns
            bank_name = columns[1].text.strip()
            try:
                market_cap = float(columns[2].text.strip())
            except ValueError:
                market_cap = float('inf')
            
            df = pd.concat([df, pd.DataFrame({'Name': [bank_name], 'MC_USD_Billion': [market_cap]})], ignore_index=True)
    print(log_progress('Data extraction complete. Initiating Transformation process'))
    return df



def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    
    exchange_rates = pd.read_csv(csv_path) # returns a data frame with exchange rates
    print(log_progress('Exchange rates fetched'))
    dict_exchange_rates = exchange_rates.set_index('Currency').to_dict()['Rate']
    df['MC_GBP_Billion'] = [np.round(x * dict_exchange_rates['GBP'],2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * dict_exchange_rates['EUR'],2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * dict_exchange_rates['INR'],2) for x in df['MC_USD_Billion']]
    print(log_progress('Data transformation complete. Initiating Loading process'))
    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path, index=False)
    print(log_progress('Data saved to CSV file'))

def load_to_db(df, conn, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    print(log_progress('SQL Connection initiated'))
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()
    print(log_progress('Data loaded to Database as a table, Executing queries'))


def run_query(query_statement, conn):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    conn = sqlite3.connect('Banks.db')
    try:
            # Execute the query and fetch results
            cursor = conn.cursor()
            cursor.execute(query_statement)
            results = cursor.fetchall()
            
            # Print results
            for row in results:
                print(row)
                
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
    conn.close()
    print(log_progress('\nProcess Complete \n'))
    


''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

df = extract(url)
df = transform(df, csv_path)

load_to_db(df, conn, table_name)
print('\nAll largest banks:')
run_query('SELECT * FROM Largest_banks', conn)
print('Average market cap in GBP:')
run_query('SELECT AVG(MC_GBP_Billion) FROM Largest_banks', conn)
print('First 5 largest banks:')
run_query('SELECT Name from Largest_banks LIMIT 5', conn)

