from datetime import datetime, timedelta
import random

class Util():

	@classmethod
	def make_boolean(cls, value) -> bool:

		if value is None:
			return False
		elif isinstance(value, int):
			return False if value == 0 else True
		elif isinstance(value, str):
			v = value.lower()
			if v == "true":
				return True
			elif v == "false":
				return False
			elif v == "0":
				return False
			else:
				return True

	@classmethod
	def get_random_date(cls, start, end) -> any:
		"""Generates a random datetime between two datetime objects."""
		delta = end - start
		# Calculate total seconds to allow for random time as well as date
		int_delta = int(delta.total_seconds())
		random_second = random.randrange(int_delta * 1020304)
		return start + timedelta(microseconds=random_second)

	@classmethod
	def parse_date(cls, date_val) -> datetime:
		if isinstance(date_val, datetime):
			return date_val

		# Add support for datetime.date
		if hasattr(date_val, "year") and hasattr(date_val, "month") and hasattr(date_val, "day"):
			# Convert date to datetime at midnight
			return datetime(date_val.year, date_val.month, date_val.day)

		if isinstance(date_val, str):
			for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
				try:
					return datetime.strptime(date_val, fmt)
				except ValueError:
					continue
		raise ValueError(f"Date '{date_val}' is not in a recognized format or type.")
