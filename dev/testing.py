import games_schedule
import pulp
import tests_for_t3 as tests_for_t3
import sys
from subprocess import call

folder_of_tests = '/home/avi_kadria/Desktop/scheduler/working/dev/tests'

if len(sys.argv) > 1:
	games_schedule.we_love_avi = int(sys.argv[1])
if len(sys.argv) > 2:
	games_schedule.d_time = int(sys.argv[2])
if len(sys.argv) > 3:
	games_schedule.json_with_enters = int(sys.argv[3])
if len(sys.argv) > 4:
	games_schedule.normal_return = int(sys.argv[4])

if(games_schedule.we_love_avi):
	default_name = folder_of_tests + '/debug_'
else:
	default_name = folder_of_tests + '/result_'

for i in range(len(tests_for_t3.list_of_tests)):
	new_file_name = default_name
	new_file_name += str(i)
	new_file_name += ".txt"
	new_file = open(new_file_name, "w")
	(slots, teams) = games_schedule.set_data_from_json(tests_for_t3.list_of_tests[i])
	sys.stdout = new_file
	print(str(games_schedule.solution(slots, teams)))

# i = 17
# new_file_name = default_name
# new_file_name += str(i)
# new_file_name += ".txt"
# new_file = open(new_file_name, "w")
# (slots, teams) = games_schedule.set_data_from_json(tests_for_t3.list_of_tests[i])
# sys.stdout = new_file
# print(str(games_schedule.solution(slots, teams)))

# new_file.write(str(games_schedule.solution(slots, teams)))

# pulp.pulpTestAll()

# testing
