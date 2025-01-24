Top 10 Largest Banks by Market Capitalization: ETL Project

This project implements an ETL (Extract, Transform, Load) pipeline to process data about the top 10 largest banks in the world by market capitalization. The pipeline extracts the data from a public source, transforms it into multiple currencies using exchange rates, and loads the processed data into both a CSV file and a SQLite database. Managers from different regions can query the data to retrieve market capitalization values in their respective currencies.

Project Overview

A multinational firm has tasked you with creating an automated pipeline to extract and process data on the top 10 largest banks by market capitalization. The data must be accessible in the following currencies:
	•	USD
	•	GBP
	•	EUR
	•	INR

The processed data will be saved in:
	1.	CSV file: A local file for sharing and reporting.
	2.	SQL database: A table for executing queries based on regions.

Features
	•	Data Extraction:
	•	Extracts data on the top 10 largest banks from a specified URL.
	•	Data Transformation:
	•	Converts market capitalization values from USD to GBP, EUR, and INR.
	•	Uses exchange rate information from a provided CSV file.
	•	Rounds values to 2 decimal places.
	•	Data Loading:
	•	Saves the transformed data to a CSV file.
	•	Creates a database table with the processed data.
	•	Query Execution:
	•	Allows managers to retrieve information for specific regions:
	•	London (GBP)
	•	Berlin (EUR)
	•	New Delhi (INR)
	•	Logging:
	•	Logs all stages of the ETL process for traceability and debugging.

Setup Instructions

Prerequisites

To run this project, ensure you have:
	•	Python 3.x installed
	•	Virtual environment (recommended)
	•	Required libraries:
	•	pandas
	•	requests
	•	sqlite3
	•	logging

Installation
	1.	Clone this repository:

git clone <repository_url>
cd top_10_banks


	2.	Install the dependencies:

pip install -r requirements.txt


	3.	Prepare the exchange rates CSV file:
	•	Add exchange rate data to exchange_rates.csv in the following format:

Currency,Exchange_Rate_to_USD
GBP,0.73
EUR,0.85
INR,74.57

Running the Project
	1.	Activate the virtual environment:

source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows


	2.	Run the main script:

python main.py


	3.	Review logs in project_log.txt for progress and troubleshooting.

Project Workflow
	1.	Extract: Fetch data from the URL containing the table “By Market Capitalization.”
	2.	Transform:
	•	Convert market capitalization values to GBP, EUR, and INR.
	•	Round results to 2 decimal places.
	3.	Load:
	•	Save the transformed data to Top_10_Banks.csv.
	•	Load the transformed data into a SQLite database as the table Top_10_Banks.
	4.	Query:
	•	Run SQL queries to extract information for:
	•	London office: SELECT Name, MC_GBP_Billion FROM Top_10_Banks
	•	Berlin office: SELECT Name, MC_EUR_Billion FROM Top_10_Banks
	•	New Delhi office: SELECT Name, MC_INR_Billion FROM Top_10_Banks

Sample Outputs
	•	Processed CSV file: Top_10_Banks.csv
	•	SQLite database table: Top_10_Banks in Banks.db

Logging

All stages of the ETL process are logged in the file project_log.txt, including:
	•	Start and end of extraction, transformation, and loading steps.
	•	Any errors encountered during execution.

Future Enhancements
	•	Automate periodic updates of exchange rates.
	•	Add support for additional currencies.
	•	Enable visualization of the processed data.

Author

Aliaksandr Krasnou
Contact: Krasnou_Aliaksandr@gmail.com