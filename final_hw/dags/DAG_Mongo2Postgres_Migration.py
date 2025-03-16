from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from utils import args
from postgres import migrate_data

with DAG(
	"Mongo2Postgres Migration",
	default_args=args,
	schedule_interval="None",
	start_date=datetime(2024, 1, 1),
) as dag:
	migrate_task = PythonOperator(
		task_id="migrate_user_sessions", python_callable=migrate_data
	)
