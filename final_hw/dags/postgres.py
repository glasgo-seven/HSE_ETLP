from datetime import datetime, timedelta
import json

from utils import mongo, postgres


def migrate_data() -> None:
	user_sessions = mongo["raw_data"]["user_sessions"]
	support_tickets = mongo["raw_data"]["support_tickets"]

	last_hour = datetime.now() - timedelta(hours=1)
	sessions = user_sessions.find({"start_time": {"$gte": last_hour}})
	tickets = support_tickets.find({"updated_at": {"$gte": last_hour}})

	with postgres.cursor() as cursor:
		for session in sessions:
			cursor.execute(
				query="""
				INSERT INTO replicated_data.user_sessions 
				VALUES (%s, %s, %s, %s, %s, %s, %s)
				ON CONFLICT (session_id) DO NOTHING
			""",
				vars=(
					session["session_id"],
					session["user_id"],
					session["start_time"],
					session["end_time"],
					json.dumps(session["pages_visited"]),
					json.dumps(session["device"]),
					json.dumps(session["actions"]),
				),
			)

		for ticket in tickets:
			cursor.execute(
				query="""
				INSERT INTO replicated_data.support_tickets 
				VALUES (%s, %s, %s, %s, %s, %s)
				ON CONFLICT (ticket_id) DO NOTHING
			""",
				vars=(
					ticket["ticket_id"],
					ticket["user_id"],
					ticket["status"],
					ticket["issue_type"],
					ticket["created_at"],
					ticket["updated_at"],
				),
			)
			
		postgres.commit()
		postgres.close()
