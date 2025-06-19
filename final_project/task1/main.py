import ydb
import ydb.iam
import pandas as pd
import time

endpoint = "grpcs://ydb.serverless.yandexcloud.net:2135"
database = "/ru-central1/b1gndgb3tmrd9vtrhv4v/etnrsc3eor53g7e35gvv"
sa_key_file = "C:\\test\\authorized_key.json"

driver = ydb.Driver(
	endpoint=endpoint,
	database=database,
	credentials=ydb.iam.ServiceAccountCredentials.from_file(sa_key_file)
)
driver.wait(timeout=5)

session_pool = ydb.SessionPool(driver)

with session_pool.checkout() as session:
	try:
		session.describe_table("cancerdata")
	except ydb.Error:
		session.execute_scheme("""
				CREATE TABLE cancerdata (
					id Uint64,
					age Double,
					gender Utf8,
					country Utf8,
					diagnosisdate Date,
					cancerstage Utf8,
					familyhistory Uint64,
					smokingstatus Utf8,
					bmi Double,
					cholesterollevel Int32,
					hypertension Uint64,
					asthma Uint64,
					cirrhosis Uint64,
					othercancer Uint64,
					treatmenttype Utf8,
					endtreatmentdate Date,
					survived Uint64,
					PRIMARY KEY (id)
				);
			   """)

df = pd.read_csv("./dataset.csv")

for i in range(9500, len(df), 500):
	time.sleep(10)
	batch = df[i:i + 500]
	values = ", ".join([f"("
						f"{row['id']}, {row['age']}, '{row['gender']}', "
						f"'{row['country']}', CAST(Date('{row['diagnosis_date']}') AS Date), '{row['cancer_stage']}',"
						f"{1 if row['family_history'] == 'Yes' else 0}, '{row['smoking_status']}', {row['bmi']},"
						f"{row['cholesterol_level']}, {row['hypertension']}, {row['asthma']},"
						f"{row['cirrhosis']}, {row['other_cancer']}, '{row['treatment_type']}', "
						f"CAST(Date('{row['end_treatment_date']}') AS Date), {row['survived']}"
						f")"
						for _, row in batch.iterrows()])
	query = f"""
		UPSERT INTO cancerdata (
			id,
			age,
			gender,
			country,
			diagnosisdate,
			cancerstage,
			familyhistory,
			smokingstatus,
			bmi,
			cholesterollevel,
			hypertension,
			asthma,
			cirrhosis,
			othercancer,
			treatmenttype,
			endtreatmentdate,
			survived
		)
		VALUES {values}
		;
	"""
	with session_pool.checkout() as session:
		session.transaction().execute(
			query,
			commit_tx=True
		)
		print(i)
