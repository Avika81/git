import numpy as np

hours_in_day = 24
days_in_week = 7
hours_in_week = hours_in_day * days_in_week
epsilon_1 = 0.0001

def day_to_num(day):
	if day == "":
		return 0
	elif day == "Sun":
		return 0
	elif day == "Mon":
		return 1
	elif day == "Tue":
		return 2
	elif day == "Wed":
		return 3
	elif day == "Thu":
		return 4
	elif day == "Fri":
		return 5
	elif day == "Sat":
		return 6


class Time:
	start = 0
	end = 0

	def __init__(self, start, end, day=""):
		self.start = day_to_num(day) * hours_in_day + start
		self.end = day_to_num(day) * hours_in_day + end

	def __eq__(self, other):
		return self.start == other.start and self.end == other.end

	def __lt__(self, other):
		return self.start < other.start

	def get_week_start(self):
		return int(self.start / hours_in_week)

	def get_day_start(self):
		return int(self.start / hours_in_day)


def tTime(day, start, end):
	return Time(start, end, day)


class Slot:
	id = -1
	location_id = -1  # not relevant atm
	time = Time(-1, -1)
	# priority = 1

	def __init__(self, id, time, unavailable_entries = [], location_id = -1):
		self.id = id
		self.time = time
		self.unavailable_entries = unavailable_entries
		self.location_id = location_id
		# priority = 1 + np.random.uniform(epsilon_1, 2 * epsilon_1)


class Multi_Slot:
	id = -1
	time = Time(-1,-1)
	slots = []
	unavailable_entries = []
	def __init__(self, id, time, unavailable_entries, slots):
		self.id = id
		self.time = time
		self.unavailable_entries = unavailable_entries
		self.slots = slots


class Event:
	id = -1
	coed = True

	def __init__(self, id, coed):
		self.id = id
		self.coed = coed

	def __eq__(self, other):
		return ((self.id == other.id) and (self.coed == other.coed))


class Team:
	id = -1
	event = -1
	min_number_of_games_to_schedule = -1
	preffered_location = -1
	availabilty = [Time(0, float("inf"))]

	def __init__(self, id, event, min_number_of_games_to_schedule, preffered_location=-1,
				 availabilty=[Time(0, float("inf"))]):
		self.id = id
		self.event = event
		self.min_number_of_games_to_schedule = min_number_of_games_to_schedule
		self.availabilty = -1


class Game:
	id = -1
	is_coed = -1
	first_team = -1
	second_team = -1

	def __init__(self, id, first_team, second_team, is_coed):
		self.id = id
		self.first_team = first_team
		self.second_team = second_team
		self.is_coed = is_coed

	def get_priority(self, slot):  # the smaller priority the more the algorithm want to use it.
		priority = 1  # all negative here, as a lot of games is not wanted
		if (self.first_team.preffered_location == slot.location_id):
			priority += 0.1
		if (self.second_team.preffered_location == slot.location_id):
			priority += 0.1
		return priority
