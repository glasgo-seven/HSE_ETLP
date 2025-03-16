from utils import click, postgres


def transfer_data() -> None:
	with postgres.cursor() as cursor:
		cursor.execute("""
			SELECT 
				DATE(start_time) AS date,
				user_id,
				COUNT(*) AS sessions,
				SUM(JSONB_ARRAY_LENGTH(pages_visited)) AS page_views
			FROM replicated_data.user_sessions
			GROUP BY date, user_id
		""")

		click.execute(
			"INSERT INTO user_activity_daily VALUES",
			[(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()],
		)

		cursor.execute("""
			SELECT 
				DATE_TRUNC('day', created_at) AS day,
				status,
				COUNT(*) AS ticket_count,
				AVG(EXTRACT(EPOCH FROM (updated_at - created_at))) AS avg_time
			FROM replicated_data.support_tickets
			GROUP BY day, status
		""")

		click.execute(
			"INSERT INTO support_performance VALUES",
			[(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()],
		)

		cursor.execute("""
			SELECT
				u.user_id,
				MAX(DATE(u.start_time)) AS last_active,
				COUNT(DISTINCT u.session_id) AS sessions,
				COUNT(t.ticket_id) AS tickets,
				coalesce(AVG(EXTRACT(EPOCH FROM (t.updated_at - t.created_at))), -1) AS avg_response
			FROM replicated_data.user_sessions u
			LEFT JOIN replicated_data.support_tickets t ON u.user_id = t.user_id
			GROUP BY u.user_id
	""")

		click.execute(
			"INSERT INTO activity_tickets VALUES",
			[(row[0], row[1], row[2], row[3], row[4]) for row in cursor.fetchall()],
		)

		cursor.close()
		postgres.close()
