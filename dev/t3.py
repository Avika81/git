import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import options, parse_command_line, parse_config_file
import logging
import json

import numpy as np
import random
import pulp
import time
import os

import tests_for_t3

we_love_avi = False
d_time = True

d = True
epsilon_1 = 0.01
days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

hours_in_day = 24
days_in_week = 7
hours_in_week = hours_in_day * days_in_week
number_of_weeks = 1 # TOOO remind Oleg it should be accounted in the input
max_time = hours_in_week * number_of_weeks

fine_for_same_game_twice = 0.9
fine_for_twice_a_week = 0.5
fine_for_twice_a_day = 0.5

times = [time.clock()]

def day_to_num(day):
	if   day == ""   : return 0
	elif day == "Sun": return 0
	elif day == "Mon": return 1
	elif day == "Tue": return 2
	elif day == "Wed": return 3
	elif day == "Thu": return 4
	elif day == "Fri": return 5
	elif day == "Sat": return 6

def print_time_diff(input):
	global times
	x = time.time()
	times.append(x)
	if(d_time):
		output = "time of - " + input + " - "
		res =  float(x) - float((times[len(times)-2]))
		output += str(res)
		print(output)
	return

class Time:
	start = 0
	end = 0
	def __init__(self, start, end, day=""):
		self.start = day_to_num(day) * hours_in_day + start
		self.end = day_to_num(day) * hours_in_day + end
	def __eq__(self,other):
		return self.start == other.start
	def __lt__(self,other):
		return self.start < other.start
	def get_week_start(self):
		return int(self.start / hours_in_week)
	def get_day_start(self):
		return int(self.start / hours_in_day)
def tTime(day,start,end):
	return Time(start,end,day)

class Slot:
	id = -1
	location_id = -1  # not relevant atm
	time = Time(-1,-1)
	def __init__(self,id, time, location_id = -1):
		self.id = id
		self.time = time
		self.location_id = location_id

class Event:
	id = -1
	coed = True
	def __init__(self,id,coed):
		self.id = id
		self.coed = coed
	def __eq__(self,other):
		return ((self.id == other.id) and (self.coed == other.coed))

class Team:
	id = -1
	event = -1
	min_number_of_games_to_schedule = -1
	preffered_location = -1
	availabilty = [Time(0,float("inf"))]
	def __init__(self,id, event,min_number_of_games_to_schedule,preffered_location = -1,availabilty=[Time(0,float("inf"))]):
		self.id = id
		self.event = event
		self.min_number_of_games_to_schedule = min_number_of_games_to_schedule
		self.availabilty = -1

class Game:
	id = -1
	is_coed = -1
	first_team = -1
	second_team = -1
	def __init__(self,id,first_team, second_team, is_coed):
		self.id = id
		self.first_team = first_team
		self.second_team = second_team
		self.is_coed = is_coed

	def get_priority(self, slot): #the smaller priority the more the algorithm want to use it.
		priority = 1  # all negative here, as a lot of games is not wanted
		if(self.first_team.preffered_location == slot.location_id):
			priority -= 0.1
		if(self.second_team.preffered_location == slot.location_id):
			priority -= 0.1
		return priority

def could_play(team1,team2):
	if(team1.event == team2.event):
		return True
	else:
		return False

def collision(x,y):
	"""check if the time x intersects with y"""
	if(x.end <= y.start):
		return(False)
	if(x.start >= y.end):
		return(False)
	return(True)

def create_possible_games(teams,number_of_teams):
	games = []
	games_for_each_team = [[] for x in np.arange(number_of_teams)]
	id = 0
	for first_team in np.arange(number_of_teams):
		for second_team in np.arange(number_of_teams):
			if (first_team<second_team):
				if(could_play( teams[first_team], teams[second_team] )):
					new_game = Game(id,teams[first_team],teams[second_team], teams[first_team].event.coed)
					games.append(new_game)
					games_for_each_team[first_team].append(id)
					games_for_each_team[second_team].append(id)

					id += 1

	return (games, games_for_each_team)

def get_index(game, slot,number_of_slots):
	return game * number_of_slots + slot

def team_is_in_game(team,game):
	if((game.first_team.id == team.id) or (game.second_team.id == team.id)):
		return True
	else:
		return False

def get_slot_id_from_var_name(name,number_of_slots,slots):
	str = name[2:]
	var_num = int(str)
	slot = var_num % number_of_slots
	return slots[slot].id

def get_team_ids_str_from_var_name(name, number_of_slots, games):
	stri = name[2:]
	var_num = int(stri)
	game = int(var_num / number_of_slots)
	r = str(str(games[game].first_team.id) + "," + str(games[game].second_team.id))
	return(r)

def valid(v):  #this is a var, return true if it's valid.
	"""
	a variable will be count as not valid if it is one of the soft variables (it is Continuous among other things)
	"""
	if (v.cat == "Continuous"):
		return(False)
	if (v.name[:4] == "coed"):
		return(False)
	return(True)

def set_data_from_json(input):
	data = json.loads(input)
	slots = []
	events = []
	events_dic = {}
	teams = []
	id_slot = 0
	for sl in range(len(data['slots'])):
		slots.append(Slot(id_slot, Time(data['slots'][sl]['start'],
			data['slots'][sl]['end']), data['slots'][sl]['id']))
		id_slot += 1

	for eve in range(len(data['events'])):
		events.append(Event(data['events'][eve]['id'],
			data['events'][eve]['is_coed']))

		events_dic[data['events'][eve]['id']] = Event(data['events'][eve]['id'],
			data['events'][eve]['is_coed'])
	for team in range(len(data['teams'])):
		teams.append(Team(data['teams'][team]['team_id'],
			events_dic[data['teams'][team]['event_id']],
			data['teams'][team]['num_of_games_to_schedule']))
	return (slots,teams)

def set_min_games_per_team(lp_prob, teams, variables, games_for_each_team, number_of_teams, number_of_slots):
	for i_team in np.arange(number_of_teams):
		min_number_wanted = teams[i_team].min_number_of_games_to_schedule
		nc = []
		for i_game in games_for_each_team[i_team]:
			for i_slot in np.arange(number_of_slots):
				nc.append((variables[get_index(i_game,i_slot,number_of_slots)], 1))

		lp_prob += pulp.LpAffineExpression(nc) >= min_number_wanted

def set_max_1_game_per_slot(lp_prob, number_of_slots, number_of_games, variables):
	for i_slot in np.arange(number_of_slots):
		nc = []
		for jj in np.arange(number_of_games):
			nc.append((variables[get_index(jj,i_slot,number_of_slots)],1))
		lp_prob += pulp.LpAffineExpression(nc) <= 1  # max of one game in a single slot

def set_each_team_is_in_one_place_at_each_time(lp_prob, teams, variables, games_for_each_team,
 number_of_teams, number_of_slots):
	big_const = max(100,number_of_slots)

	for slot in np.arange(number_of_slots):
		l = np.zeros(number_of_slots)  # those who intersects with slot.
		# for s in np.arange(number_of_slots):
		# 	if(collision(slots[slot].time, slots[s].time)):
		# 		l[s] = True
		# l[slot] = False

		ll = np.full(number_of_slots, -1)
		i = 0
		for s in np.arange(number_of_slots):
			if(collision(slots[slot].time, slots[s].time) and s!=slot):
				ll[i] = s
				i+=1

		for team in np.arange(number_of_teams):
			nc = []
			nc_t = []
			for game in games_for_each_team[team]:
				nc.append((variables[get_index(game,slot,number_of_slots)], big_const))
				nc_t.append((variables[get_index(game,slot,number_of_slots)], big_const))
				# for s2 in np.arange(number_of_slots):
				# 	if(l[s2]):
				# 		nc.append((variables[get_index(game,s2,number_of_slots)], 1))
				for s2 in np.arange(i):
					if(ll[s2] == -1):
						print("-1")
						break
					nc_t.append((variables[get_index(game,ll[s2],number_of_slots)], 1))
			# if(str(nc) != str(nc_t):
			# 	print("Error!!")
			# 	print()
			lp_prob += pulp.LpAffineExpression(nc_t) <= big_const

def set_target_function_for_regular_variables(c,number_variables,variables, games,slots,number_of_slots, number_of_games):
	for g in np.arange(number_of_games):
		for s in np.arange(number_of_slots):
			# bonus = np.random.uniform(epsilon_1, 2 * epsilon_1 )
			c.append((variables[get_index(g,s,number_of_slots)],-1 * (games[g].get_priority(slots[s])) ))

def set_no_parallel_coed_no_coed(lp_prob, teams, variables, games_for_each_team,
 number_of_teams, number_of_slots, number_of_games, games, c):
	big_const = max(128,number_of_slots)
	coed_variables = pulp.LpVariable.dicts("coed",range(number_of_slots), 0, 1,cat="Binary")  # the variables

	for slot in np.arange(number_of_slots):
		c.append((coed_variables[slot],0))
		#If it is true, than there could not be a non coed game.

		# nc = []
		# nc.append((coed_variables[slot],big_const))
		# for game in np.arange(number_of_games):
		# 	if(games[game].is_coed == 0):
		# 		nc.append((variables[get_index(game,slot,number_of_slots)], 1))
		# lp_prob += pulp.LpAffineExpression(nc) <= big_const

		for game in np.arange(number_of_games):
			if(games[game].is_coed == 0):
				nc = []
				nc.append((coed_variables[slot],1))
				nc.append((variables[get_index(game,slot,number_of_slots)], 1))
				lp_prob += pulp.LpAffineExpression(nc) <= 2


		# #if there is coed -> the variable must be true
		# nc = []
		# nc.append((coed_variables[slot],big_const))
		# for game in np.arange(number_of_games):
		# 	if(games[game].is_coed != 0):
		# 		nc.append((variables[get_index(game,slot,number_of_slots)], -1))
		# lp_prob += pulp.LpAffineExpression(nc) >= 0

		for game in np.arange(number_of_games):
			if(games[game].is_coed != 0):
				nc.append((coed_variables[slot],1))
				nc.append((variables[get_index(game,slot,number_of_slots)], -1))
				lp_prob += pulp.LpAffineExpression(nc) >= 0

		# find intersections:
		ll = np.full(number_of_slots, -1)
		i = 0
		for s in np.arange(number_of_slots):
			if(collision(slots[slot].time, slots[s].time) and s != slot):
				ll[i] = s
				i+=1

		# if two slots intersects, the coed_variable of them should be equal.
		# the equation is : i*x_0 - sum(x_j) == 0 (there are i variables of x_j)
		if(i != 0):
			nc = []
			nc.append((coed_variables[slot],i))

			for i in np.arange(i):
				if(i==-1):
					print("-1")
					break
				nc.append((coed_variables[ll[i]],-1))
			lp_prob += pulp.LpAffineExpression(nc) == 0

			# print(nc)
			# print()
	 # for slot in np.arange(number_of_slots):
		# l = np.zeros(number_of_slots)  # those who intersects with slot.
	 #
		# # for s in np.arange(number_of_slots):
		# # 	if(collision(slots[slot].time, slots[s].time)):
		# # 		l[s] = True
		# # l[slot] = False
	 #
		# ll = np.full(number_of_slots, -1)
		# i = 0
		# for s in np.arange(number_of_slots):
		# 	if(collision(slots[slot].time, slots[s].time) and s!=slot):
		# 		ll[i] = s
		# 		i+=1
		# for game in np.arange(number_of_games):
		# 	nc = []
		# 	nc_t = []
	 #
		# 	nc.append((variables[get_index(game,slot,number_of_slots)], big_const))
		# 	nc_t.append((variables[get_index(game,slot,number_of_slots)], big_const))
		# 	for g in np.arange(number_of_games):
		# 		if(games[g].is_coed != games[game].is_coed):
		# 			# for i in np.arange(number_of_slots):
		# 			# 	if(l[i]):
		# 			# 		nc.append((variables[get_index(g,i,number_of_slots)], 1))
		# 			for i in np.arange(i):
		# 				if(ll[i] == -1):
		# 					break
		# 				nc_t.append((variables[get_index(g,ll[i],number_of_slots)], 1))
	 #
		# 	lp_prob += pulp.LpAffineExpression(nc_t) <= big_const

	# for slot in np.arange(number_of_slots):
	# 	l = np.zeros(number_of_slots)  # those who intersects with slot.
	#
	# 	for s in np.arange(number_of_slots):
	# 		if(collision(slots[slot].time, slots[s].time)):
	# 			l[s] = True
	# 	l[slot] = False
	#
	# 	#is_coed:
	# 	nc = []
	# 	nc.append((is_coed_variables[slot],big_const))
	# 	for i in np.arange(number_of_slots):
	# 		if(l[i]):
	# 			nc.append((not_coed_variables[i],1))
	# 	lp_prob += pulp.LpAffineExpression(nc) <= big_const

# def set_coed_variables(lp_prob, teams, variables, games_for_each_team,
#  number_of_teams, number_of_slots, number_of_games, games), is_coed_variables, not_coed_variables):
# 	big_const = max(100, number_of_games)
# 	for slot in np.arange(number_of_slots):
# 		#only one of them is true:
# 		nc = []
# 		nc.append((is_coed_variables[slot], 1))
# 		nc.append((not_coed_variables[slot], 1))
# 		lp_prob += pulp.LpAffineExpression(nc) == 1
#
# 		#exist coed -> true
# 		# the eq is - sum(x_i - coed games) - big_const * coed_variable
# 		nc = []
# 		nc.append((is_coed_variables[slot], -big_const))
# 		for game in np.arange(number_of_games):
# 			if(games[game].is_coed == True):
# 				nc.append((variables[get_index(game,slot,number_of_slots)], 1))
# 		lp_prob += pulp.LpAffineExpression(nc) <= 0
#
# 		#exist variable is true -> there is no none-coed game up.
# 		nc = []
# 		nc.append((is_coed_variables[slot], big_const))
# 		for game in np.arange(number_of_games):
# 			if(games[game].is_coed == False):
# 				nc.append((variables[get_index(game,slot,number_of_slots)], 1))
# 		lp_prob += pulp.LpAffineExpression(nc)<=big_const

def each_game_happens_once(lp_prob,c,variables, number_variables, number_of_games,
	number_of_slots, number_of_teams, teams, games, slots, fine):
	for game in np.arange(number_of_games):
		nc = []
		for slot in np.arange(number_of_slots):
			nc.append((variables[get_index(game,slot,number_of_slots)], 1))
		ll = str(game) + " once "
		v1 = pulp.LpVariable(name = ll + "elastic_neg", upBound=0)
		nc.append((v1,1))  # if the value is big negative it gives more space
		lp_prob += pulp.LpAffineExpression(nc) <= 1

		c.append((v1,fine))  # the fine is 0.9 (huge).

def each_group_play_once_a_week(lp_prob,c,variables, number_variables, number_of_games,
	number_of_slots, number_of_teams, teams, games, slots, games_for_each_team, fine):
	for team in np.arange(number_of_teams):
		for week in np.arange(number_of_weeks):
			nc = []
			ns = 0
			for slot in np.arange(number_of_slots):
				if(slots[slot].time.get_week_start() == week):
					ns += 1
					for game in games_for_each_team[team]:
						nc.append((variables[get_index(game,slot,number_of_slots)], 1))
			if(ns <= 1):
				continue
			ll = str(team) + " week - " + str(week)
			v1 = pulp.LpVariable(name = ll + "elastic_neg", upBound=0)
			nc.append((v1,1))  # if the value is big negative it gives more space
			lp_prob += pulp.LpAffineExpression(nc) <= 1

			c.append((v1,fine))  # the fine is 0.5.

def each_group_play_once_a_day (lp_prob,c,variables, number_variables, number_of_games,
	number_of_slots, number_of_teams, teams, games, slots, games_for_each_team, fine):
	for team in np.arange(number_of_teams):
		for day in np.arange(number_of_weeks * days_in_week):
			nc = []
			ns = 0
			for slot in np.arange(number_of_slots):
				if(slots[slot].time.get_day_start() == day):
					ns += 1
					for game in games_for_each_team[team]:
						nc.append((variables[get_index(game,slot,number_of_slots)], 1))

			if(ns <= 1):
				continue

			ll = str(team) + " day - " + str(day)
			v1 = pulp.LpVariable(name = ll + "elastic_neg", upBound=0)
			nc.append((v1,1))  # if the value is big negative it gives more space
			lp_prob += pulp.LpAffineExpression(nc) <= 1
			c.append((v1,fine))  # the fine is 0.5.

def solution(slots, teams):
	'''the input is in json format, "slots: ... events: ... Teams: ..." '''
	# (slots, teams) = set_data_from_json(input)
	print_time_diff("start solution")
	number_of_teams = len(teams)

	(games, games_for_each_team) = create_possible_games(teams, number_of_teams)
	print_time_diff("create_possible_games")

	number_of_slots = len(slots)
	number_of_games = len(games)
	number_variables = number_of_games * number_of_slots

	print("num_var: " + str(number_variables) + ", teams: " + str(number_of_teams) + ", slots " + str(number_of_slots) + ", games: " + str(number_of_games))

	variables = pulp.LpVariable.dicts("y",range(number_variables), 0, 1,cat="Binary")  # the variables
	# is_coed_variables = pulp.LpVariable.dicts("is_coed", range(number_of_slots), 0, 1, cat="Binary") # 1 -> in this slot it's coed, 0 otherwise
	# not_coed_variables = pulp.LpVariable.dicts("not_coed", range(number_of_slots), 0, 1, cat="Binary") # 1 -> in this slot it's not coed, 0 otherwise

	lp_prob = pulp.LpProblem("schedule_games", pulp.LpMaximize)  # the lp_prob instance
	print_time_diff("created variables")
	# variables are : 0 - slot-1 those for game1, and so on.  to
	# get x_ij, do
	# i * slot)+j [ using the function get_index ]

	c = []
	set_target_function_for_regular_variables(c,number_variables,variables, games, slots, number_of_slots, number_of_games)
	print_time_diff("set_target_function_for_regular_variables")

	# set_coed_variables(lp_prob, teams, variables, games_for_each_team,
	#  number_of_teams, number_of_slots, number_of_games, games, is_coed_variables, not_coed_variables)

	#there can't be a coed game in parallel to another non-coed game
	set_no_parallel_coed_no_coed(lp_prob, teams, variables, games_for_each_team,
	 number_of_teams, number_of_slots, number_of_games, games,c)
	print_time_diff("set_no_parallel_coed_no_coed")

	# Make sure all teams play as much as needed:
	set_min_games_per_team(lp_prob, teams, variables, games_for_each_team, number_of_teams, number_of_slots)
	print_time_diff("set_min_games_per_team")

	# In each slot there could be only one game.
	set_max_1_game_per_slot(lp_prob, number_of_slots, number_of_games, variables)
	print_time_diff("set_max_1_game_per_slot")
	# Each team is only in one place at a time
	set_each_team_is_in_one_place_at_each_time(lp_prob, teams, variables, games_for_each_team,
	 number_of_teams, number_of_slots)
	print_time_diff("set_each_team_is_in_one_place_at_each_time")

	# soft constraints: !!!!  (they wouldn't surely be happening but
	# there is a fine if they won't
	# (and the algorithm will try to avoid it but not at any cost) [the
	# bigger the fine the more important it is]

	#each game happens once: (not a must)
	each_game_happens_once(lp_prob, c, variables, number_variables, number_of_games,
	 number_of_slots, number_of_teams, teams, games, slots, fine_for_same_game_twice)
	print_time_diff("each_game_happens_once")

	each_group_play_once_a_week(lp_prob,c,variables, number_variables, number_of_games,
	 number_of_slots, number_of_teams, teams, games, slots, games_for_each_team ,fine_for_twice_a_week)
	print_time_diff("each_group_play_once_a_week")

	each_group_play_once_a_day (lp_prob,c,variables, number_variables, number_of_games,
	 number_of_slots, number_of_teams, teams, games, slots, games_for_each_team, fine_for_twice_a_day)
	print_time_diff("each_group_play_once_a_day")

	lp_prob.setObjective(pulp.LpAffineExpression(c))
	print_time_diff("setObjective")
	lp_prob.solve()
	print_time_diff("solved")

	output = '['
	if pulp.LpStatus[lp_prob.status] != "Optimal":
		if(pulp.LpStatus[lp_prob.status] == "Infeasible"):
			output = "The problem is not solveable :(, please try to insert more slots."
		else:
			output = "Error the problem is: " + pulp.LpStatus[lp_prob.status] + "send to Avi he'll fix it"
		return output
	else:
		res = lp_prob.variables()
		for v in res:
			if (v.varValue == 0 or not valid(v)):
				if(not valid(v)):
					if(we_love_avi): print("dd - " + v.cat + " " + str(v.name) + " - " + str(v.varValue))
				continue
			else:
				output += '{"slotid":' + str(get_slot_id_from_var_name(v.name,number_of_slots,slots)) + ','
				output += '"teamsid":' + str(get_team_ids_str_from_var_name(v.name,number_of_slots,games)) + '},'
				if(we_love_avi) : output += "\tvar: " + str(v.name) + " - " + str(v.varValue) + "\n"
				if(d) : output += "\n"
		output = output[:len(output) - 2] + "]"
	return output


# print(tests_for_t3.example_6)
(slots,teams) = set_data_from_json(tests_for_t3.example_6)

# if(we_love_avi):
# 	for s in slots:
# 		print("id - " + str(s.id))
# 		print("Time - start: " +  str(s.time.start) + ", end: " + str(s.time.end))
#
# 	for t in teams:
# 		print("id - " + str(t.id))
# 		print("num_of_games_to_schedule - " + str(t.min_number_of_games_to_schedule))

print(solution(slots, teams))
