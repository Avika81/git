# from pylinprogmaster import linprog
import numpy as np
import random
import pulp

debug = False
debug2 = False
epsilon = 0.01
max_shift_time = 12.0
ideal_shift_times = [(2,2),(3,4)]

def day_to_num(day):
    if day == "Sun": return 1
    elif day == "Mon": return 2
    elif day == "Tue": return 3
    elif day == "Wed": return 4
    elif day == "Thu": return 5
    elif day == "Fri": return 6
    elif day == "Sat": return 7

class Time:
    day = ""
    start = 0
    end = 0
    def __init__(self, day,start,end):
        self.day = day
        self.start = start
        self.end = end
    def __eq__(self,other):
        if(self.day != other.day):
            return False
        return self.start == other.start
    def __lt__(self,other):
        if(self.day!=other.day):
            return day_to_num(self.day)<day_to_num(other.day)
        return self.start < other.start

class Employee:
    id = 0
    name = ""
    availability = [[]]
    jobs = []
    max_day = []
    max_week = 0
    def __init__(self, id, name, availability, jobs, max_day = [4,4,4,4,4,4,4], max_week = 20):
        self.id = id
        self.name = name
        self.availability = availability
        self.jobs = jobs
        self.max_day = max_day
        self.max_week = max_week

class Shift:
    id = 0
    time = Time("",0,0)
    job_id = 0
    number_employees_needed = 1
    priority = 1
    def __init__(self,id, time, job_id):
        self.id = id
        self.time = time
        self.job_id = job_id
        self.number_employees_needed = 1
    def __eq__(self,other):
        return self.time == other.time
    def __lt__(self,other):
        return self.time < other.time

days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

employees = [Employee(1,"Bill",
[Time("Sun",14,24),
Time("Mon",15,24),
Time("Tue",16.5,24),
Time("Wed",3,24),
Time("Thu",16.5,24),
Time("Fri",13,24),
Time("Sat",10,24)],
[1,2,3,4]),

Employee(2,"Jenny",
[Time("Sun",8.5,24),
Time("Mon",12,24),
Time("Tue",12,24),
Time("Wed",12,18),
Time("Wed",21,24),
Time("Thu",12,24),
Time("Fri",12,24),
Time("Sat",8.5,24)],
[1,2,3,4]),

Employee(3,"Tom",
[Time("Sun",12,24),
Time("Mon",15,24),
Time("Tue",15,24),
Time("Wed",15,24),
Time("Thu",15,24),
Time("Fri",13,18)],
[1,2,3,4]),

Employee(4,"Amy",
[Time("Sun",14,24),
Time("Mon",15,24),
Time("Tue",16.5,24),
Time("Wed",15,18),
Time("Thu",16.5,24),
Time("Fri",13,24),
Time("Sat",10,24)],
[1,2,3,4])
]
""" test 1: BB """
shifts = [ 
Shift(0,Time("Sun",12,13),1),
Shift(1,Time("Sun",13,14),1),
Shift(2,Time("Sun",14,15),1),
Shift(3,Time("Sun",15,16),1),
Shift(4,Time("Sun",16,17),1),
Shift(5,Time("Sun",17,18),1),
Shift(6,Time("Sun",18,19),1), #same is easy here **
Shift(7,Time("Sun",19,20),1),
Shift(8,Time("Sun",20,21),1),

Shift(9,Time("Mon",18,19),1),
Shift(10,Time("Mon",19,20),1),
Shift(11,Time("Mon",20,21),1),
Shift(12,Time("Mon",21,22),1),
Shift(13,Time("Mon",22,23),1),

Shift(14,Time("Tue",18,19),1),
Shift(15,Time("Tue",19,20),1),
Shift(16,Time("Tue",20,21),1),
Shift(17,Time("Tue",21,22),1),
Shift(18,Time("Tue",22,23),1),

Shift(19,Time("Wed",18,19),1),
Shift(20,Time("Wed",19,20),1),
Shift(21,Time("Wed",20,21),1),
Shift(22,Time("Wed",21,22),1),
Shift(23,Time("Wed",22,23),1),

Shift(24,Time("Thu",18,19),1),
Shift(25,Time("Thu",19,20),1),
Shift(26,Time("Thu",20,21),1),
Shift(27,Time("Thu",21,22),1),
Shift(28,Time("Thu",22,23),1)
]


""" test 2: FFB 
shifts = [ 
Shift(0,Time("Sun",10.5,11.5),1),
Shift(1,Time("Sun",11.5,12.5),1),
Shift(2,Time("Sun",12.5,13.5),1),
Shift(3,Time("Sun",13.5,14.5),1),
Shift(4,Time("Sun",14.5,15.5),1),
Shift(5,Time("Sun",15.5,16.5),1),
Shift(6,Time("Mon",15.5,16.5),1),
Shift(7,Time("Tue",15.5,16.5),1),
Shift(8,Time("Wed",15.5,16.5),1),
Shift(9,Time("Thu",15.5,16.5),1),
Shift(10,Time("Fri",15.5,16.5),1)
]"""

""" test 3: VB 
shifts = [ 
Shift(1,Time("Mon",19,20),1),
Shift(2,Time("Mon",20,21),1),
Shift(3,Time("Mon",21,22),1),
Shift(4,Time("Tue",19,20),1),
Shift(5,Time("Tue",20,21),1),
Shift(6,Time("Tue",21,22),1),
Shift(7,Time("Wed",19,20),1),
Shift(8,Time("Wed",20,21),1),
Shift(9,Time("Wed",21,22),1),
Shift(10,Time("Thu",19,20),1),
Shift(11,Time("Thu",20,21),1),
Shift(12,Time("Thu",21,22),1)
] """
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

def is_continious(t1,t2):
    if(t1.day!=t2.day):
        return False
    elif(t1.end == t2.start):
        return True
    return False

def get_shift_id_from_var_name(name,number_of_shifts,shifts):
    str = name[2:]
    var_num = int(str)
    shift = var_num % number_of_shifts
    return shifts[shift].id

def get_name_of_employee_from_var_name(name,number_of_shifts):
    str = name[2:]
    var_num = int(str)
    employee = int(int(var_num) / int(number_of_shifts))
    return employees[employee].name

preffered_eq = []   
#create preferred shifts:
shifts.sort()

for ideal_shift_time in ideal_shift_times:
    s=0
    while(s < number_of_shifts - ideal_shift_time[0]):
        b = True;
        for i in range(ideal_shift_time[0]-1):
            if(not is_continious(shifts[s+i].time,shifts[s+i+1].time)):
                b = False
        if b:
            id = ""
            for i in range(ideal_shift_time[0]-1):
                id += str(shifts[s+i].id) + "-"
            id+=str(shifts[s + ideal_shift_time[0] - 1].id)
            if(debug2): print(id)
            new_shift = Shift(id,Time(shifts[s].time.day,shifts[s].time.start,shifts[s+ideal_shift_time[0]-1].time.end),1)
            new_shift.priority = ideal_shift_time[1]  # preferred job
            shifts.append(new_shift) 
            new_eq = [s,ideal_shift_time[0],len(shifts) - 1]  # triplet of the start, length and new location.
            preffered_eq.append(new_eq)
        s += 1

old_number_of_shifts = number_of_shifts
number_of_shifts = len(shifts)
if(debug2): 
    for s in shifts:
        print(s.id)

number_variables = number_of_shifts * number_of_employees 

variables = pulp.LpVariable.dicts("x",range(number_variables), 0, 1, cat = 'Integer')
lp_prob = pulp.LpProblem("schedule", pulp.LpMaximize)

# variables are : 0 - shifts-1 those for employee1, and so on.  to get xij, do
# i * number_of_shifts)+j

#preffered with preffered intersection:
for s1 in range(old_number_of_shifts,number_of_shifts):
    l_collisions = []
    for s2 in range(old_number_of_shifts,number_of_shifts):
        if(s1 >= s2):
            continue
        if(collision(shifts[s1].time, shifts[s2].time)):
            l_collisions.append(s2)
    nc = []
    for e in range(number_of_employees):
        nc.append((variables[get_index(e,s1,number_of_shifts)],1))
        for s2 in l_collisions:
            nc.append((variables[get_index(e,s2,number_of_shifts)],1))
    lp_prob += pulp.LpAffineExpression(nc) <= 1

# preffered shifts with the regular shift intersection:
for new_eq in preffered_eq:
    nc = []
    for e in range(number_of_employees):
        for i in range(new_eq[1]):
            nc.append((variables[get_index(e,new_eq[0]+i,number_of_shifts)],1))
        nc.append((variables[get_index(e,new_eq[2],number_of_shifts)],1))
    lp_prob += pulp.LpAffineExpression(nc) <= 1

"""
#each employee is able to work in a single shift only one time
for i in range(number_variables):
    new_line = np.zeros(number_variables)
    new_line[i] = 1
    A.append(new_line)
    b.append(1)
"""

#shifts constraints:
for s in range(number_of_shifts):
    new_line = np.zeros(number_variables)
    nc = []
    for e in range(number_of_employees):
        if(could_do_this_job(shifts[s], employees[e])):  # the employee can do it?
            nc.append((variables[get_index(e,s,number_of_shifts)],1))
            
        else:  # should kill this variable: (so adding the constaint of xij==0
            nl = []
            nl.append((variables[get_index(e,s,number_of_shifts)],1))
            lp_prob += pulp.LpAffineExpression(nl) == 0
    lp_prob += pulp.LpAffineExpression(nc) <= shifts[s].number_employees_needed

#week constraints:
for e in range(number_of_employees):
    nc = []
    for s in range(number_of_shifts):
        nc.append((variables[get_index(e,s,number_of_shifts)],total_time(shifts[s].time)))
    lp_prob += pulp.LpAffineExpression(nc) <= employees[e].max_week
   
#day constraints:
for e in range(number_of_employees):
    for d in range(len(days)):
        nc = []
        for s in range(number_of_shifts):
            if(shifts[s].time.day == days[d]):
                nc.append((variables[get_index(e,s,number_of_shifts)],total_time(shifts[s].time)))
        lp_prob += pulp.LpAffineExpression(nc) <= employees[e].max_day[d]
       
#check that each employee is only in one place at a time
for s1 in range(number_of_shifts):
    l_collisions = []
    for s2 in range(number_of_shifts):
        if(s1 >= s2):
            continue
        if(collision(shifts[s1].time, shifts[s2].time)):
            l_collisions.append(s2)
    for e in range(number_of_employees):
        nc = []
        new_line = np.zeros(number_variables)
        nc.append((variables[get_index(e,s1,number_of_shifts)],1))
        for s2 in l_collisions:
            nc.append((variables[get_index(e,s2,number_of_shifts)],1))
        lp_prob += pulp.LpAffineExpression(nc) <= 1
       
c = []
for e in range(number_of_employees):
    for s in range(number_of_shifts):
        bonus = np.random.uniform(0,epsilon)
        c.append((variables[get_index(e,s,number_of_shifts)],shifts[s].priority * total_time(shifts[s].time) + bonus))
lp_prob += pulp.LpAffineExpression(c) , "total_res"

if(debug): print(lp_prob)

lp_prob.solve()

if pulp.LpStatus[lp_prob.status] != "Optimal":
    print("error the problem is: " + pulp.LpStatus[lp_prob.status])
else:
    res = lp_prob.variables()
    if(debug):
        for i in range(len(res)):
            print("{} = {}".format(lp_prob.variables()[i].name, lp_prob.variables()[i].varValue))
    for v in res:
        if(v.varValue == 0):
            continue
        else:
            output = "shift " + str(get_shift_id_from_var_name(v.name,number_of_shifts,shifts)) + ": "
            output += get_name_of_employee_from_var_name(v.name,number_of_shifts)
            if(debug) : output += "\tvar: " + str(v.name) +"-"+ str(v.varValue)
            print(output)

""" the linprog.py solution:
#Ax<=b,max <c,x>
A = []
b = []  
c = []
eq_left = []
eq_right = []


number_variables = number_of_shifts * number_of_employees 
# variables are : 0 - shifts-1 those for employee1, and so on.  to get xij, do
# i * number_of_shifts)+j

#preffered with preffered intersection:
for s1 in range(old_number_of_shifts,number_of_shifts):
    l_collisions = []
    for s2 in range(old_number_of_shifts,number_of_shifts):
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

# preffered shifts with the regular shift intersection:
for new_eq in preffered_eq:
    eq = np.zeros(number_variables)
    for i in range(new_eq[1]):
        eq[new_eq[0]+i] = 1
    eq[new_eq[2]] = 1
    A.append(eq)
    b.append(1)
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
        c[get_index(e,s,number_of_shifts)] = - shifts[s].priority * total_time(shifts[s].time) - bonus

resolution,sol = linprog.linsolve(c,A,b,eq_left,eq_right,range(number_variables))

if(debug): print(sol)

if resolution != "solved":
    print(resolution)
else:
    for s in range(number_of_shifts):
        l = []
        print('shift ' + str(shifts[s].id))
        for e in range(number_of_employees):
            if sol[get_index(e,s,number_of_shifts)] > 1 - 1/max_shift_time:
                l.append(employees[e])
            output = ""
            for e in l:
                output += str(e.name) + "," 
        print("employees: " + output)
"""
