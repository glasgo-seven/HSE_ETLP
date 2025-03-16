from airflow import DAG
from airflow.operators.python import PythonOperator

from utils import args
from mongo import generate_data

with DAG(
	"Mongo DataGen",
	default_args=args,
	schedule_interval="None",
	catchup=False,
) as dag:
	generate_task = PythonOperator(
		task_id="generate_mongo_data", python_callable=generate_data
	)

	generate_task
