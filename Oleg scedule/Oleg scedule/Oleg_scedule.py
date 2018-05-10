from pylinprogmaster import linprog
import numpy as np
import random

debug = False
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

""" test 1: BB"""
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
        c[get_index(e,s,number_of_shifts)] = - shifts[s].priority * total_time(shifts[s].time) - bonus

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
            output = ""
            for e in l:
                output += str(e.name) + "," 
        print("employees: " + output)
