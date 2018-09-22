import json
import sys
import time

import numpy as np
import pulp
from itertools import chain
# import tests_for_t3

import dev.classes as classes
import dev.get_games as get_games

# from settings import settings

we_love_avi = False  # is the first command_line argument
d_time = False  # is the second command_line argument
normal_return = True  # is the third command_line argument

epsilon_1 = 0.01
days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

hours_in_day = 24
days_in_week = 7
hours_in_week = hours_in_day * days_in_week

fine_for_same_game_twice = 2 # can't be lower than 1 or the algorithm is irrelevant
fine_for_twice_a_week = 0.2
fine_for_twice_a_day = 0.3
fine_for_twice_in_2_days = 0.1

times = [time.clock()]


def print_time_diff(input):
    global times
    x = time.time()
    times.append(x)
    if d_time:
        output = "time of - " + input + " - "
        res = float(x) - float((times[len(times) - 2]))
        output += str(res)
        print(output)
    return


def collision(x, y):
    """check if the time x intersects with y"""
    if x.end <= y.start:
        return False
    if x.start >= y.end:
        return False
    return True


def create_possible_games(teams, number_of_teams):
    output = []
    games = []
    games_for_each_team = [[] for x in np.arange(number_of_teams)]
    id = 0
    for first_team in np.arange(number_of_teams):
        for second_team in np.arange(number_of_teams):
            if first_team < second_team:
                if get_games.could_play(teams[first_team], teams[second_team]):
                    new_game = classes.Game(id, teams[first_team], teams[second_team], teams[first_team].event.coed)
                    games.append(new_game)
                    games_for_each_team[first_team].append(id)
                    games_for_each_team[second_team].append(id)

                    id += 1
    return games, games_for_each_team


def get_index(game, slot, number_of_slots):
    return game * number_of_slots + slot


def team_is_in_game(team, game):
    if (game.first_team.id == team.id) or (game.second_team.id == team.id):
        return True
    else:
        return False


def get_multi_slot_id_from_var_name(name, number_of_multi_slots):
    str = name[2:]
    var_num = int(str)
    multi_slot = var_num % number_of_multi_slots
    return multi_slot


def get_game_id_from_var_name(name, number_of_slots):
    stri = name[2:]
    var_num = int(stri)
    game = int(var_num / number_of_slots)
    return game


def get_team_ids_str_from_var_name(name, number_of_slots, games):
    game = get_game_id_from_var_name(name, number_of_slots)

    return games[game].first_team.id, games[game].second_team.id


def valid(v):  # this is a var, return true if it's valid.
    """
    a variable will be count as not valid if it is one of the soft variables (it is Continuous among other things)
    """
    if v.cat == "Continuous":
        return False
    if var_type(v) == "coed":
        return False
    return True


def var_type(v):
    return v.name[:4]


def set_data_from_json(input):
    data = json.loads(input)
    slots = []
    events = []
    events_dic = {}
    teams = []
    for sl, obj in enumerate(data['slots']):
        slots.append(classes.Slot(data['slots'][sl]['id'], classes.Time(data['slots'][sl]['start'],
                                                                        data['slots'][sl]['end']),
                                  data['slots'][sl]['unavailable_entries'],
                                  data['slots'][sl]['id']))

    for eve, obj in enumerate(data['events']):
        events.append(classes.Event(data['events'][eve]['id'],
                                    data['events'][eve]['is_coed']))

        events_dic[data['events'][eve]['id']] = classes.Event(data['events'][eve]['id'],
                                                              data['events'][eve]['is_coed'])
    for team, obj in enumerate(data['teams']):
        teams.append(classes.Team(data['teams'][team]['team_id'],
                                  events_dic[data['teams'][team]['event_id']],
                                  data['teams'][team]['num_of_games_to_schedule']))
    return slots, teams


def set_min_games_per_team(lp_prob, teams, variables, games_for_each_team, number_of_teams, number_of_slots):
    for index, teamObj in enumerate(teams):
        i_team = teamObj.id
        min_number_wanted = teams[i_team].min_number_of_games_to_schedule
        nc = []
        for i_game in games_for_each_team[i_team]:
            for i_slot in np.arange(number_of_slots):
                nc.append((variables[get_index(i_game, i_slot, number_of_slots)], 1))

        lp_prob += pulp.LpAffineExpression(nc) >= min_number_wanted


def set_max_games_per_multi_slot(lp_prob, multi_slots, number_of_multi_slots, number_of_games, variables):
    for i_slot in np.arange(number_of_multi_slots):
        max_games = len(multi_slots[i_slot].slots)
        nc = []
        for jj in np.arange(number_of_games):
            nc.append((variables[get_index(jj, i_slot, number_of_multi_slots)], 1))
        lp_prob += pulp.LpAffineExpression(nc) <= max_games  # max of one game in a single slot


def there_is_smaller_collision(slot, number_of_slots, slots):
    for s in np.arange(number_of_slots):
        if collision(slots[slot].time, slots[s].time) and s != slot:
            if s < slot:
                return False
    return True


def set_each_team_is_in_one_place_at_each_time(lp_prob, teams, variables, games_for_each_team,
                                                number_of_teams, number_of_multi_slots, slots):
    big_const = max(100, number_of_multi_slots)

    for slot in np.arange(number_of_multi_slots):
        if there_is_smaller_collision(slot, number_of_multi_slots, slots):
            continue

        ll = np.full(number_of_slots, -1)
        i = 0
        for s in np.arange(number_of_slots):
            if collision(slots[slot].time, slots[s].time) and s != slot:
                ll[i] = s
                i += 1

        for index, teamObj in enumerate(teams):
            team = teamObj.id
            nc = []
            nc_t = []
            for game in games_for_each_team[team]:
                nc.append((variables[get_index(game, slot, number_of_slots)], big_const))
                nc_t.append((variables[get_index(game, slot, number_of_slots)], big_const))
                # for s2 in np.arange(number_of_slots):
                #     if(l[s2]):
                #         nc.append((variables[get_index(game,s2,number_of_slots)], 1))
                for s2 in np.arange(i):
                    if ll[s2] == -1:
                        print("-1")
                        break
                    nc_t.append((variables[get_index(game, ll[s2], number_of_slots)], 1))
            # if(str(nc) != str(nc_t):
            #     print("Error!!")
            #     print()
            lp_prob += pulp.LpAffineExpression(nc_t) <= big_const


# def set_that_every_game_is_played_once(lp_prob, teams, variables, number_of_games, number_of_teams, number_of_slots):
#     for g in np.arange(number_of_games):
#         nc = []
#         for s in np.arange(number_of_slots):
#             nc.append((variables[get_index(g, s, number_of_slots)], 1))
#         lp_prob += pulp.LpAffineExpression(nc) == 1


def set_target_function_for_regular_variables(c, number_variables, variables, games, slots, number_of_multi_slots,
                                              number_of_games):
    for g in np.arange(number_of_games):
        for s in np.arange(number_of_multi_slots):
            # bonus = np.random.uniform(epsilon_1, 2 * epsilon_1 )
            c.append((variables[get_index(g, s, number_of_multi_slots)], (games[g].get_priority(slots[s]))))


def set_no_parallel_coed_no_coed(lp_prob, teams, variables, games_for_each_team,
                                 number_of_teams, number_of_multi_slots, number_of_games, games, c, slots, multi_slots):
    big_const = number_of_multi_slots + 1
    coed_variables = pulp.LpVariable.dicts("coed", range(number_of_multi_slots), 0, 1, cat="Binary")  # the variables

    for slot in np.arange(number_of_multi_slots):
        ll = np.full(number_of_multi_slots, -1)
        i = 0

        c.append((coed_variables[slot], 0))
        n_coed = 0

        # If it is true, than there could not be a non coed game.
        nc = []
        nc.append((coed_variables[slot], big_const))
        for game in np.arange(number_of_games):
            if games[game].is_coed == 0:
                nc.append((variables[get_index(game, slot, number_of_multi_slots)], 1))
        lp_prob += pulp.LpAffineExpression(nc) <= big_const

        # if there is coed -> the variable must be true
        nc = []
        nc.append((coed_variables[slot], big_const))
        for game in np.arange(number_of_games):
            if games[game].is_coed != 0:
                nc.append((variables[get_index(game, slot, number_of_multi_slots)], -1))
        lp_prob += pulp.LpAffineExpression(nc) >= 0

        # find intersections:
        ll = np.full(number_of_multi_slots, -1)
        i = 0
        for s in np.arange(number_of_multi_slots):
            if collision(multi_slots[slot].time, multi_slots[s].time) and s != slot:
                ll[i] = s
                i += 1

        # if two slots intersects, the coed_variable of them should be equal.
        # the equation is : i*x_0 - sum(x_j) == 0 (there are i variables of x_j)
        # if there_is_smaller_collision(slot, number_of_slots, slots):
        #     continue

        if i != 0:
            print("I > 0 !! ")
            nc = []
            nc.append((coed_variables[slot], i))

            for i in np.arange(i):
                if i == -1:
                    print("-1")
                    break
                nc.append((coed_variables[ll[i]], -1))
            lp_prob += pulp.LpAffineExpression(nc) == 0


def each_game_happens_once(lp_prob, c, variables, number_variables, number_of_games,
                            number_of_multi_slots, number_of_teams, teams, games, slots, fine):
    for game in np.arange(number_of_games):
        nc = []
        for slot in np.arange(number_of_multi_slots):
            nc.append((variables[get_index(game, slot, number_of_multi_slots)], 1))
        ll = "once - " + str(game)
        v1 = pulp.LpVariable(name=ll + "elastic_neg", upBound=0)
        nc.append((v1, 1))  # if the value is big negative it gives more space
        lp_prob += pulp.LpAffineExpression(nc) <= 1

        c.append((v1, fine))  # the fine is huge.


def each_group_play_once_a_week(lp_prob, c, variables, number_variables, number_of_games,
                                number_of_multi_slots, number_of_teams, teams, games, multi_slots,
                                games_for_each_team, fine, number_of_weeks):
    if(we_love_avi): print("week - " + str(games_for_each_team))
    for index, teamObj in enumerate(teams):
        team = teamObj.id
        for week in np.arange(number_of_weeks):
            nc = []
            ns = 0
            for slot in np.arange(number_of_multi_slots):
                if multi_slots[slot].time.get_week_start() == week:
                    ns += 1
                    for game in games_for_each_team[team]:
                       nc.append((variables[get_index(game, slot, number_of_multi_slots)], 1))
            if ns <= 1:
                continue
            ll = "week - t-" + str(team) + ", w-" + str(week)
            v1 = pulp.LpVariable(name=ll + "elastic_neg", upBound=0)
            nc.append((v1, 1))  # if the value is big negative it gives more space
            lp_prob += pulp.LpAffineExpression(nc) <= 1

            c.append((v1, fine))  # the fine is 0.5.


def each_group_play_once_a_day(lp_prob, c, variables, number_variables, number_of_games,
                                number_of_multi_slots, number_of_teams, teams, games, multi_slots,
                                games_for_each_team, fine, number_of_days):
    for index, teamObj in enumerate(teams):
        team = teamObj.id
        for day in np.arange(number_of_days):
            nc = []
            ns = 0
            for slot in np.arange(number_of_multi_slots):
                if multi_slots[slot].time.get_day_start() == day:
                    ns += 1
                    for game in games_for_each_team[team]:
                        nc.append((variables[get_index(game, slot, number_of_multi_slots)], 1))

            if ns <= 1:
                continue

            ll = "1day - t- " + str(team) + ", d- " + str(day)
            v1 = pulp.LpVariable(name=ll + "elastic_neg", upBound=0)
            nc.append((v1, 1))  # if the value is big negative it gives more space
            lp_prob += pulp.LpAffineExpression(nc) <= 1

            c.append((v1, fine))

def set_availability_for_teams(lp_prob, games, multi_slots, number_of_multi_slots, number_of_games, variables):
    for i_slot in np.arange(number_of_multi_slots):
        for g in np.arange(number_of_games):
            if(games[g].first_team.id in multi_slots[i_slot].unavailable_entries or
                    games[g].second_team.id in multi_slots[i_slot].unavailable_entries):
                nc = [(variables[get_index(g,i_slot,number_of_multi_slots)], 1)]  #kill this variable
                lp_prob += pulp.LpAffineExpression(nc) <= 0
                # print("game - [" + str(g.first_team.id) + "can't be in slot" + str(i_slot))

# def each_group_play_once_in_2_days (lp_prob,c,variables, number_variables, number_of_games,
#     number_of_slots, number_of_teams, teams, games, slots, games_for_each_team, fine, number_of_days):
#
#     for team in np.arange(number_of_teams):
#         for day in np.arange(number_of_days):
#             nc = []
#             ns = 0
#             for slot in np.arange(number_of_slots):
#                 if(slots[slot].time.get_day_start() == day or slots[slot].time.get_day_start() == day + 1):
#                     ns += 1
#                     for game in games_for_each_team[team]:
#                         nc.append((variables[get_index(game,slot,number_of_slots)], 1))
#
#             if(ns <= 1):
#                 continue
#
#             ll = "2day - t- " + str(team) + ", d- " + str(day)
#             v1 = pulp.LpVariable(name = ll + "elastic_neg", upBound=0)
#             nc.append((v1,1))  # if the value is big negative it gives more space
#             lp_prob += pulp.LpAffineExpression(nc) <= 1
#
#             c.append((v1,fine))

# def each_group_play_once_in_4_days (lp_prob,c,variables, number_variables, number_of_games,
#     number_of_slots, number_of_teams, teams, games, slots, games_for_each_team, fine, number_of_days):
#
#     for team in np.arange(number_of_teams):
#         for day in np.arange(number_of_days):
#             nc = []
#             ns = 0
#             for slot in np.arange(number_of_slots):
#                 if(slots[slot].time.get_day_start() == day or slots[slot].time.get_day_start() == day):
#                     ns += 1
#                     for game in games_for_each_team[team]:
#                         nc.append((variables[get_index(game,slot,number_of_slots)], 1))
#
#             if(ns <= 1):
#                 continue
#
#             ll = "4day - t- " + str(team) + ", d- " + str(day)
#             v1 = pulp.LpVariable(name = ll + "elastic_neg", upBound=0)
#             nc.append((v1,1))  # if the value is big negative it gives more space
#             lp_prob += pulp.LpAffineExpression(nc) <= 1
#
#             c.append((v1,fine))

def maximal_ending_time(slots):
    m = 0
    for slot in slots:
        m = max(m, slot.time.end)
    return m


def get_output(lp_prob, number_of_slots, number_of_multi_slots, games,
                multi_slots, slots, teams):
    output = []

    if pulp.LpStatus[lp_prob.status] != "Optimal":
        if pulp.LpStatus[lp_prob.status] == "Infeasible":
            output = "The problem is not solveable :(, please try to insert more slots."
        else:
            output = "Error the problem is: " + pulp.LpStatus[lp_prob.status] + "send to Avi he'll fix it"
        return output
    else:
        res = lp_prob.variables()
        for v in res:
            if v.varValue == 0 or not valid(v):
                if not valid(v):
                    if we_love_avi:
                        if v.varValue != 0 and var_type(v) != 'coed':
                            # print("type - " + var_type(v))
                            print("sadly, there is - " + v.name + ", of - " + str(v.varValue))
                        if var_type(v) == 'coed':
                            print(v.name + " is " + str(v.varValue))
                continue
            else:
                multi_slot_id = get_multi_slot_id_from_var_name(v.name, number_of_multi_slots)
                inner_slot_id = np.random.randint(len(multi_slots[multi_slot_id].slots))
                output.append({
                    'slotId': multi_slots[multi_slot_id].slots[inner_slot_id].id,
                    'teamsId': get_team_ids_str_from_var_name(v.name, number_of_multi_slots, games),
                })
                if(we_love_avi):
                    print("multi_slot_id - " + str(multi_slot_id) + "team - " +
                        str(get_team_ids_str_from_var_name(v.name, number_of_multi_slots, games)))

                del multi_slots[multi_slot_id].slots[inner_slot_id]
                game_id = get_game_id_from_var_name(v.name, number_of_multi_slots)
                games[game_id].first_team.min_number_of_games_to_schedule -=  1
                games[game_id].second_team.min_number_of_games_to_schedule -=  1

    return output

def combine_slots(slots):
    number_of_slots = len(slots)
    t_slots = slots
    ll = np.zeros(number_of_slots)
    mult_slots = []
    for s1 in np.arange(number_of_slots):
        if(ll[s1] == 0):
            tslots = [t_slots[s1]]
            for s2 in np.arange(number_of_slots):
                if(slots[s1].time == t_slots[s2].time and s2 != s1):
                    tslots.append(t_slots[s2])
                    ll[s2] = 1
            mult_slots.append(classes.Multi_Slot(tslots[0].id, tslots[0].time, tslots[0].unavailable_entries, tslots))
    return mult_slots

def solution(slots, teams):
    multi_slots = combine_slots(slots)
    print_time_diff("combine_slots")
    output = subsolution(multi_slots,teams, slots)

    for i in range(4):
        res = subsolution(multi_slots, teams, slots)
        if isinstance(res, dict):
            output += res

    return output

def temp_reload(games, games_for_each_team, slots, teams):
    games = games
    games_for_each_team = games_for_each_team
    slots = slots
    teams = teams
    return

def subsolution(multi_slots, teams, slots):
    '''The input is in two lists, one for slots and one for the teams '''

    # (slots, teams) = set_data_from_json(input)
    print_time_diff("start solution")
    number_of_teams = len(teams)

    max_time = maximal_ending_time(slots)
    number_of_days = max_time / hours_in_day + 1
    number_of_weeks = max_time / hours_in_week + 1


    (games, games_for_each_team) = get_games.get_games(teams, number_of_teams)
    # if(len(games) < 1): return []

    if(we_love_avi): print(games)
    if(we_love_avi): print(games_for_each_team)
    print_time_diff("get_game")

    temp_reload(games, games_for_each_team, slots, teams)
    number_of_slots = len(slots)
    number_of_multi_slots = len(multi_slots)
    number_of_games = len(games)
    number_variables = number_of_games * number_of_multi_slots

    if we_love_avi:
        print("num_var: " + str(number_variables) + ", teams: " + str(number_of_teams)
              + ", slots " + str(number_of_slots) + ", games: " + str(number_of_games)
              + ", multi_slots" + str(number_of_multi_slots) +  "\n")


    variables = pulp.LpVariable.dicts("y", range(number_variables), 0, 1, cat="Binary")  # the variables
    # is_coed_variables = pulp.LpVariable.dicts("is_coed", range(number_of_slots), 0, 1, cat="Binary") # 1 -> in this slot it's coed, 0 otherwise
    # not_coed_variables = pulp.LpVariable.dicts("not_coed", range(number_of_slots), 0, 1, cat="Binary") # 1 -> in this slot it's not coed, 0 otherwise

    lp_prob = pulp.LpProblem("schedule_games", pulp.LpMaximize)  # the lp_prob instance
    print_time_diff("created variables")
    # variables are : 0 - slot-1 those for game1, and so on.  to
    # get x_ij, do
    # i * slot)+j [ using the function get_index ]

    c = []
    set_target_function_for_regular_variables(c, number_variables, variables, games, slots, number_of_multi_slots,
                                              number_of_games)
    print_time_diff("set_target_function_for_regular_variables")

    temp_reload(games, games_for_each_team, slots, teams)

    set_max_games_per_multi_slot(lp_prob, multi_slots, number_of_multi_slots, number_of_games, variables)
    print_time_diff("set_max_games_per_multi_slot")


    set_availability_for_teams(lp_prob, games, multi_slots, number_of_multi_slots, number_of_games, variables)
    print_time_diff("set_availability_for_teams")

    # Each team is only in one place at a time - irrelevant,
    # note - assuming that intersection is always all the slot.
    # set_each_team_is_in_one_place_at_each_time(lp_prob, teams, variables, games_for_each_team,
    #                                             number_of_teams, number_of_multi_slots, slots)
    # print_time_diff("set_each_team_is_in_one_place_at_each_time")

    # there can't be a coed game in parallel to another non-coed game
    set_no_parallel_coed_no_coed(lp_prob, teams, variables, games_for_each_team,
                                 number_of_teams, number_of_multi_slots, number_of_games,
                                 games, c, slots, multi_slots)
    print_time_diff("set_no_parallel_coed_no_coed")

    temp_reload(games, games_for_each_team, slots, teams)

    # soft constraints: !!!!  (they wouldn't surely be happening but
    # there is a fine if they won't
    # (and the algorithm will try to avoid it but not at any cost) [the
    # bigger the fine the more important it is]

    temp_reload(games, games_for_each_team, slots, teams)

    # each game happens only once
    each_game_happens_once(lp_prob, c, variables, number_variables, number_of_games,
                            number_of_multi_slots, number_of_teams, teams, games, slots, fine_for_same_game_twice)

    print_time_diff("each_game_happens_once")

    temp_reload(games, games_for_each_team, slots, teams)

    each_group_play_once_a_week(lp_prob, c, variables, number_variables, number_of_games,
                                    number_of_multi_slots, number_of_teams, teams, games, multi_slots,
                                    games_for_each_team, fine_for_twice_a_week, number_of_weeks)
    print_time_diff("each_group_play_once_a_week")

    each_group_play_once_a_day(lp_prob, c, variables, number_variables, number_of_games,
                                number_of_multi_slots, number_of_teams, teams, games, multi_slots, games_for_each_team,
                                fine_for_twice_a_day, number_of_days)
    print_time_diff("each_group_play_once_a_day")

    # soft_if_in_same_day_then_no_breaks()

    lp_prob.setObjective(pulp.LpAffineExpression(c))
    print_time_diff("setObjective")

    # lp_prob.solve(pulp.CBC().solve())
    lp_prob.solve()
    print_time_diff("solve")

    output = get_output(lp_prob, number_of_slots, number_of_multi_slots, games,
                        multi_slots, slots, teams)
    print_time_diff("get_output")

    return output
