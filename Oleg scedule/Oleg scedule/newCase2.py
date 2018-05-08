from pylinprogmaster import linprog
import numpy as np
import random

debug = True
epsilon = 0.01
max_shift_time = 12.0
class Time:
    day = ""
    start = 0
    end = 0
    def __init__(self, day,start,end):
        self.day = day
        self.start = start
        self.end = end
        
class Employee:
    id = 0
    name = ""
    availability = [[]]
    jobs = []
    max_day = [24,24,24,24,24,24,24]
    max_week = 80
    def __init__(self, id, name, availability, jobs):
        self.id = id
        self.name = name
        self.availability = availability
        self.jobs = jobs

class Shift:
    id = 0
    time = Time("",0,0)
    job_id = 0
    number_employees_needed = 1
    def __init__(self,id, time, job_id):
        self.id = id
        self.time = time
        self.job_id = job_id
        self.number_employees_needed = 1

days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

employees = [
	Employee(
		1, #employee_id
		"Ivan Drago",
		# can be available at this time period
		[
			Time("Sun", 0, 3), 
			Time("Thu", 12, 20)			
		],
		[1,2] #job_ids
	),
	Employee(
		2, #employee_id
		"Superman",
		# can be available at this time period
		[
			Time("Tue", 8, 11),
			Time("Tue", 11, 21),
			Time("Wed", 12, 14),
			Time("Wed", 16, 20)			
		],
		[3,4] #job_ids
	),
	Employee(
		3, #employee_id
		"Batman",
		# can be available at this time period
		[
			Time("Mon", 6, 9),
			Time("Mon", 13, 19),
			Time("Thu", 12, 14),
			Time("Thu", 16, 24)			
		],
		[1,2,3,7] #job_ids
	),
]

shifts = [
	#shift_id - time period from to - job_id				expected							real
	Shift(1, Time("Sun", 0, 2), 1),    #result - shift1   Ivan Drago							success
	Shift(2, Time("Sun", 4, 6), 2),    #result - shift2	  empty									success
	Shift(3, Time("Sun", 8, 12), 3),   #result - shift3   empty									success
	
	Shift(4, Time("Mon", 8, 10), 2),   #result - shift4   empty									success
	Shift(5, Time("Mon", 12, 20), 3),  #result - shift5   empty									success
	Shift(6, Time("Mon", 0, 24), 5),   #result - shift6   empty									success
	
	Shift(7, Time("Tue", 8, 10), 2),   #result - shift7   empty									success
	Shift(8, Time("Tue", 11, 20), 3),  #result - shift8   Superman 								success
	Shift(9, Time("Tue", 0, 24), 3),   #result - shift9   empty									success
	
	Shift(10, Time("Wed", 17, 18), 4), #result - shift10  Superman								success
	Shift(11, Time("Wed", 12, 20), 3), #result - shift11  empty									success
	Shift(12, Time("Wed", 20, 22), 1), #result - shift12  empty									success
	
	Shift(13, Time("Thu", 12, 20), 1), #result - shift13  Ivan Drago                      		success
	Shift(14, Time("Thu", 16, 18), 2), #result - shift14  Batman								success
	Shift(15, Time("Thu", 20, 24), 3), #result - shift15  Batman								success
	
	
	
]

number_of_employees = len(employees)
number_of_shifts = len(shifts)

def collision(x,y):
    if(x.day != y.day):
        return(False)
    if(x.end <= y.start):
        return(False)
    if(x.start >= y.end):
        return(False)
    return(True)

def in_time(x,y):  # check if x is in y
    if(x.day != y.day):
        return(False)
    if(x.start < y.start):
        return(False)
    if(x.end > y.end):
        return(False)
    return(True)

def could_do_this_job(s,e): #shift,start time,employee
    if(s.job_id not in e.jobs):
        return(False)
    for t in e.availability:
        if in_time(s.time, t):
            return(True)
    return(False)

def total_time(t):
    res = t.end - t.start
    return res

def get_index(employee,shift,number_of_shifts):
    return(employee*number_of_shifts+shift)

#Ax<=b,max <c,x>
A = []
b = []  
c = []
eq_left = []
eq_right = []

number_variables = number_of_shifts * number_of_employees 
# variables are : 0 - shifts-1 those for employee1, and so on.  to get xij, do
# i * number_of_shifts)+j

#each employee is able to work in a single shift only one time
for i in range(number_variables):
    new_line = np.zeros(number_variables)
    new_line[i] = 1
    A.append(new_line)
    b.append(1)

#shifts constraints:
shift_num = -1
for s in range(number_of_shifts):
    shift_num += 1
    new_line = np.zeros(number_variables)
    for e in range(number_of_employees):
        if(could_do_this_job(shifts[s], employees[e])):  # the employee can do it?
            new_line[get_index(e,s,number_of_shifts)] = 1 # he is only one employee

        else:  # should kill this variable: (so adding the constaint of xij==0
            nl = np.zeros(number_variables)
            nl[get_index(e,s,number_of_shifts)] = 1
            eq_left.append(nl)
            eq_right.append(0)
    A.append(new_line)
    b.append(shifts[s].number_employees_needed)

#week constraints:
for e in range(number_of_employees):
    new_line = np.zeros(number_variables)
    for s in range(number_of_shifts):
        new_line[get_index(e,s,number_of_shifts)] = total_time(shifts[s].time)  # the length of this shift
    A.append(new_line)
    b.append(employees[e].max_week)

#day constraints:
for e in range(number_of_employees):
    for d in range(len(days)):
        new_line = np.zeros(number_variables)
        for s in range(number_of_shifts):
            if(shifts[s].time.day == days[d]):
                new_line[get_index(e,s,number_of_shifts)] = total_time(shifts[s].time)
        A.append(new_line)
        b.append(employees[e].max_day[d])

#check that each employee is only in one place at a time
for s1 in range(number_of_shifts):
    l_collisions = []
    for s2 in range(number_of_shifts):
        if(s1 >= s2):
            continue
        if(collision(shifts[s1].time, shifts[s2].time)):
            l_collisions.append(s2)
    for e in range(number_of_employees):
        new_line = np.zeros(number_variables)
        new_line[get_index(e,s1,number_of_shifts)] = 1
        for s2 in l_collisions:
            new_line[get_index(e,s2,number_of_shifts)] = 1
        A.append(new_line)
        b.append(1)

if(debug):
    for row in range(len(A)):
        output = str(A[row]) + "<=" + str(b[row])
        print(output)

c = np.zeros(number_variables)
for e in range(number_of_employees):
    for s in range(number_of_shifts):
        bonus = np.random.uniform(0,epsilon)
        c[get_index(e,s,number_of_shifts)] = - 1 - bonus

resolution,sol = linprog.linsolve(c,A,b,eq_left,eq_right,range(number_variables))

if(debug): print(sol)

if resolution != "solved":
    print(resolution)
else:
    for s in range(number_of_shifts):
        l = []
        print('shift' + str(shifts[s].id))
        for e in range(number_of_employees):
            if sol[get_index(e,s,number_of_shifts)] > 1 - 1/max_shift_time:
                l.append(employees[e])
            output = "No employee meet shifts requirements"
            if l:
                output = ""
            for e in l:
                output += str(e.name) + "," 
        print("employees: " + output)
