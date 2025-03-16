from datetime import datetime, timedelta
import random
import uuid

from utils import mongo


N_ROWS = 777


def generate_user_session() -> dict:
	return {
		"session_id":		str(random.randint(10**3, 10**6)),
		"user_id":			random.randint(10**1, 10**3),
		"start_time":		datetime.now(),
		"end_time":			datetime.now() + timedelta(minutes=random.randint(1, 60)),
		"pages_visited":	["/home", "/product"],
		"device":			{"type": "mobile", "os": "Android"},
		"actions":			["click", "scroll"]
	}


def generate_support_ticket() -> dict:
	return {
		"ticket_id":	str(object=uuid.uuid4()),
		"user_id":		random.randint(10**1, 10**3),
		"status":		random.choice(["open", "closed", "pending"]),
		"issue_type":	random.choice(["technical", "billing", "general"]),
		"created_at":	datetime.now(),
		"updated_at":	datetime.now()
	}


def generate_data() -> None:
	collection = mongo["raw_data"]["user_sessions"]
	support_tickets = mongo["raw_data"]["support_tickets"]

	documents: list[dict] = [
		generate_user_session() for _ in range(N_ROWS)
	]

	tickets: list[dict] = [
		generate_support_ticket() for _ in range(N_ROWS)
	]

	collection.insert_many(documents)
	support_tickets.insert_many(tickets)
