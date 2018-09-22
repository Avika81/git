from collections import defaultdict

import numpy as np
import random
import pulp

import classes as classes

epsilon_1 = 0.01
fine_for_extra_game = 0.9

def get_game_from_var_name(name):
    str1 = name[2:]
    return int(str1)

def could_play(team1, team2):
    if team1.event == team2.event:
        return True
    else:
        return False
def valid(v):
    if v.cat == "Continuous":
        return False
    return True
def get_games(teams, number_of_teams):
    output_games = []
    output_for_each_team = {}
    games = []
    games_for_each_team = {}
    for i in np.arange(number_of_teams):
        games_for_each_team.setdefault(teams[i].id, [])
        output_for_each_team.setdefault(teams[i].id, [])
    id = 0
    for first_team in np.arange(number_of_teams):
        for second_team in np.arange(number_of_teams):
            if first_team < second_team:
                if could_play(teams[first_team], teams[second_team]):
                    new_game = classes.Game(id, teams[first_team], teams[second_team], teams[first_team].event.coed)
                    games.append(new_game)
                    games_for_each_team.setdefault(first_team, []).append(id)
                    games_for_each_team.setdefault(second_team, []).append(id)

                    id += 1

    number_of_games = len(games)
    lp_prob_games = pulp.LpProblem("schedule_games", pulp.LpMaximize)  # the lp_prob instance
    variables_games = pulp.LpVariable.dicts("y", range(number_of_games), 0, 1, cat="Binary")  # the variables
    c = []

    for i in np.arange(number_of_games):
        bonus = np.random.uniform(epsilon_1, 2 * epsilon_1)
        c.append((variables_games[i], (1 + bonus)))

    for i_team in np.arange(number_of_teams):
        min_number_wanted = teams[i_team].min_number_of_games_to_schedule
        nc = []
        for i_game in games_for_each_team[i_team]:
            nc.append((variables_games[i_game], 1))
        ll = "extr - t-" + str(i_team)
        v1 = pulp.LpVariable(name=ll + "elastic_neg", upBound=0)
        nc.append((v1, 1))  # if the value is big negative it gives more space
        lp_prob_games += pulp.LpAffineExpression(nc) <= min_number_wanted
        c.append((v1, fine_for_extra_game)) # fine_for_extra_game
    lp_prob_games.setObjective(pulp.LpAffineExpression(c))
    lp_prob_games.solve()

    if pulp.LpStatus[lp_prob_games.status] != "Optimal":
        if pulp.LpStatus[lp_prob_games.status] == "Infeasible":
            print("The problem is not solvable :(, please try to insert more slots.")
        else:
            print("create_games!! Error the problem is: " + pulp.LpStatus[
                lp_prob_games.status] + "send to Avi he'll fix it")
        return []

    else:
        id = 0

        res = lp_prob_games.variables()
        for v in res:
            # if v.varValue == 1:
            if(v.varValue > 0 and valid(v)):
                for i in np.arange(int(v.varValue)):
                    x = get_game_from_var_name(v.name)
                    output_games.append(classes.Game(id, games[x].first_team, games[x].second_team, games[x].is_coed))
                    # output_games.append(games[x])
                    output_for_each_team.setdefault(games[x].first_team.id, []).append(id)
                    output_for_each_team.setdefault(games[x].second_team.id, []).append(id)
                    id += 1
    return output_games, output_for_each_team
