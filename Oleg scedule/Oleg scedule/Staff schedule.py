# from pylinprogmaster import linprog
import numpy as np
import random
import pulp

d = True
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
    if   day == ""   : return 0
    elif day == "Sun": return 1
    elif day == "Mon": return 2
    elif day == "Tue": return 3
    elif day == "Wed": return 4
    elif day == "Thu": return 5
    elif day == "Fri": return 6
    elif day == "Sat": return 7

class Time:
    start = 0
    end = 0
    def __init__(self, start, end, day = ""):
        self.start = day_to_num(day)*24 + start
        self.end = day_to_num(day)*24 + end
    def __eq__(self,other):
        return self.start == other.start
    def __lt__(self,other):
        return self.start < other.start

def tTime(day,start,end):
    return(Time(start,end,day))

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
    time = Time(0,0)
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
[tTime("Sun",8.5,24),
 tTime("Sun",14,24),
tTime("Mon",15,24),
tTime("Tue",16.5,24),
tTime("Wed",3,24),
tTime("Thu",16.5,24),
tTime("Fri",13,24),
tTime("Sat",10,24)],
[1,2,3,4]),

Employee(2,"Jenny",
[tTime("Sun",8.5,24),
tTime("Mon",12,24),
tTime("Tue",12,24),
tTime("Wed",12,18),
tTime("Wed",21,24),
tTime("Thu",12,24),
tTime("Fri",12,24),
tTime("Sat",8.5,24)],
[1,2,3,4]),

Employee(3,"Tom",
[tTime("Sun",12,24),
tTime("Mon",15,24),
tTime("Tue",15,24),
tTime("Wed",15,24),
tTime("Thu",15,24),
tTime("Fri",13,18)],
[1,2,3,4]),

Employee(4,"Amy",
[tTime("Sun",8.5,24),
tTime("Sun",14,24),
tTime("Mon",15,24),
tTime("Tue",16.5,24),
tTime("Wed",15,18),
tTime("Thu",16.5,24),
tTime("Fri",13,24),
tTime("Sat",10,24)],
[1,2,3,4])
]
""" test 1: BB """
shifts = [ 
Shift(0,tTime("Sun",12,13),1),
Shift(1,tTime("Sun",13,14),1),
Shift(2,tTime("Sun",14,15),1),
Shift(3,tTime("Sun",15,16),1),
Shift(4,tTime("Sun",16,17),1),
Shift(5,tTime("Sun",17,18),1),
Shift(6,tTime("Sun",18,19),1),
Shift(7,tTime("Sun",19,20),1),
Shift(8,tTime("Sun",20,21),1),

Shift(9,tTime("Mon",18,19),1),
Shift(10,tTime("Mon",19,20),1),
Shift(11,tTime("Mon",20,21),1),
Shift(12,tTime("Mon",21,22),1),
Shift(13,tTime("Mon",22,23),1),

Shift(14,tTime("Tue",18,19),1),
Shift(15,tTime("Tue",19,20),1),
Shift(16,tTime("Tue",20,21),1),
Shift(17,tTime("Tue",21,22),1),
Shift(18,tTime("Tue",22,23),1),

Shift(19,tTime("Wed",18,19),1),
Shift(20,tTime("Wed",19,20),1),
Shift(21,tTime("Wed",20,21),1),
Shift(22,tTime("Wed",21,22),1),
Shift(23,tTime("Wed",22,23),1),

Shift(24,tTime("Thu",18,19),1),
Shift(25,tTime("Thu",19,20),1),
Shift(26,tTime("Thu",20,21),1),
Shift(27,tTime("Thu",21,22),1),
Shift(28,tTime("Thu",22,23),1)
]

""" test 2: FFB 
shifts = [ 
Shift(0,tTime("Sun",10.5,11.5),1),
Shift(1,tTime("Sun",11.5,12.5),1),
Shift(2,tTime("Sun",12.5,13.5),1),
Shift(3,tTime("Sun",13.5,14.5),1),
Shift(4,tTime("Sun",14.5,15.5),1),
Shift(5,tTime("Sun",15.5,16.5),1),
Shift(6,tTime("Mon",15.5,16.5),1),
Shift(7,tTime("Tue",15.5,16.5),1),
Shift(8,tTime("Wed",15.5,16.5),1),
Shift(9,tTime("Thu",15.5,16.5),1),
Shift(10,tTime("Fri",15.5,16.5),1)
]

 test 3: VB 
shifts = [ 
Shift(1,tTime("Mon",19,20),1),
Shift(2,tTime("Mon",20,21),1),
Shift(3,tTime("Mon",21,22),1),
Shift(4,tTime("Tue",19,20),1),
Shift(5,tTime("Tue",20,21),1),
Shift(6,tTime("Tue",21,22),1),
Shift(7,tTime("Wed",19,20),1),
Shift(8,tTime("Wed",20,21),1),
Shift(9,tTime("Wed",21,22),1),
Shift(10,tTime("Thu",19,20),1),
Shift(11,tTime("Thu",20,21),1),
Shift(12,tTime("Thu",21,22),1)
] 

 test 4: Soc 
shifts = [ 
Shift(0,tTime("Sun",13,14),1),
Shift(1,tTime("Sun",14,15),1),
Shift(2,tTime("Sun",15,16),1),
Shift(3,tTime("Sun",16,17),1),
Shift(4,tTime("Sun",17,18),1),
Shift(5,tTime("Sun",18,19),1),

Shift(6,tTime("Mon",16,17),1),
Shift(7,tTime("Mon",17,18),1),
Shift(8,tTime("Mon",18,19),1),

Shift(9,tTime("Tue",16,17),1),
Shift(10,tTime("Tue",17,18),1),
Shift(11,tTime("Tue",18,19),1),


Shift(12,tTime("Wed",16,17),1),
Shift(13,tTime("Wed",17,18),1),
Shift(14,tTime("Wed",18,19),1),


Shift(15,tTime("Thu",16,17),1),
Shift(16,tTime("Thu",17,18),1),
Shift(17,tTime("Thu",18,19),1),


Shift(18,tTime("Fri",16,17),1),
Shift(19,tTime("Fri",17,18),1),
Shift(20,tTime("Fri",18,19),1)
] 

 test 5: Soft 
shifts = [ 
Shift(1,tTime("Mon",17,18.5),1),
Shift(2,tTime("Mon",18.5,20),1),

Shift(3,tTime("Tue",17,18.5),1),
Shift(4,tTime("Tue",18.5,20),1),

Shift(5,tTime("Wed",17,18.5),1),
Shift(6,tTime("Wed",18.5,20),1),

Shift(7,tTime("Thu",17,18.5),1),
Shift(8,tTime("Thu",18.5,20),1),

Shift(9,tTime("Fri",17,18.5),1),
Shift(10,tTime("Fri",18.5,20),1),

Shift(11,tTime("Sat",12.5,14),1),
Shift(12,tTime("Sat",14,15.5),1),
Shift(13,tTime("Sat",15.5,17),1),
Shift(14,tTime("Sat",17,18.5),1),
Shift(15,tTime("Sat",18.5,20),1),
Shift(16,tTime("Sat",18.5,20),1),
]

 test 6: WP 
shifts = [ 
Shift(1,tTime("Mon",18,19),1),
Shift(2,tTime("Mon",19,20),1),

Shift(3,tTime("Mon",21,22),1),
Shift(4,tTime("Mon",22,23),1),

Shift(5,tTime("Tue",18,19),1),
Shift(6,tTime("Tue",19,20),1),
Shift(7,tTime("Tue",20,21),1),

Shift(8,tTime("Tue",22,23),1),

Shift(9,tTime("Wed",18,19),1),
Shift(10,tTime("Wed",19,20),1),

Shift(11,tTime("Wed",21,22),1),
Shift(12,tTime("Wed",22,23),1),

Shift(13,tTime("Thu",18,19),1),

Shift(14,tTime("Thu",20,21),1),
Shift(15,tTime("Thu",21,22),1),
Shift(16,tTime("Thu",22,23),1)
] """

number_of_employees = len(employees)
number_of_shifts = len(shifts)

def get_start_day(t):
    r = int(t.start / 24)
    return r

def get_end_day(t):
    r = int(t.end / 24)
    return r

def collision(x,y):
    if(x.end <= y.start):
        return(False)
    if(x.start >= y.end):
        return(False)
    return(True)

def in_time(x,y):  # check if x is in y
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
    if(t1.end >= t2.start - yet_count_as_continous):
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
            new_shift = Shift(id,Time(shifts[s].time.start,shifts[s+ideal_shift_time[0]-1].time.end),1)
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

for d in days:  # the shifts should be on full hours.
    for h in range(hours_in_day):
        t = tTime(d,h,h+1)
        l = []
        for s in range(number_of_shifts):
            if (collision(t,shifts[s].time)):
                l.append(s)
        nc_int = []
        nc_cont = []
        for e in range(number_of_employees):
            for s in l:
                nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
                nc_cont.append((variables_cont[get_index(e,s,number_of_shifts)],1))
        lp_prob_int += pulp.LpAffineExpression(nc_int) <= 1    
        lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= 1

'''
#preffered with preffered intersection:
for s1 in range(number_of_shifts):
    l_collisions = []
    for s2 in range(number_of_shifts):
        if(s1 >= s2): #to avoid multiplications
            continue
        if(collision(shifts[s1].time, shifts[s2].time)):
            nc_int = []
            nc_cont = []
            for e in range(number_of_employees):
                
                nc_int.append((variables_int[get_index(e,s1,number_of_shifts)],1))
                nc_cont.append((variables_cont[get_index(e,s1,number_of_shifts)],1))
                
                nc_int.append((variables_int[get_index(e,s2,number_of_shifts)],1))
                nc_cont.append((variables_cont[get_index(e,s2,number_of_shifts)],1))   
                
            lp_prob_int += pulp.LpAffineExpression(nc_int) <= 1    
            lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= 1
              
    """
    nc_int = []
    nc_cont = []
    for e in range(number_of_employees):
        nc_int.append((variables_int[get_index(e,s1,number_of_shifts)],1))
        nc_cont.append((variables_cont[get_index(e,s1,number_of_shifts)],1))
        
        for s2 in l_collisions:
            nc_int.append((variables_int[get_index(e,s2,number_of_shifts)],1))
            nc_cont.append((variables_cont[get_index(e,s2,number_of_shifts)],1))
    lp_prob_int += pulp.LpAffineExpression(nc_int) <= 1    
    lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= 1
    """
# preffered shifts with the regular shift intersection:
for new_eq in preffered_eq:
    nc_int = []
    nc_cont = []
    
    for e in range(number_of_employees):
        for i in range(new_eq[1]):
            nc_int.append((variables_int[get_index(e,new_eq[0]+i,number_of_shifts)],1))
            nc_cont.append((variables_cont[get_index(e,new_eq[0]+i,number_of_shifts)],1))
        nc_int.append((variables_int[get_index(e,new_eq[2],number_of_shifts)],1))
        nc_cont.append((variables_cont[get_index(e,new_eq[2],number_of_shifts)],1))

    lp_prob_int += pulp.LpAffineExpression(nc_int) <= 1
    lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= 1
'''
#max of 1 shift a day (maybe a longer one)
for e in range(number_of_employees):
    for d in range(len(days)):
        nc_int = []
        nc_cont = []
        
        for s in range(number_of_shifts):
            if(get_day(shifts[s].time) == days[d]):
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
            if(get_start_day(shifts[s].time) == day_to_num(days[d]) or get_end_day(shifts[s].time) == day_to_num(days[d])):  # TODO : make it work for half a shift of time (the shift may continue to next day)
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

