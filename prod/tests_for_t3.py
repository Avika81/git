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
	[{"slotid":0,"teamsid":11,12},
	{"slotid":2,"teamsid":10,13},
	{"slotid":3,"teamsid":27,31},
	{"slotid":4,"teamsid":25,29},
	{"slotid":5,"teamsid":24,30},
	{"slotid":6,"teamsid":28,33},
	{"slotid":7,"teamsid":4,5},
	{"slotid":8,"teamsid":0,2},
	{"slotid":9,"teamsid":16,17},
	{"slotid":10,"teamsid":23,34},
	{"slotid":11,"teamsid":21,22},
	{"slotid":12,"teamsid":30,32},
	{"slotid":13,"teamsid":24,26},
	{"slotid":14,"teamsid":11,14},
	{"slotid":15,"teamsid":29,31},
	{"slotid":16,"teamsid":9,15},
	{"slotid":17,"teamsid":18,19},
	{"slotid":18,"teamsid":8,13},
	{"slotid":19,"teamsid":25,27},
	{"slotid":20,"teamsid":8,12},
	{"slotid":21,"teamsid":20,22},
	{"slotid":22,"teamsid":17,18},
	{"slotid":23,"teamsid":3,6},
	{"slotid":24,"teamsid":23,30},
	{"slotid":25,"teamsid":2,7},
	{"slotid":26,"teamsid":1,4},
	{"slotid":27,"teamsid":9,11},
	{"slotid":28,"teamsid":8,14},
	{"slotid":29,"teamsid":17,19},
	{"slotid":30,"teamsid":26,32},
	{"slotid":31,"teamsid":5,7},
	{"slotid":32,"teamsid":3,4},
	{"slotid":33,"teamsid":1,2},
	{"slotid":34,"teamsid":16,20},
	{"slotid":35,"teamsid":20,21},
	{"slotid":36,"teamsid":27,30},
	{"slotid":37,"teamsid":23,24},
	{"slotid":38,"teamsid":3,7},
	{"slotid":39,"teamsid":18,22},
	{"slotid":40,"teamsid":28,31},
	{"slotid":41,"teamsid":32,33}]
	{"slotid":42,"teamsid":25,34},
	{"slotid":43,"teamsid":14,15},
	{"slotid":44,"teamsid":9,13},
	{"slotid":45,"teamsid":10,12},
	{"slotid":46,"teamsid":8,11},
	{"slotid":47,"teamsid":0,1},
	{"slotid":48,"teamsid":28,29},
	{"slotid":49,"teamsid":33,34},
	{"slotid":50,"teamsid":16,18},
	{"slotid":51,"teamsid":19,21},
	{"slotid":52,"teamsid":2,6},
	{"slotid":53,"teamsid":17,22},
	{"slotid":54,"teamsid":0,4},
	{"slotid":55,"teamsid":10,15},
	{"slotid":56,"teamsid":27,28},
	{"slotid":57,"teamsid":24,34},
	{"slotid":58,"teamsid":26,31},
	{"slotid":59,"teamsid":5,6},
	{"slotid":60,"teamsid":0,3},
	{"slotid":61,"teamsid":12,15},
	{"slotid":62,"teamsid":1,5},
	{"slotid":63,"teamsid":9,10},
	{"slotid":64,"teamsid":23,32},
	{"slotid":65,"teamsid":16,21},
	{"slotid":66,"teamsid":6,7},
	{"slotid":67,"teamsid":25,26},
	{"slotid":68,"teamsid":13,14},
	{"slotid":69,"teamsid":29,33},
	{"slotid":70,"teamsid":19,20},
'''

example_7 = '{"slots":[{"id":0,"start":1,"end":2},{"id":1,"start":1,"end":2},{"id":2,"start":1,"end":2},{"id":3,"start":2,"end":3},{"id":4,"start":2,"end":3},{"id":5,"start":2,"end":3},{"id":6,"start":3,"end":4},{"id":7,"start":3,"end":4},{"id":8,"start":3,"end":4},{"id":9,"start":4,"end":5},{"id":10,"start":4,"end":5},{"id":11,"start":4,"end":5},{"id":12,"start":25,"end":26},{"id":13,"start":26,"end":27},{"id":14,"start":27,"end":28},{"id":15,"start":28,"end":29},{"id":16,"start":29,"end":30},{"id":17,"start":30,"end":31},{"id":18,"start":31,"end":32},{"id":19,"start":49,"end":50},{"id":20,"start":50,"end":51},{"id":21,"start":51,"end":52},{"id":22,"start":52,"end":53},{"id":23,"start":53,"end":54},{"id":24,"start":54,"end":55},{"id":25,"start":55,"end":56},{"id":26,"start":73,"end":74},{"id":27,"start":74,"end":75},{"id":28,"start":75,"end":76},{"id":29,"start":76,"end":77},{"id":30,"start":77,"end":78},{"id":31,"start":97,"end":98},{"id":32,"start":98,"end":99},{"id":33,"start":99,"end":100},{"id":34,"start":100,"end":101},{"id":35,"start":169,"end":170},{"id":36,"start":169,"end":170},{"id":37,"start":170,"end":171},{"id":38,"start":170,"end":171},{"id":39,"start":171,"end":172},{"id":40,"start":171,"end":172},{"id":41,"start":172,"end":173},{"id":42,"start":172,"end":173},{"id":43,"start":173,"end":174},{"id":44,"start":173,"end":174},{"id":45,"start":174,"end":175},{"id":46,"start":174,"end":175},{"id":47,"start":175,"end":176},{"id":48,"start":193,"end":194},{"id":49,"start":194,"end":195},{"id":50,"start":195,"end":196},{"id":51,"start":196,"end":197},{"id":52,"start":197,"end":198},{"id":53,"start":198,"end":199},{"id":54,"start":199,"end":200},{"id":55,"start":200,"end":201},{"id":56,"start":217,"end":218},{"id":57,"start":218,"end":219},{"id":58,"start":219,"end":220},{"id":59,"start":220,"end":221},{"id":60,"start":221,"end":222},{"id":61,"start":241,"end":242},{"id":62,"start":242,"end":243},{"id":63,"start":243,"end":244},{"id":64,"start":244,"end":245},{"id":65,"start":245,"end":246},{"id":66,"start":265,"end":266},{"id":67,"start":266,"end":267},{"id":68,"start":267,"end":268},{"id":69,"start":268,"end":269},{"id":70,"start":269,"end":270},{"id":100,"start":1001,"end":1002},{"id":101,"start":1001,"end":1002},{"id":102,"start":1001,"end":1002},{"id":103,"start":1002,"end":1003},{"id":104,"start":1002,"end":1003},{"id":105,"start":1002,"end":1003},{"id":106,"start":1003,"end":1004},{"id":107,"start":1003,"end":1004},{"id":108,"start":1003,"end":1004},{"id":109,"start":1004,"end":1005},{"id":110,"start":1004,"end":1005},{"id":111,"start":1004,"end":1005},{"id":112,"start":1025,"end":1026},{"id":113,"start":1026,"end":1027},{"id":114,"start":1027,"end":1028},{"id":115,"start":1028,"end":1029},{"id":116,"start":1029,"end":1030},{"id":117,"start":1030,"end":1031},{"id":118,"start":1031,"end":1032},{"id":119,"start":1049,"end":1050},{"id":120,"start":1050,"end":1051},{"id":121,"start":1051,"end":1052},{"id":122,"start":1052,"end":1053},{"id":123,"start":1053,"end":1054},{"id":124,"start":1054,"end":1055},{"id":125,"start":1055,"end":1056},{"id":126,"start":1073,"end":1074},{"id":127,"start":1074,"end":1075},{"id":128,"start":1075,"end":1076},{"id":129,"start":1076,"end":1077},{"id":130,"start":1077,"end":1078},{"id":131,"start":1097,"end":1098},{"id":132,"start":1098,"end":1099},{"id":133,"start":1099,"end":10100},{"id":134,"start":1100,"end":1101},{"id":135,"start":1169,"end":1170},{"id":136,"start":1169,"end":1170},{"id":137,"start":1170,"end":1171},{"id":138,"start":1170,"end":1171},{"id":139,"start":1171,"end":1172},{"id":140,"start":1171,"end":1172},{"id":141,"start":1172,"end":1173},{"id":142,"start":1172,"end":1173},{"id":143,"start":1173,"end":1174},{"id":144,"start":1173,"end":1174},{"id":145,"start":1174,"end":1175},{"id":146,"start":1174,"end":1175},{"id":147,"start":1175,"end":1176},{"id":148,"start":1193,"end":1194},{"id":149,"start":1194,"end":1195},{"id":150,"start":1195,"end":1196},{"id":151,"start":1196,"end":1197},{"id":152,"start":1197,"end":1198},{"id":153,"start":1198,"end":1199},{"id":154,"start":1199,"end":1200},{"id":155,"start":1200,"end":1201},{"id":156,"start":1217,"end":1218},{"id":157,"start":1218,"end":1219},{"id":158,"start":1219,"end":1220},{"id":159,"start":1220,"end":1221},{"id":160,"start":1221,"end":1222},{"id":161,"start":1241,"end":1242},{"id":162,"start":1242,"end":1243},{"id":163,"start":1243,"end":1244},{"id":164,"start":1244,"end":1245},{"id":165,"start":1245,"end":1246},{"id":166,"start":1265,"end":1266},{"id":167,"start":1266,"end":1267},{"id":168,"start":1267,"end":1268},{"id":169,"start":1268,"end":1269},{"id":170,"start":1269,"end":1270},{"id":262,"start":2242,"end":2243},{"id":263,"start":2243,"end":2244},{"id":264,"start":2244,"end":2245},{"id":265,"start":2245,"end":2246},{"id":266,"start":2265,"end":2266},{"id":267,"start":2266,"end":2267},{"id":268,"start":2267,"end":2268},{"id":269,"start":2268,"end":2269},{"id":270,"start":2269,"end":2270},{"id":270,"start":2270,"end":2271}],"events":[{"id":1,"is_coed":false},{"id":2,"is_coed":true},{"id":3,"is_coed":false},{"id":4,"is_coed":true},{"id":5,"is_coed":false}],"teams":[{"team_id":0,"event_id":1,"num_of_games_to_schedule":4},{"team_id":1,"event_id":1,"num_of_games_to_schedule":4},{"team_id":2,"event_id":1,"num_of_games_to_schedule":4},{"team_id":3,"event_id":1,"num_of_games_to_schedule":4},{"team_id":4,"event_id":1,"num_of_games_to_schedule":4},{"team_id":5,"event_id":1,"num_of_games_to_schedule":4},{"team_id":6,"event_id":1,"num_of_games_to_schedule":4},{"team_id":7,"event_id":1,"num_of_games_to_schedule":4},{"team_id":8,"event_id":2,"num_of_games_to_schedule":4},{"team_id":9,"event_id":2,"num_of_games_to_schedule":4},{"team_id":10,"event_id":2,"num_of_games_to_schedule":4},{"team_id":11,"event_id":2,"num_of_games_to_schedule":4},{"team_id":12,"event_id":2,"num_of_games_to_schedule":4},{"team_id":13,"event_id":2,"num_of_games_to_schedule":4},{"team_id":14,"event_id":2,"num_of_games_to_schedule":4},{"team_id":15,"event_id":2,"num_of_games_to_schedule":4},{"team_id":16,"event_id":3,"num_of_games_to_schedule":4},{"team_id":17,"event_id":3,"num_of_games_to_schedule":4},{"team_id":18,"event_id":3,"num_of_games_to_schedule":4},{"team_id":19,"event_id":3,"num_of_games_to_schedule":4},{"team_id":20,"event_id":3,"num_of_games_to_schedule":4},{"team_id":21,"event_id":3,"num_of_games_to_schedule":4},{"team_id":22,"event_id":3,"num_of_games_to_schedule":4},{"team_id":23,"event_id":4,"num_of_games_to_schedule":4},{"team_id":24,"event_id":4,"num_of_games_to_schedule":4},{"team_id":25,"event_id":4,"num_of_games_to_schedule":4},{"team_id":26,"event_id":4,"num_of_games_to_schedule":4},{"team_id":27,"event_id":4,"num_of_games_to_schedule":4},{"team_id":28,"event_id":4,"num_of_games_to_schedule":4},{"team_id":29,"event_id":4,"num_of_games_to_schedule":4},{"team_id":30,"event_id":4,"num_of_games_to_schedule":4},{"team_id":31,"event_id":4,"num_of_games_to_schedule":4},{"team_id":32,"event_id":4,"num_of_games_to_schedule":4},{"team_id":33,"event_id":4,"num_of_games_to_schedule":4},{"team_id":34,"event_id":4,"num_of_games_to_schedule":4},{"team_id":35,"event_id":1,"num_of_games_to_schedule":5},{"team_id":36,"event_id":1,"num_of_games_to_schedule":5},{"team_id":37,"event_id":1,"num_of_games_to_schedule":5},{"team_id":38,"event_id":1,"num_of_games_to_schedule":5},{"team_id":39,"event_id":1,"num_of_games_to_schedule":5},{"team_id":40,"event_id":1,"num_of_games_to_schedule":5},{"team_id":41,"event_id":1,"num_of_games_to_schedule":5},{"team_id":42,"event_id":1,"num_of_games_to_schedule":5},{"team_id":43,"event_id":2,"num_of_games_to_schedule":5},{"team_id":44,"event_id":2,"num_of_games_to_schedule":5},{"team_id":45,"event_id":2,"num_of_games_to_schedule":5},{"team_id":46,"event_id":2,"num_of_games_to_schedule":5},{"team_id":47,"event_id":2,"num_of_games_to_schedule":5},{"team_id":48,"event_id":2,"num_of_games_to_schedule":5},{"team_id":49,"event_id":2,"num_of_games_to_schedule":5},{"team_id":50,"event_id":2,"num_of_games_to_schedule":5},{"team_id":51,"event_id":3,"num_of_games_to_schedule":5},{"team_id":52,"event_id":3,"num_of_games_to_schedule":5},{"team_id":53,"event_id":3,"num_of_games_to_schedule":5},{"team_id":54,"event_id":3,"num_of_games_to_schedule":5},{"team_id":55,"event_id":3,"num_of_games_to_schedule":5},{"team_id":56,"event_id":3,"num_of_games_to_schedule":5},{"team_id":57,"event_id":3,"num_of_games_to_schedule":5},{"team_id":58,"event_id":5,"num_of_games_to_schedule":5},{"team_id":59,"event_id":5,"num_of_games_to_schedule":5},{"team_id":60,"event_id":5,"num_of_games_to_schedule":5},{"team_id":61,"event_id":5,"num_of_games_to_schedule":5},{"team_id":62,"event_id":5,"num_of_games_to_schedule":5},{"team_id":63,"event_id":5,"num_of_games_to_schedule":5},{"team_id":64,"event_id":5,"num_of_games_to_schedule":5},{"team_id":65,"event_id":5,"num_of_games_to_schedule":5},{"team_id":66,"event_id":5,"num_of_games_to_schedule":5}]}'

example_8 ='{"events":[{"id":1,"event_start":"2018-09-03","games_per_team":4,"required_slots":10,"is_coed":false}],"teams":[{"team_id":2,"event_id":1,"num_of_games_to_schedule":4},{"team_id":3,"event_id":1,"num_of_games_to_schedule":4},{"team_id":4,"event_id":1,"num_of_games_to_schedule":4},{"team_id":5,"event_id":1,"num_of_games_to_schedule":4},{"team_id":6,"event_id":1,"num_of_games_to_schedule":4}],"slots":[{"id":1,"start":20,"end":21,"unavailable_entries":[]},{"id":2,"start":21,"end":22,"unavailable_entries":[]},{"id":3,"start":22,"end":23,"unavailable_entries":[]},{"id":4,"start":188,"end":189,"unavailable_entries":[]},{"id":5,"start":189,"end":190,"unavailable_entries":[]},{"id":6,"start":190,"end":191,"unavailable_entries":[]},{"id":7,"start":356,"end":357,"unavailable_entries":[]},{"id":8,"start":357,"end":358,"unavailable_entries":[]},{"id":9,"start":358,"end":359,"unavailable_entries":[]},{"id":10,"start":524,"end":525,"unavailable_entries":[]},{"id":11,"start":525,"end":526,"unavailable_entries":[]},{"id":12,"start":526,"end":527,"unavailable_entries":[]},{"id":13,"start":692,"end":693,"unavailable_entries":[]},{"id":14,"start":693,"end":694,"unavailable_entries":[]},{"id":15,"start":694,"end":695,"unavailable_entries":[]}]}'


example_not_working = '{"events":[{"id":1,"event_start":"2018-09-02","games_per_team":2,"required_slots":3,"is_coed":false},{"id":17,"event_start":"2018-09-02","games_per_team":2,"required_slots":6,"is_coed":false}],"teams":[{"team_id":17,"event_id":1,"num_of_games_to_schedule":2},{"team_id":19,"event_id":1,"num_of_games_to_schedule":2},{"team_id":20,"event_id":1,"num_of_games_to_schedule":2},{"team_id":48,"event_id":17,"num_of_games_to_schedule":2},{"team_id":49,"event_id":17,"num_of_games_to_schedule":2},{"team_id":50,"event_id":17,"num_of_games_to_schedule":2},{"team_id":51,"event_id":17,"num_of_games_to_schedule":2},{"team_id":53,"event_id":17,"num_of_games_to_schedule":2},{"team_id":54,"event_id":17,"num_of_games_to_schedule":2}],"slots":[{"id":1,"start":20,"end":21,"unavailable_entries":[]},{"id":2,"start":20,"end":21,"unavailable_entries":[]},{"id":3,"start":20,"end":21,"unavailable_entries":[]},{"id":4,"start":21,"end":22,"unavailable_entries":[]},{"id":5,"start":21,"end":22,"unavailable_entries":[]},{"id":6,"start":21,"end":22,"unavailable_entries":[]},{"id":7,"start":22,"end":23,"unavailable_entries":[]},{"id":8,"start":22,"end":23,"unavailable_entries":[]},{"id":9,"start":22,"end":23,"unavailable_entries":[]}]}'

example_9 = '{"events":[{"id":1,"event_start":"2018-09-03","games_per_team":3,"required_slots":8,"is_coed":false},{"id":2,"event_start":"2018-09-03","games_per_team":3,"required_slots":5,"is_coed":false}],"teams":[{"team_id":2,"event_id":1,"num_of_games_to_schedule":3},{"team_id":3,"event_id":1,"num_of_games_to_schedule":3},{"team_id":4,"event_id":1,"num_of_games_to_schedule":3},{"team_id":5,"event_id":1,"num_of_games_to_schedule":10},{"team_id":6,"event_id":1,"num_of_games_to_schedule":3},{"team_id":7,"event_id":2,"num_of_games_to_schedule":3},{"team_id":8,"event_id":2,"num_of_games_to_schedule":3},{"team_id":9,"event_id":2,"num_of_games_to_schedule":3}],"slots":[{"id":1,"start":20,"end":21,"unavailable_entries":[]},{"id":2,"start":21,"end":22,"unavailable_entries":[]},{"id":3,"start":22,"end":23,"unavailable_entries":[]},{"id":4,"start":188,"end":189,"unavailable_entries":[]},{"id":5,"start":189,"end":190,"unavailable_entries":[]},{"id":6,"start":190,"end":191,"unavailable_entries":[]},{"id":7,"start":356,"end":357,"unavailable_entries":[]},{"id":8,"start":357,"end":358,"unavailable_entries":[]},{"id":9,"start":358,"end":359,"unavailable_entries":[]},{"id":12,"start":526,"end":527,"unavailable_entries":[]},{"id":11,"start":525,"end":526,"unavailable_entries":[]},{"id":10,"start":524,"end":525,"unavailable_entries":[]},{"id":13,"start":692,"end":693,"unavailable_entries":[]},{"id":14,"start":693,"end":694,"unavailable_entries":[]},{"id":15,"start":694,"end":695,"unavailable_entries":[]},{"id":16,"start":860,"end":861,"unavailable_entries":[]},{"id":17,"start":861,"end":862,"unavailable_entries":[]},{"id":18,"start":862,"end":863,"unavailable_entries":[]},{"id":19,"start":1028,"end":1029,"unavailable_entries":[]},{"id":20,"start":1029,"end":1030,"unavailable_entries":[]},{"id":21,"start":1030,"end":1031,"unavailable_entries":[]}]}'

example_10 = '{"events":[{"id":8,"event_start":"2018-09-11","games_per_team":2,"required_slots":5,"is_coed":true}],"teams":[{"team_id":62,"event_id":8,"num_of_games_to_schedule":2},{"team_id":63,"event_id":8,"num_of_games_to_schedule":2},{"team_id":64,"event_id":8,"num_of_games_to_schedule":2},{"team_id":65,"event_id":8,"num_of_games_to_schedule":2},{"team_id":66,"event_id":8,"num_of_games_to_schedule":2}],"slots":[{"id":1,"start":14,"end":15,"unavailable_entries":[63,64,65]},{"id":2,"start":14,"end":15,"unavailable_entries":[63,64,65]},{"id":3,"start":182,"end":183,"unavailable_entries":[63,64,65]},{"id":4,"start":182,"end":183,"unavailable_entries":[63,64,65]},{"id":5,"start":350,"end":351,"unavailable_entries":[63,64,65]},{"id":6,"start":350,"end":351,"unavailable_entries":[63,64,65]}]}'

example_11 = '{"events":[{"id":22,"event_start":"2018-09-11","games_per_team":2,"required_slots":4,"is_coed":false}],"teams":[{"team_id":119,"event_id":22,"num_of_games_to_schedule":2},{"team_id":120,"event_id":22,"num_of_games_to_schedule":2},{"team_id":121,"event_id":22,"num_of_games_to_schedule":2},{"team_id":122,"event_id":22,"num_of_games_to_schedule":2}],"slots":[{"id":1,"start":8,"end":8.5,"unavailable_entries":[]},{"id":17,"start":16,"end":16.5,"unavailable_entries":[]},{"id":29,"start":22,"end":22.5,"unavailable_entries":[]},{"id":28,"start":21.5,"end":22,"unavailable_entries":[]},{"id":27,"start":21,"end":21.5,"unavailable_entries":[]},{"id":26,"start":20.5,"end":21,"unavailable_entries":[]},{"id":25,"start":20,"end":20.5,"unavailable_entries":[]},{"id":24,"start":19.5,"end":20,"unavailable_entries":[]},{"id":23,"start":19,"end":19.5,"unavailable_entries":[]},{"id":22,"start":18.5,"end":19,"unavailable_entries":[]},{"id":21,"start":18,"end":18.5,"unavailable_entries":[]},{"id":20,"start":17.5,"end":18,"unavailable_entries":[]},{"id":19,"start":17,"end":17.5,"unavailable_entries":[]},{"id":18,"start":16.5,"end":17,"unavailable_entries":[]},{"id":16,"start":15.5,"end":16,"unavailable_entries":[]},{"id":2,"start":8.5,"end":9,"unavailable_entries":[]},{"id":15,"start":15,"end":15.5,"unavailable_entries":[]},{"id":14,"start":14.5,"end":15,"unavailable_entries":[]},{"id":13,"start":14,"end":14.5,"unavailable_entries":[]},{"id":12,"start":13.5,"end":14,"unavailable_entries":[]},{"id":11,"start":13,"end":13.5,"unavailable_entries":[]},{"id":10,"start":12.5,"end":13,"unavailable_entries":[]},{"id":9,"start":12,"end":12.5,"unavailable_entries":[]},{"id":8,"start":11.5,"end":12,"unavailable_entries":[]},{"id":7,"start":11,"end":11.5,"unavailable_entries":[]},{"id":6,"start":10.5,"end":11,"unavailable_entries":[]},{"id":5,"start":10,"end":10.5,"unavailable_entries":[]},{"id":4,"start":9.5,"end":10,"unavailable_entries":[]},{"id":3,"start":9,"end":9.5,"unavailable_entries":[]},{"id":30,"start":22.5,"end":23,"unavailable_entries":[]}]}'

example_biggg = '{"events":[{"id":7,"event_start":"2018-09-12","games_per_team":8,"required_slots":140,"is_coed":true}],"teams":[{"team_id":27,"event_id":7,"num_of_games_to_schedule":8},{"team_id":28,"event_id":7,"num_of_games_to_schedule":8},{"team_id":29,"event_id":7,"num_of_games_to_schedule":8},{"team_id":30,"event_id":7,"num_of_games_to_schedule":8},{"team_id":31,"event_id":7,"num_of_games_to_schedule":8},{"team_id":32,"event_id":7,"num_of_games_to_schedule":8},{"team_id":33,"event_id":7,"num_of_games_to_schedule":8},{"team_id":34,"event_id":7,"num_of_games_to_schedule":8},{"team_id":35,"event_id":7,"num_of_games_to_schedule":8},{"team_id":36,"event_id":7,"num_of_games_to_schedule":8},{"team_id":37,"event_id":7,"num_of_games_to_schedule":8},{"team_id":38,"event_id":7,"num_of_games_to_schedule":8},{"team_id":39,"event_id":7,"num_of_games_to_schedule":8},{"team_id":40,"event_id":7,"num_of_games_to_schedule":8},{"team_id":41,"event_id":7,"num_of_games_to_schedule":8},{"team_id":42,"event_id":7,"num_of_games_to_schedule":8},{"team_id":43,"event_id":7,"num_of_games_to_schedule":8},{"team_id":44,"event_id":7,"num_of_games_to_schedule":8},{"team_id":45,"event_id":7,"num_of_games_to_schedule":8},{"team_id":46,"event_id":7,"num_of_games_to_schedule":8},{"team_id":47,"event_id":7,"num_of_games_to_schedule":8},{"team_id":48,"event_id":7,"num_of_games_to_schedule":8},{"team_id":49,"event_id":7,"num_of_games_to_schedule":8},{"team_id":50,"event_id":7,"num_of_games_to_schedule":8},{"team_id":51,"event_id":7,"num_of_games_to_schedule":8},{"team_id":52,"event_id":7,"num_of_games_to_schedule":8},{"team_id":53,"event_id":7,"num_of_games_to_schedule":8},{"team_id":54,"event_id":7,"num_of_games_to_schedule":8},{"team_id":55,"event_id":7,"num_of_games_to_schedule":8},{"team_id":56,"event_id":7,"num_of_games_to_schedule":8},{"team_id":57,"event_id":7,"num_of_games_to_schedule":8},{"team_id":58,"event_id":7,"num_of_games_to_schedule":8},{"team_id":59,"event_id":7,"num_of_games_to_schedule":8},{"team_id":60,"event_id":7,"num_of_games_to_schedule":8},{"team_id":61,"event_id":7,"num_of_games_to_schedule":8}],"slots":[{"id":1,"start":18,"end":19,"unavailable_entries":[]},{"id":137,"start":17,"end":18,"unavailable_entries":[]},{"id":38,"start":20,"end":21,"unavailable_entries":[]},{"id":39,"start":21,"end":22,"unavailable_entries":[]},{"id":40,"start":22,"end":23,"unavailable_entries":[]},{"id":36,"start":18,"end":19,"unavailable_entries":[]},{"id":136,"start":16,"end":17,"unavailable_entries":[]},{"id":2,"start":19,"end":20,"unavailable_entries":[]},{"id":37,"start":19,"end":20,"unavailable_entries":[]},{"id":3,"start":20,"end":21,"unavailable_entries":[]},{"id":4,"start":21,"end":22,"unavailable_entries":[]},{"id":5,"start":22,"end":23,"unavailable_entries":[]},{"id":10,"start":46,"end":47,"unavailable_entries":[]},{"id":41,"start":42,"end":43,"unavailable_entries":[]},{"id":42,"start":43,"end":44,"unavailable_entries":[]},{"id":43,"start":44,"end":45,"unavailable_entries":[]},{"id":44,"start":45,"end":46,"unavailable_entries":[]},{"id":45,"start":46,"end":47,"unavailable_entries":[]},{"id":9,"start":45,"end":46,"unavailable_entries":[]},{"id":6,"start":42,"end":43,"unavailable_entries":[]},{"id":7,"start":43,"end":44,"unavailable_entries":[]},{"id":8,"start":44,"end":45,"unavailable_entries":[]},{"id":138,"start":40,"end":41,"unavailable_entries":[]},{"id":139,"start":41,"end":42,"unavailable_entries":[]},{"id":48,"start":68,"end":69,"unavailable_entries":[]},{"id":46,"start":66,"end":67,"unavailable_entries":[]},{"id":49,"start":69,"end":70,"unavailable_entries":[]},{"id":50,"start":70,"end":71,"unavailable_entries":[]},{"id":140,"start":64,"end":65,"unavailable_entries":[]},{"id":47,"start":67,"end":68,"unavailable_entries":[]},{"id":141,"start":65,"end":66,"unavailable_entries":[]},{"id":15,"start":70,"end":71,"unavailable_entries":[]},{"id":14,"start":69,"end":70,"unavailable_entries":[]},{"id":13,"start":68,"end":69,"unavailable_entries":[]},{"id":12,"start":67,"end":68,"unavailable_entries":[]},{"id":11,"start":66,"end":67,"unavailable_entries":[]},{"id":20,"start":94,"end":95,"unavailable_entries":[]},{"id":16,"start":90,"end":91,"unavailable_entries":[]},{"id":55,"start":94,"end":95,"unavailable_entries":[]},{"id":53,"start":92,"end":93,"unavailable_entries":[]},{"id":52,"start":91,"end":92,"unavailable_entries":[]},{"id":51,"start":90,"end":91,"unavailable_entries":[]},{"id":17,"start":91,"end":92,"unavailable_entries":[]},{"id":18,"start":92,"end":93,"unavailable_entries":[]},{"id":19,"start":93,"end":94,"unavailable_entries":[]},{"id":54,"start":93,"end":94,"unavailable_entries":[]},{"id":21,"start":114,"end":115,"unavailable_entries":[]},{"id":22,"start":115,"end":116,"unavailable_entries":[]},{"id":23,"start":116,"end":117,"unavailable_entries":[]},{"id":24,"start":117,"end":118,"unavailable_entries":[]},{"id":25,"start":118,"end":119,"unavailable_entries":[]},{"id":56,"start":114,"end":115,"unavailable_entries":[]},{"id":57,"start":115,"end":116,"unavailable_entries":[]},{"id":58,"start":116,"end":117,"unavailable_entries":[]},{"id":59,"start":117,"end":118,"unavailable_entries":[]},{"id":60,"start":118,"end":119,"unavailable_entries":[]},{"id":30,"start":142,"end":143,"unavailable_entries":[]},{"id":29,"start":141,"end":142,"unavailable_entries":[]},{"id":65,"start":142,"end":143,"unavailable_entries":[]},{"id":64,"start":141,"end":142,"unavailable_entries":[]},{"id":63,"start":140,"end":141,"unavailable_entries":[]},{"id":62,"start":139,"end":140,"unavailable_entries":[]},{"id":61,"start":138,"end":139,"unavailable_entries":[]},{"id":28,"start":140,"end":141,"unavailable_entries":[]},{"id":27,"start":139,"end":140,"unavailable_entries":[]},{"id":26,"start":138,"end":139,"unavailable_entries":[]},{"id":33,"start":164,"end":165,"unavailable_entries":[]},{"id":66,"start":162,"end":163,"unavailable_entries":[]},{"id":67,"start":163,"end":164,"unavailable_entries":[]},{"id":68,"start":164,"end":165,"unavailable_entries":[]},{"id":69,"start":165,"end":166,"unavailable_entries":[]},{"id":70,"start":166,"end":167,"unavailable_entries":[]},{"id":31,"start":162,"end":163,"unavailable_entries":[]},{"id":35,"start":166,"end":167,"unavailable_entries":[]},{"id":34,"start":165,"end":166,"unavailable_entries":[]},{"id":32,"start":163,"end":164,"unavailable_entries":[]},{"id":71,"start":186,"end":187,"unavailable_entries":[]},{"id":73,"start":188,"end":189,"unavailable_entries":[]},{"id":72,"start":187,"end":188,"unavailable_entries":[]},{"id":74,"start":189,"end":190,"unavailable_entries":[]},{"id":75,"start":190,"end":191,"unavailable_entries":[]},{"id":78,"start":212,"end":213,"unavailable_entries":[]},{"id":79,"start":213,"end":214,"unavailable_entries":[]},{"id":80,"start":214,"end":215,"unavailable_entries":[]},{"id":77,"start":211,"end":212,"unavailable_entries":[]},{"id":76,"start":210,"end":211,"unavailable_entries":[]},{"id":81,"start":234,"end":235,"unavailable_entries":[]},{"id":82,"start":235,"end":236,"unavailable_entries":[]},{"id":83,"start":236,"end":237,"unavailable_entries":[]},{"id":84,"start":237,"end":238,"unavailable_entries":[]},{"id":85,"start":238,"end":239,"unavailable_entries":[]},{"id":87,"start":259,"end":260,"unavailable_entries":[]},{"id":90,"start":262,"end":263,"unavailable_entries":[]},{"id":89,"start":261,"end":262,"unavailable_entries":[]},{"id":88,"start":260,"end":261,"unavailable_entries":[]},{"id":86,"start":258,"end":259,"unavailable_entries":[]},{"id":93,"start":284,"end":285,"unavailable_entries":[]},{"id":94,"start":285,"end":286,"unavailable_entries":[]},{"id":92,"start":283,"end":284,"unavailable_entries":[]},{"id":91,"start":282,"end":283,"unavailable_entries":[]},{"id":95,"start":286,"end":287,"unavailable_entries":[]},{"id":100,"start":310,"end":311,"unavailable_entries":[]},{"id":99,"start":309,"end":310,"unavailable_entries":[]},{"id":98,"start":308,"end":309,"unavailable_entries":[]},{"id":97,"start":307,"end":308,"unavailable_entries":[]},{"id":96,"start":306,"end":307,"unavailable_entries":[]},{"id":101,"start":330,"end":331,"unavailable_entries":[]},{"id":103,"start":332,"end":333,"unavailable_entries":[]},{"id":104,"start":333,"end":334,"unavailable_entries":[]},{"id":105,"start":334,"end":335,"unavailable_entries":[]},{"id":102,"start":331,"end":332,"unavailable_entries":[]},{"id":110,"start":358,"end":359,"unavailable_entries":[]},{"id":106,"start":354,"end":355,"unavailable_entries":[]},{"id":107,"start":355,"end":356,"unavailable_entries":[]},{"id":108,"start":356,"end":357,"unavailable_entries":[]},{"id":109,"start":357,"end":358,"unavailable_entries":[]},{"id":113,"start":380,"end":381,"unavailable_entries":[]},{"id":114,"start":381,"end":382,"unavailable_entries":[]},{"id":115,"start":382,"end":383,"unavailable_entries":[]},{"id":112,"start":379,"end":380,"unavailable_entries":[]},{"id":111,"start":378,"end":379,"unavailable_entries":[]},{"id":117,"start":403,"end":404,"unavailable_entries":[]},{"id":116,"start":402,"end":403,"unavailable_entries":[]},{"id":118,"start":404,"end":405,"unavailable_entries":[]},{"id":119,"start":405,"end":406,"unavailable_entries":[]},{"id":120,"start":406,"end":407,"unavailable_entries":[]},{"id":123,"start":428,"end":429,"unavailable_entries":[]},{"id":124,"start":429,"end":430,"unavailable_entries":[]},{"id":125,"start":430,"end":431,"unavailable_entries":[]},{"id":122,"start":427,"end":428,"unavailable_entries":[]},{"id":121,"start":426,"end":427,"unavailable_entries":[]},{"id":127,"start":451,"end":452,"unavailable_entries":[]},{"id":130,"start":454,"end":455,"unavailable_entries":[]},{"id":129,"start":453,"end":454,"unavailable_entries":[]},{"id":128,"start":452,"end":453,"unavailable_entries":[]},{"id":126,"start":450,"end":451,"unavailable_entries":[]},{"id":133,"start":476,"end":477,"unavailable_entries":[]},{"id":134,"start":477,"end":478,"unavailable_entries":[]},{"id":135,"start":478,"end":479,"unavailable_entries":[]},{"id":131,"start":474,"end":475,"unavailable_entries":[]},{"id":132,"start":475,"end":476,"unavailable_entries":[]}]}'

example_simple = '{"events":[{"id":1,"event_start":"2018-09-10","games_per_team":1,"required_slots":1,"is_coed":false}],"teams":[{"team_id":1,"event_id":1,"num_of_games_to_schedule":1},{"team_id":2,"event_id":1,"num_of_games_to_schedule":1}],"slots":[{"id":1,"start":20,"end":21,"unavailable_entries":[]}]}'
