import prod_games_schedule
import tests_for_t3
import sys

if len(sys.argv) > 1:
	prod_games_schedule.we_love_avi = int(sys.argv[1])
if len(sys.argv) > 2:
	prod_games_schedule.d_time = int(sys.argv[2])
if len(sys.argv) > 3:
	prod_games_schedule.json_with_enters = int(sys.argv[3])
if len(sys.argv) > 4:
	prod_games_schedule.normal_return = int(sys.argv[4])

(slots, teams) = prod_games_schedule.set_data_from_json(tests_for_t3.example_biggg)
print(prod_games_schedule.solution(slots, teams))

# testing
