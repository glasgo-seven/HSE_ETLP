from datetime import datetime

import pymongo
import psycopg2
from clickhouse_driver import Client

args = {
	'owner': 'airflow',
	'start_date': datetime(2024, 3, 1),
}


mongo = pymongo.MongoClient(
	host="localhost",
	port=27017,
	username="root",
	password="example",
)

postgres = psycopg2.connect(
	dbname='airflow',
	user='airflow',
	password='airflow',
	host='postgres'
)

click = Client(
	host='localhost',
	user='admin',
	password='secret'
)
