# from pylinprogmaster import linprog
import numpy as np
import random
import pulp

debug = False
debug2 = False
debug3 = False
debug_var = False
epsilon_1 = 0.01
epsilon_2 = 0.01

hours_in_day = 24
max_shift_time = 12.0
ideal_shift_times = [(4,15),(3,13),(2,5)]  # 4+1 < 3+2
yet_count_as_continous = 1  # the legnth of maximal break

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
[Time("Sun",8.5,24),
 Time("Sun",14,24),
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
[Time("Sun",8.5,24),
Time("Sun",14,24),
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
Shift(6,Time("Sun",18,19),1),
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
]

 test 3: VB 
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
] 

 test 4: Soc 
shifts = [ 
Shift(0,Time("Sun",13,14),1),
Shift(1,Time("Sun",14,15),1),
Shift(2,Time("Sun",15,16),1),
Shift(3,Time("Sun",16,17),1),
Shift(4,Time("Sun",17,18),1),
Shift(5,Time("Sun",18,19),1),

Shift(6,Time("Mon",16,17),1),
Shift(7,Time("Mon",17,18),1),
Shift(8,Time("Mon",18,19),1),

Shift(9,Time("Tue",16,17),1),
Shift(10,Time("Tue",17,18),1),
Shift(11,Time("Tue",18,19),1),


Shift(12,Time("Wed",16,17),1),
Shift(13,Time("Wed",17,18),1),
Shift(14,Time("Wed",18,19),1),


Shift(15,Time("Thu",16,17),1),
Shift(16,Time("Thu",17,18),1),
Shift(17,Time("Thu",18,19),1),


Shift(18,Time("Fri",16,17),1),
Shift(19,Time("Fri",17,18),1),
Shift(20,Time("Fri",18,19),1)
] 

 test 5: Soft 
shifts = [ 
Shift(1,Time("Mon",17,18.5),1),
Shift(2,Time("Mon",18.5,20),1),

Shift(3,Time("Tue",17,18.5),1),
Shift(4,Time("Tue",18.5,20),1),

Shift(5,Time("Wed",17,18.5),1),
Shift(6,Time("Wed",18.5,20),1),

Shift(7,Time("Thu",17,18.5),1),
Shift(8,Time("Thu",18.5,20),1),

Shift(9,Time("Fri",17,18.5),1),
Shift(10,Time("Fri",18.5,20),1),

Shift(11,Time("Sat",12.5,14),1),
Shift(12,Time("Sat",14,15.5),1),
Shift(13,Time("Sat",15.5,17),1),
Shift(14,Time("Sat",17,18.5),1),
Shift(15,Time("Sat",18.5,20),1),
Shift(16,Time("Sat",18.5,20),1),
]

 test 6: WP 
shifts = [ 
Shift(1,Time("Mon",18,19),1),
Shift(2,Time("Mon",19,20),1),

Shift(3,Time("Mon",21,22),1),
Shift(4,Time("Mon",22,23),1),

Shift(5,Time("Tue",18,19),1),
Shift(6,Time("Tue",19,20),1),
Shift(7,Time("Tue",20,21),1),

Shift(8,Time("Tue",22,23),1),

Shift(9,Time("Wed",18,19),1),
Shift(10,Time("Wed",19,20),1),

Shift(11,Time("Wed",21,22),1),
Shift(12,Time("Wed",22,23),1),

Shift(13,Time("Thu",18,19),1),

Shift(14,Time("Thu",20,21),1),
Shift(15,Time("Thu",21,22),1),
Shift(16,Time("Thu",22,23),1)
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
    elif(t1.end >= t2.start - yet_count_as_continous):
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

def get_variable_index_from_var_name(name,number_of_shifts):
    str = name[2:]
    return int(str)

preffered_eq = []   
#create preferred shifts:
shifts.sort()

for ideal_shift_time in ideal_shift_times:
    s=0
    while(s <= number_of_shifts - ideal_shift_time[0]):
        b = True;
        for i in range(ideal_shift_time[0]-1):
            if(not is_continious(shifts[s+i].time,shifts[s+i+1].time)):
                b = False
        if b:
            id = ""
            for i in range(ideal_shift_time[0]-1):
                id += str(shifts[s+i].id) + "-"
            id+=str(shifts[s + ideal_shift_time[0] - 1].id)
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

variables_cont = pulp.LpVariable.dicts("x",range(number_variables),   0, 1,cat="Continuous")
lp_prob_cont = pulp.LpProblem("schedule", pulp.LpMaximize)

variables_int = pulp.LpVariable.dicts("y",range(number_variables),   0, 1,cat="Integer")
lp_prob_int = pulp.LpProblem("schedule_int", pulp.LpMaximize)
# variables are : 0 - shifts-1 those for employee1, and so on.  to get xij, do
# i * number_of_shifts)+j

#max of 1 shift a day (maybe a longer one)
for e in range(number_of_employees):
    for d in range(len(days)):
        nc_int = []
        nc_cont = []
        
        for s in range(number_of_shifts):
            if(shifts[s].time.day == days[d]):
                nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
                nc_cont.append((variables_cont[get_index(e,s,number_of_shifts)],1))
        lp_prob_int += pulp.LpAffineExpression(nc_int) <= 1
        lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= 1


#shifts constraints:
for s in range(number_of_shifts):
    new_line = np.zeros(number_variables)
    nc_int = []
    nc_cont = []
    
    for e in range(number_of_employees):
        if(could_do_this_job(shifts[s], employees[e])):  # the employee can do it?
            nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
            nc_cont.append((variables_cont[get_index(e,s,number_of_shifts)],1))
            
        else:  # should kill this variable: (so adding the constaint of xij==0
            nl_int = []
            nl_cont = []
            nl_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
            nl_cont.append((variables_cont[get_index(e,s,number_of_shifts)],1))
            lp_prob_int += pulp.LpAffineExpression(nl_int) == 0
            lp_prob_cont += pulp.LpAffineExpression(nl_cont) == 0
    lp_prob_int += pulp.LpAffineExpression(nc_int) <= shifts[s].number_employees_needed
    lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= shifts[s].number_employees_needed

#week constraints:
for e in range(number_of_employees):
    nc_int = []
    nc_cont = []
    
    for s in range(number_of_shifts):
        nc_int.append((variables_int[get_index(e,s,number_of_shifts)],total_time(shifts[s].time)))
        nc_cont.append((variables_cont[get_index(e,s,number_of_shifts)],total_time(shifts[s].time)))
    lp_prob_int += pulp.LpAffineExpression(nc_int) <= employees[e].max_week
    lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= employees[e].max_week
#day constraints:
for e in range(number_of_employees):
    for d in range(len(days)):
        nc_int = []
        nc_cont = []
        
        for s in range(number_of_shifts):
            if(shifts[s].time.day == days[d]):
                nc_int.append((variables_int[get_index(e,s,number_of_shifts)],total_time(shifts[s].time)))
                nc_cont.append((variables_cont[get_index(e,s,number_of_shifts)],total_time(shifts[s].time)))        
        lp_prob_int += pulp.LpAffineExpression(nc_int) <= employees[e].max_day[d]
        lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= employees[e].max_day[d]
       
#check that each employee is only in one place at a time
for s1 in range(number_of_shifts):
    l_collisions = []
    for s2 in range(number_of_shifts):
        if(s1 >= s2):
            continue
        if(collision(shifts[s1].time, shifts[s2].time)):
            l_collisions.append(s2)
    for e in range(number_of_employees):
        nc_int = []
        nc_cont = []
        
        new_line = np.zeros(number_variables)
        nc_int.append((variables_int[get_index(e,s1,number_of_shifts)],1))
        nc_cont.append((variables_cont[get_index(e,s1,number_of_shifts)],1))
        
        for s2 in l_collisions:
            nc_int.append((variables_int[get_index(e,s2,number_of_shifts)],1))
            nc_cont.append((variables_cont[get_index(e,s2,number_of_shifts)],1))
         
        lp_prob_int += pulp.LpAffineExpression(nc_int) <= 1
        lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= 1
       
c_int = []
c_cont = []

for e in range(number_of_employees):
    for s in range(number_of_shifts):
        bonus = np.random.uniform(0,epsilon_1)
        c_int.append((variables_int[get_index(e,s,number_of_shifts)],shifts[s].priority + bonus))
        c_cont.append((variables_cont[get_index(e,s,number_of_shifts)],shifts[s].priority + bonus))

lp_prob_int += pulp.LpAffineExpression(c_int) , "total_res"
lp_prob_cont += pulp.LpAffineExpression(c_cont) , "total_res"

if(debug): print(lp_prob_cont)
if(debug): print("INTTT")
if(debug): print(lp_prob_int)

lp_prob_cont.solve()

if pulp.LpStatus[lp_prob_cont.status] != "Optimal":
    print("error the problem is: " + pulp.LpStatus[lp_prob_cont.status])

else:
    res = lp_prob_cont.variables()
    if(debug3):
        for i in range(len(res)):
            print("{} = {}".format(lp_prob_cont.variables()[i].name, lp_prob_cont.variables()[i].varValue))
    for v in res:
        if(debug3):
            if(v.varValue != 1 and v.varValue != 0):
                print("{} = {}".format(v.name, v.varValue))
        if(v.varValue == 1):
            ne = []
            index = get_variable_index_from_var_name(v.name,number_of_shifts)
            ne.append((variables_int[index],1))
            lp_prob_int += pulp.LpAffineExpression(ne) == 1

print("cont : " + str(pulp.value(lp_prob_cont.objective)))

lp_prob_int.solve()

if pulp.LpStatus[lp_prob_int.status] != "Optimal":
    print("error the problem is: " + pulp.LpStatus[lp_prob_int.status])
else:
    res = lp_prob_int.variables()
    if(debug_var):
        for i in range(len(res)):
            print("{} = {}".format(lp_prob_int.variables()[i].name, lp_prob_int.variables()[i].varValue))
    for v in res:
        if(v.varValue == 0):
            continue
        else:
            output = "shift " + str(get_shift_id_from_var_name(v.name,number_of_shifts,shifts)) + ": "
            output += get_name_of_employee_from_var_name(v.name,number_of_shifts)
            if(debug_var) : output += "\tvar: " + str(v.name) +"-"+ str(v.varValue)
            print(output)
print("int : " + str(pulp.value(lp_prob_int.objective)))

"""
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
print(pulp.value(lp_prob.objective))"""

