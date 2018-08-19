#tests:
#first test - Avi
'''
	time1 = Time(0,2)
	event1 = Event(1,1)

	teams = [ Team(x,event1,3) for x in range(7) ]

	slots = [Slot(x, Time(x*500,x*500+2)) for x in range(11)]
'''
# first test - Michael
'''
	slots = [Slot(0,Time(8,9),1),
		Slot(1,Time(9,10),1),
		Slot(2,Time(32,33),1),
		Slot(3,Time(33,34),1),
		Slot(4,Time(56,57),1),
		Slot(5,Time(57,58),1)
	]

	event1 = Event(1,False)

	teams = [ Team(1,event1,3),
	 Team(2,event1,3),
	 Team(3,event1,3),
	 Team(4,event1,3)
	]

		output (the order of games isn't important) :

		result:
		0 - [1,3]
		1 - [2,4]
		2 - [2,3]
		3 - [1,4]
		4 - [3,4]
		5 - [1,2]
'''

#second test - Michael
'''
	event1 = Event(1,True)

	slots = [Slot(0,Time(8,9),1),
	Slot(1,Time(8,9),2),
	Slot(2,Time(32,33),3),
	Slot(3,Time(32,33),4),
	]
	teams = [Team(x+1, event1, 2) for x in range(4)]

	#result:
	# 0 - [1,2]
	# 1 - [2,3]
	# 2 - [1,4]
	# 3 - [3,4]
'''

#test 3 - Michael
'''
	slots = [Slot(0,Time(8,9),1),
	Slot(1,Time(9,10),2),
	Slot(2,Time(32,33),3),
	Slot(3,Time(33,34),4),
	Slot(4,Time(56,57),5),
	Slot(5,Time(57,58),6),
	Slot(6,Time(8,9),7),
	Slot(7,Time(32,33),8),
	Slot(8,Time(56,57),9)
	]

	events = [Event(1,True), Event(2,False)]

	teams = [Team(1,events[0],3),
	Team(2,events[0],3),
	Team(3,events[0],3),
	Team(4,events[0],3),
	Team(5,events[1],1),
	Team(6,events[1],1),
	Team(7,events[1],1)
	]

	result -
	[{"slotid":0,"teamsid":2,4},
	{"slotid":1,"teamsid":5,7},
	{"slotid":3,"teamsid":3,4},
	{"slotid":4,"teamsid":1,4},
	{"slotid":5,"teamsid":6,7},
	{"slotid":6,"teamsid":1,3},
	{"slotid":7,"teamsid":1,2},
	{"slotid":8,"teamsid":2,3}]
'''

#test 4 - Michael
example_4 = '{"slots":[{"id":0,"start":8,"end":9},{"id":1,"start":8,"end":9},{"id":2,"start":9,"end":10},{"id":3,"start":9,"end":10},{"id":4,"start":32,"end":33},{"id":5,"start":32,"end":33},{"id":6,"start":33,"end":34},{"id":7,"start":56,"end":57},{"id":8,"start":56,"end":57},{"id":9,"start":57,"end":58},{"id":10,"start":58,"end":59},{"id":11,"start":80,"end":81},{"id":12,"start":80,"end":81},{"id":13,"start":81,"end":82},{"id":14,"start":81,"end":82},{"id":11,"start":104,"end":105},{"id":12,"start":104,"end":105},{"id":13,"start":105,"end":106},{"id":14,"start":127,"end":128},{"id":15,"start":128,"end":129},{"id":16,"start":129,"end":130},{"id":17,"start":153,"end":154}],"events":[{"id":1,"is_coed":true},{"id":2,"is_coed":false}],"teams":[{"team_id":1,"event_id":1,"num_of_games_to_schedule":4},{"team_id":2,"event_id":1,"num_of_games_to_schedule":4},{"team_id":3,"event_id":1,"num_of_games_to_schedule":4},{"team_id":4,"event_id":1,"num_of_games_to_schedule":4},{"team_id":5,"event_id":1,"num_of_games_to_schedule":4},{"team_id":6,"event_id":2,"num_of_games_to_schedule":5},{"team_id":7,"event_id":2,"num_of_games_to_schedule":5},{"team_id":8,"event_id":2,"num_of_games_to_schedule":5},{"team_id":9,"event_id":2,"num_of_games_to_schedule":5}]}'
''' result:
	{"slotid":0,"teamsid":7,8},
	{"slotid":1,"teamsid":1,3},
	{"slotid":2,"teamsid":2,4},
	{"slotid":4,"teamsid":1,2},
	{"slotid":5,"teamsid":6,8},
	{"slotid":6,"teamsid":7,9},
	{"slotid":7,"teamsid":7,9},
	{"slotid":8,"teamsid":2,5},
	{"slotid":10,"teamsid":3,4},
	{"slotid":11,"teamsid":1,4},
	{"slotid":12,"teamsid":6,7},
	{"slotid":13,"teamsid":3,5},
	{"slotid":14,"teamsid":8,9},
	{"slotid":15,"teamsid":4,5},
	{"slotid":16,"teamsid":6,8},
	{"slotid":17,"teamsid":2,3},
	{"slotid":18,"teamsid":7,9},
	{"slotid":19,"teamsid":6,8},
	{"slotid":20,"teamsid":1,5},
	{"slotid":21,"teamsid":6,9}}
'''

example_4_t = '{"slots":[{"id":0,"start":8,"end":9},{"id":1,"start":8,"end":9},{"id":2,"start":9,"end":10},{"id":3,"start":9,"end":10},{"id":4,"start":32,"end":33},{"id":5,"start":32,"end":33},{"id":6,"start":33,"end":34},{"id":7,"start":56,"end":57},{"id":8,"start":56,"end":57},{"id":9,"start":57,"end":58},{"id":10,"start":58,"end":59},{"id":11,"start":104,"end":105},{"id":12,"start":104,"end":105},{"id":13,"start":105,"end":106},{"id":14,"start":127,"end":128},{"id":15,"start":128,"end":129},{"id":16,"start":129,"end":130},{"id":17,"start":153,"end":154}],"events":[{"id":1,"is_coed":true},{"id":2,"is_coed":false}],"teams":[{"team_id":1,"event_id":1,"num_of_games_to_schedule":4},{"team_id":2,"event_id":1,"num_of_games_to_schedule":4},{"team_id":3,"event_id":1,"num_of_games_to_schedule":4},{"team_id":4,"event_id":1,"num_of_games_to_schedule":4},{"team_id":5,"event_id":1,"num_of_games_to_schedule":4},{"team_id":6,"event_id":2,"num_of_games_to_schedule":5},{"team_id":7,"event_id":2,"num_of_games_to_schedule":5},{"team_id":8,"event_id":2,"num_of_games_to_schedule":5},{"team_id":9,"event_id":2,"num_of_games_to_schedule":5}]}'

# result - the problem is not solveable.

example_4_tt = '{"slots":[{"id":0,"start":8,"end":9},{"id":1,"start":8,"end":9},{"id":2,"start":9,"end":10},{"id":3,"start":9,"end":10},{"id":4,"start":32,"end":33},{"id":5,"start":32,"end":33},{"id":6,"start":33,"end":34},{"id":7,"start":56,"end":57},{"id":8,"start":56,"end":57},{"id":9,"start":57,"end":58},{"id":10,"start":58,"end":59},{"id":11,"start":80,"end":81},{"id":12,"start":80,"end":81},{"id":13,"start":81,"end":82},{"id":14,"start":81,"end":82},{"id":11,"start":104,"end":105},{"id":12,"start":104,"end":105},{"id":13,"start":105,"end":106},{"id":14,"start":127,"end":128},{"id":15,"start":128,"end":129},{"id":16,"start":129,"end":130},{"id":17,"start":153,"end":154}],"events":[{"id":1,"is_coed":true},{"id":2,"is_coed":false}],"teams":[{"team_id":1,"event_id":1,"num_of_games_to_schedule":4},{"team_id":2,"event_id":1,"num_of_games_to_schedule":4},{"team_id":3,"event_id":1,"num_of_games_to_schedule":4},{"team_id":4,"event_id":1,"num_of_games_to_schedule":4},{"team_id":5,"event_id":1,"num_of_games_to_schedule":4},{"team_id":6,"event_id":2,"num_of_games_to_schedule":4},{"team_id":7,"event_id":2,"num_of_games_to_schedule":4},{"team_id":8,"event_id":2,"num_of_games_to_schedule":4},{"team_id":9,"event_id":2,"num_of_games_to_schedule":4}]}'

'''results:
	[{"slotid":11,"teamsid":1,2},
	{"slotid":4,"teamsid":2,4},
	{"slotid":19,"teamsid":2,5},
	{"slotid":18,"teamsid":3,4},
	{"slotid":13,"teamsid":3,5},
	{"slotid":17,"teamsid":4,5},
	{"slotid":15,"teamsid":6,7},
	{"slotid":21,"teamsid":6,7},
	{"slotid":7,"teamsid":6,8},
	{"slotid":20,"teamsid":6,9},
	{"slotid":0,"teamsid":7,8},
	{"slotid":8,"teamsid":7,9},
	{"slotid":6,"teamsid":8,9},
	{"slotid":14,"teamsid":8,9},
	{"slotid":16,"teamsid":1,3},
	{"slotid":3,"teamsid":1,4},
	{"slotid":9,"teamsid":1,5},
	{"slotid":10,"teamsid":2,3}]
'''

example_4_ttt = '{"slots":[{"id":0,"start":8,"end":9},{"id":1,"start":8,"end":9},{"id":2,"start":9,"end":10},{"id":3,"start":9,"end":10},{"id":4,"start":32,"end":33},{"id":5,"start":32,"end":33},{"id":6,"start":33,"end":34},{"id":7,"start":56,"end":57},{"id":8,"start":56,"end":57},{"id":9,"start":57,"end":58},{"id":10,"start":58,"end":59},{"id":11,"start":104,"end":105},{"id":12,"start":104,"end":105},{"id":13,"start":105,"end":106},{"id":14,"start":127,"end":128},{"id":15,"start":128,"end":129},{"id":16,"start":129,"end":130},{"id":17,"start":153,"end":154}],"events":[{"id":1,"is_coed":true},{"id":2,"is_coed":false}],"teams":[{"team_id":1,"event_id":1,"num_of_games_to_schedule":4},{"team_id":2,"event_id":1,"num_of_games_to_schedule":4},{"team_id":3,"event_id":1,"num_of_games_to_schedule":4},{"team_id":4,"event_id":1,"num_of_games_to_schedule":4},{"team_id":5,"event_id":1,"num_of_games_to_schedule":4},{"team_id":6,"event_id":2,"num_of_games_to_schedule":4},{"team_id":7,"event_id":2,"num_of_games_to_schedule":4},{"team_id":8,"event_id":2,"num_of_games_to_schedule":4},{"team_id":9,"event_id":2,"num_of_games_to_schedule":4}]}'

'''results:
	[{"slotid":12,"teamsid":2,4},
	{"slotid":0,"teamsid":2,5},
	{"slotid":1,"teamsid":3,4},
	{"slotid":15,"teamsid":1,2},
	{"slotid":14,"teamsid":3,5},
	{"slotid":9,"teamsid":4,5},
	{"slotid":7,"teamsid":6,7},
	{"slotid":11,"teamsid":6,7},
	{"slotid":17,"teamsid":6,8},
	{"slotid":3,"teamsid":6,9},
	{"slotid":2,"teamsid":7,8},
	{"slotid":5,"teamsid":7,9},
	{"slotid":8,"teamsid":8,9},
	{"slotid":10,"teamsid":1,3},
	{"slotid":16,"teamsid":8,9},
	{"slotid":4,"teamsid":1,4},
	{"slotid":13,"teamsid":1,5},
	{"slotid":6,"teamsid":2,3}]
'''

example_4_final = '{"slots":[{"id":0,"start":8,"end":9},{"id":1,"start":8,"end":9},{"id":2,"start":9,"end":10},{"id":3,"start":9,"end":10},{"id":4,"start":32,"end":33},{"id":5,"start":32,"end":33},{"id":6,"start":33,"end":34},{"id":7,"start":56,"end":57},{"id":8,"start":56,"end":57},{"id":9,"start":57,"end":58},{"id":10,"start":58,"end":59},{"id":11,"start":80,"end":81},{"id":12,"start":80,"end":81},{"id":13,"start":81,"end":82},{"id":14,"start":127,"end":128},{"id":15,"start":128,"end":129},{"id":16,"start":129,"end":130},{"id":17,"start":153,"end":154}],"events":[{"id":1,"is_coed":true},{"id":2,"is_coed":false}],"teams":[{"team_id":1,"event_id":1,"num_of_games_to_schedule":4},{"team_id":2,"event_id":1,"num_of_games_to_schedule":4},{"team_id":3,"event_id":1,"num_of_games_to_schedule":4},{"team_id":4,"event_id":1,"num_of_games_to_schedule":4},{"team_id":5,"event_id":1,"num_of_games_to_schedule":4},{"team_id":6,"event_id":2,"num_of_games_to_schedule":4},{"team_id":7,"event_id":2,"num_of_games_to_schedule":4},{"team_id":8,"event_id":2,"num_of_games_to_schedule":4},{"team_id":9,"event_id":2,"num_of_games_to_schedule":4}]}'
'''results:
	[{"slotid":5,"teamsid":2,5},
	{"slotid":4,"teamsid":3,4},
	{"slotid":14,"teamsid":1,2},
	{"slotid":12,"teamsid":3,5},
	{"slotid":16,"teamsid":4,5},
	{"slotid":1,"teamsid":6,7},
	{"slotid":6,"teamsid":6,7},
	{"slotid":13,"teamsid":6,8},
	{"slotid":10,"teamsid":6,9},
	{"slotid":9,"teamsid":7,8},
	{"slotid":7,"teamsid":1,3},
	{"slotid":15,"teamsid":7,9},
	{"slotid":0,"teamsid":8,9},
	{"slotid":17,"teamsid":8,9},
	{"slotid":11,"teamsid":1,4},
	{"slotid":2,"teamsid":1,5},
	{"slotid":3,"teamsid":2,3},
	{"slotid":8,"teamsid":2,4}]

'''

example_5 = '{"slots":[{"id":0,"start":8,"end":9},{"id":1,"start":8,"end":9},{"id":2,"start":9,"end":10},{"id":3,"start":9,"end":10},{"id":4,"start":32,"end":33},{"id":5,"start":32,"end":33},{"id":6,"start":33,"end":34},{"id":7,"start":56,"end":57},{"id":8,"start":56,"end":57},{"id":9,"start":57,"end":58},{"id":10,"start":58,"end":59},{"id":11,"start":80,"end":81},{"id":12,"start":80,"end":81},{"id":13,"start":81,"end":82},{"id":14,"start":81,"end":82},{"id":15,"start":104,"end":105},{"id":16,"start":104,"end":105},{"id":17,"start":105,"end":106}],"events":[{"id":1,"is_coed":true},{"id":2,"is_coed":false}],"teams":[{"team_id":1,"event_id":1,"num_of_games_to_schedule":4},{"team_id":2,"event_id":1,"num_of_games_to_schedule":4},{"team_id":3,"event_id":1,"num_of_games_to_schedule":4},{"team_id":4,"event_id":1,"num_of_games_to_schedule":4},{"team_id":5,"event_id":1,"num_of_games_to_schedule":4},{"team_id":6,"event_id":2,"num_of_games_to_schedule":4},{"team_id":7,"event_id":2,"num_of_games_to_schedule":4},{"team_id":8,"event_id":2,"num_of_games_to_schedule":4},{"team_id":9,"event_id":2,"num_of_games_to_schedule":4}]}'
'''results:
	[{"slotid":15,"teamsid":2,4},
	{"slotid":5,"teamsid":2,5},
	{"slotid":1,"teamsid":3,4},
	{"slotid":16,"teamsid":3,5},
	{"slotid":10,"teamsid":4,5},
	{"slotid":6,"teamsid":6,7},
	{"slotid":11,"teamsid":6,7},
	{"slotid":2,"teamsid":1,2},
	{"slotid":7,"teamsid":6,8},
	{"slotid":0,"teamsid":6,9},
	{"slotid":3,"teamsid":7,8},
	{"slotid":8,"teamsid":1,3},
	{"slotid":9,"teamsid":7,9},
	{"slotid":12,"teamsid":8,9},
	{"slotid":17,"teamsid":8,9},
	{"slotid":4,"teamsid":1,4},
	{"slotid":13,"teamsid":1,5},
	{"slotid":14,"teamsid":2,3}]
'''

example_6 = '{"slots":[{"id":0,"start":1,"end":2},{"id":1,"start":1,"end":2},{"id":2,"start":1,"end":2},{"id":3,"start":2,"end":3},{"id":4,"start":2,"end":3},{"id":5,"start":2,"end":3},{"id":6,"start":3,"end":4},{"id":7,"start":3,"end":4},{"id":8,"start":3,"end":4},{"id":9,"start":4,"end":5},{"id":10,"start":4,"end":5},{"id":11,"start":4,"end":5},{"id":12,"start":25,"end":26},{"id":13,"start":26,"end":27},{"id":14,"start":27,"end":28},{"id":15,"start":28,"end":29},{"id":16,"start":29,"end":30},{"id":17,"start":30,"end":31},{"id":18,"start":31,"end":32},{"id":19,"start":49,"end":50},{"id":20,"start":50,"end":51},{"id":21,"start":51,"end":52},{"id":22,"start":52,"end":53},{"id":23,"start":53,"end":54},{"id":24,"start":54,"end":55},{"id":25,"start":55,"end":56},{"id":26,"start":73,"end":74},{"id":27,"start":74,"end":75},{"id":28,"start":75,"end":76},{"id":29,"start":76,"end":77},{"id":30,"start":77,"end":78},{"id":31,"start":97,"end":98},{"id":32,"start":98,"end":99},{"id":33,"start":99,"end":100},{"id":34,"start":100,"end":101},{"id":35,"start":169,"end":170},{"id":36,"start":169,"end":170},{"id":37,"start":170,"end":171},{"id":38,"start":170,"end":171},{"id":39,"start":171,"end":172},{"id":40,"start":171,"end":172},{"id":41,"start":172,"end":173},{"id":42,"start":172,"end":173},{"id":43,"start":173,"end":174},{"id":44,"start":173,"end":174},{"id":45,"start":174,"end":175},{"id":46,"start":174,"end":175},{"id":47,"start":175,"end":176},{"id":48,"start":193,"end":194},{"id":49,"start":194,"end":195},{"id":50,"start":195,"end":196},{"id":51,"start":196,"end":197},{"id":52,"start":197,"end":198},{"id":53,"start":198,"end":199},{"id":54,"start":199,"end":200},{"id":55,"start":200,"end":201},{"id":56,"start":217,"end":218},{"id":57,"start":218,"end":219},{"id":58,"start":219,"end":220},{"id":59,"start":220,"end":221},{"id":60,"start":221,"end":222},{"id":61,"start":241,"end":242},{"id":62,"start":242,"end":243},{"id":63,"start":243,"end":244},{"id":64,"start":244,"end":245},{"id":65,"start":245,"end":246},{"id":66,"start":265,"end":266},{"id":67,"start":266,"end":267},{"id":68,"start":267,"end":268},{"id":69,"start":268,"end":269},{"id":70,"start":269,"end":270}],"events":[{"id":1,"is_coed":false},{"id":2,"is_coed":true},{"id":3,"is_coed":false},{"id":4,"is_coed":false}],"teams":[{"team_id":0,"event_id":1,"num_of_games_to_schedule":4},{"team_id":1,"event_id":1,"num_of_games_to_schedule":4},{"team_id":2,"event_id":1,"num_of_games_to_schedule":4},{"team_id":3,"event_id":1,"num_of_games_to_schedule":4},{"team_id":4,"event_id":1,"num_of_games_to_schedule":4},{"team_id":5,"event_id":1,"num_of_games_to_schedule":4},{"team_id":6,"event_id":1,"num_of_games_to_schedule":4},{"team_id":7,"event_id":1,"num_of_games_to_schedule":4},{"team_id":8,"event_id":2,"num_of_games_to_schedule":4},{"team_id":9,"event_id":2,"num_of_games_to_schedule":4},{"team_id":10,"event_id":2,"num_of_games_to_schedule":4},{"team_id":11,"event_id":2,"num_of_games_to_schedule":4},{"team_id":12,"event_id":2,"num_of_games_to_schedule":4},{"team_id":13,"event_id":2,"num_of_games_to_schedule":4},{"team_id":14,"event_id":2,"num_of_games_to_schedule":4},{"team_id":15,"event_id":2,"num_of_games_to_schedule":4},{"team_id":16,"event_id":3,"num_of_games_to_schedule":4},{"team_id":17,"event_id":3,"num_of_games_to_schedule":4},{"team_id":18,"event_id":3,"num_of_games_to_schedule":4},{"team_id":19,"event_id":3,"num_of_games_to_schedule":4},{"team_id":20,"event_id":3,"num_of_games_to_schedule":4},{"team_id":21,"event_id":3,"num_of_games_to_schedule":4},{"team_id":22,"event_id":3,"num_of_games_to_schedule":4},{"team_id":23,"event_id":4,"num_of_games_to_schedule":4},{"team_id":24,"event_id":4,"num_of_games_to_schedule":4},{"team_id":25,"event_id":4,"num_of_games_to_schedule":4},{"team_id":26,"event_id":4,"num_of_games_to_schedule":4},{"team_id":27,"event_id":4,"num_of_games_to_schedule":4},{"team_id":28,"event_id":4,"num_of_games_to_schedule":4},{"team_id":29,"event_id":4,"num_of_games_to_schedule":4},{"team_id":30,"event_id":4,"num_of_games_to_schedule":4},{"team_id":31,"event_id":4,"num_of_games_to_schedule":4},{"team_id":32,"event_id":4,"num_of_games_to_schedule":4},{"team_id":33,"event_id":4,"num_of_games_to_schedule":4},{"team_id":34,"event_id":4,"num_of_games_to_schedule":4}]}'

'''results:
    [{"slotid":20,"teamsid":32,34},
    {"slotid":67,"teamsid":2,6},
    {"slotid":48,"teamsid":2,7},
    {"slotid":64,"teamsid":3,5},
    {"slotid":13,"teamsid":3,6},
    {"slotid":5,"teamsid":3,7},
    {"slotid":26,"teamsid":4,5},
    {"slotid":70,"teamsid":4,7},
    {"slotid":11,"teamsid":8,9},
    {"slotid":42,"teamsid":8,12},
    {"slotid":50,"teamsid":8,13},
    {"slotid":22,"teamsid":8,15},
    {"slotid":36,"teamsid":0,4},
    {"slotid":30,"teamsid":9,10},
    {"slotid":55,"teamsid":9,11},
    {"slotid":56,"teamsid":9,14},
    {"slotid":7,"teamsid":10,12},
    {"slotid":19,"teamsid":0,5},
    {"slotid":31,"teamsid":10,13},
    {"slotid":59,"teamsid":10,15},
    {"slotid":40,"teamsid":11,12},
    {"slotid":68,"teamsid":11,13},
    {"slotid":4,"teamsid":11,14},
    {"slotid":24,"teamsid":12,14},
    {"slotid":33,"teamsid":0,6},
    {"slotid":57,"teamsid":13,15},
    {"slotid":65,"teamsid":14,15},
    {"slotid":14,"teamsid":16,18},
    {"slotid":66,"teamsid":16,19},
    {"slotid":51,"teamsid":16,20},
    {"slotid":27,"teamsid":16,21},
    {"slotid":23,"teamsid":17,18},
    {"slotid":58,"teamsid":17,19},
    {"slotid":54,"teamsid":17,20},
    {"slotid":6,"teamsid":17,22},
    {"slotid":49,"teamsid":0,1},
    {"slotid":2,"teamsid":18,21},
    {"slotid":34,"teamsid":18,22},
    {"slotid":41,"teamsid":19,21},
    {"slotid":16,"teamsid":19,22},
    {"slotid":45,"teamsid":20,21},
    {"slotid":21,"teamsid":20,22},
    {"slotid":9,"teamsid":23,27},
    {"slotid":46,"teamsid":23,30},
    {"slotid":52,"teamsid":23,31},
    {"slotid":29,"teamsid":23,33},
    {"slotid":35,"teamsid":24,28},
    {"slotid":69,"teamsid":24,29},
    {"slotid":12,"teamsid":24,32},
    {"slotid":10,"teamsid":24,34},
    {"slotid":37,"teamsid":25,27},
    {"slotid":15,"teamsid":25,28},
    {"slotid":17,"teamsid":1,5},
    {"slotid":1,"teamsid":25,33},
    {"slotid":32,"teamsid":25,34},
    {"slotid":62,"teamsid":26,28},
    {"slotid":47,"teamsid":26,29},
    {"slotid":25,"teamsid":26,31},
    {"slotid":39,"teamsid":26,33},
    {"slotid":61,"teamsid":27,30},
    {"slotid":63,"teamsid":1,6},
    {"slotid":60,"teamsid":27,32},
    {"slotid":8,"teamsid":28,30},
    {"slotid":53,"teamsid":1,7},
    {"slotid":28,"teamsid":29,32},
    {"slotid":44,"teamsid":29,33},
    {"slotid":38,"teamsid":30,31},
    {"slotid":43,"teamsid":2,3},
    {"slotid":18,"teamsid":31,34},
    {"slotid":0,"teamsid":2,4}]
'''
