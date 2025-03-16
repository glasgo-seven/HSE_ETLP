from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from utils import args
from clickhouse import transfer_data

with DAG(
	"ClickHouse Transfer",
	schedule_interval="None",
	start_date=datetime(2024, 1, 1),
	default_args=args,
) as dag:
	transfer_data_task = PythonOperator(
		task_id="transfer_data",
		python_callable=transfer_data
	)

	transfer_data_task
