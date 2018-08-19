import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import options, parse_command_line, parse_config_file
import logging
import json

from pylinprogmaster import linprog
import numpy as np
import random
import pulp
import time

we_love_avi = False
epsilon_1 = 0.01
smallest_break_possible = 0
days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
ideal_shift_time = 3 #could be 4 aswell. 
ideal_shift_times = [(1,1),(3,2),(5,2)]
hours_in_day = 24
start_time = time.clock()

def day_to_num(day):
    if   day == ""   : return 0
    elif day == "Sun": return 0
    elif day == "Mon": return 1
    elif day == "Tue": return 2
    elif day == "Wed": return 3
    elif day == "Thu": return 4
    elif day == "Fri": return 5
    elif day == "Sat": return 6

class Time:
    start = 0
    end = 0
    def __init__(self, start, end, day=""):
        self.start = day_to_num(day) * hours_in_day + start
        self.end = day_to_num(day) * hours_in_day + end
    def __eq__(self,other):
        return self.start == other.start
    def __lt__(self,other):
        return self.start < other.start
def tTime(day,start,end):
    return Time(start,end,day)

class Employee:
    id = 0
    name = ""
    availability = [[]]
    # jobs = [] not needed
    max_day = []
    max_week = 0
    number_tokens = 10
    def __init__(self, id, name, availability, jobs, max_day=[4,4,4,4,4,4,4], max_week=20, number_tokens=10):
        self.id = id
        self.name = name
        self.availability = availability
        self.jobs = jobs
        self.max_day = max_day
        self.max_week = max_week

class Game:
    id = 0
    time = []
    job_ids = [0,1]                      # job ids are 0 and 1
    number_employees_needed = [1,1]      # both jobs need 1 employee
    requiredEmployees = [[0,2, [1,2]]]   #job_id    number of employees    list of employees_ids   
    location_id = 0  # TODO :ask them
    priority = 1
    availableEmployees = []
    def is_eq(self,other):
        return (self.time.start == self.time.start and self.time.end == self.time.end)
    def __init__(self,id, time, job_id, number_employees_needed=1, priority=1):
        self.id = id
        self.time = time
        self.job_id = job_id
        self.number_employees_needed = 1
    def __eq__(self,other):
        return self.time == other.time
    def __lt__(self,other):
        return self.time < other.time

class Shift:
    id = 0
    job_id = 0
    time = 0
    number_of_employees = 1
    priority = 1
    def is_eq(self,other):
        return (self.time.start == self.time.start and self.time.end == self.time.end)
    def __init__(self,id, time, job_id, number_employees_needed=1, priority=1):
        self.id = id
        self.time = time
        self.job_id = job_id
        self.number_employees_needed = 1
    def __eq__(self,other):
        return self.time == other.time
    def __lt__(self,other):
        return self.time < other.time



'''
example = '{"params":{"shifts":[{"id":0,"time":[3,6],"jobId":1},{"id":1,"time":[6,9],"jobId":1},{"id":2,"time":[9,12],"jobId":1},{"id":3,"time":[100,102],"jobId":2},{"id":4,"time":[140,142],"jobId":2}],"employees":[{"id":0,"availability":[[0,1000,0]],"maxDayTime":[4,4,4,4,4,4,4],"maxWeekTime":"20","jobIds":[1,2,3]},{"id":1,"availability":[[0,1000,0]],"maxDayTime":[4,4,4,4,4,4,4],"maxWeekTime":"20","jobIds":[1,2,3]},{"id":2,"availability":[[0,1000,0]],"maxDayTime":[4,4,4,4,4,4,4],"maxWeekTime":"20","jobIds":[1,2,3]},{"id":3,"availability":[[0,1000,0]],"maxDayTime":[4,4,4,4,4,4,4],"maxWeekTime":"20","jobIds":[1,2,3]}]}}'
data = json.loads(example)

shifts = []
#setup shifts from data
for sh in range(len(data['params']['shifts'])):
    shifts.append(Shift(data['params']['shifts'][sh]['id'], data['params']['shifts'][sh]['time'], data['params']['shifts'][sh]['jobId']))

#setup employees from data
employees = []
for emp in range(len(data['params']['employees'])):
             #id, name, availability, jobs, max_day, max_week = 20
    employees.append(Employee(data['params']['employees'][emp]['id'], 'EmployeeName', data['params']['employees'][emp]['availability'], data['params']['employees'][emp]['jobIds'], data['params']['employees'][emp]['maxDayTime'], int(data['params']['employees'][emp]['maxWeekTime'])))
'''

class Time:
    start = 0
    end = 0
    def __init__(self, start, end, day=""):
        self.start = day_to_num(day) * hours_in_day + start
        self.end = day_to_num(day) * hours_in_day + end
    def __eq__(self,other):
        return self.start == other.start
    def __lt__(self,other):
        return self.start < other.start
def tTime(day,start,end):
    return Time(start,end,day)

class Employee:
    id = 0
    name = ""
    availability = [[]]
    jobs = []
    max_day = []
    max_week = 0
    number_tokens = 10
    def __init__(self, id, name, availability, jobs, max_day=[4,4,4,4,4,4,4], max_week=20, number_tokens=10):
        self.id = id
        self.name = name
        self.availability = availability
        self.jobs = jobs
        self.max_day = max_day
        self.max_week = max_week

class Shift:
    id = 0
    time = []
    job_id = 0
    number_employees_needed = 1
    priority = 1
    availableEmployees = []
    def is_eq(self,other):
        return (self.time.start == self.time.start and self.time.end == self.time.end)
    def __init__(self,id, time, job_id, number_employees_needed=1, priority=1):
        self.id = id
        self.time = time
        self.job_id = job_id
        self.number_employees_needed = 1
    def __eq__(self,other):
        return self.time == other.time
    def __lt__(self,other):
        return self.time < other.time

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
[1,2,3,4])]


""" test 2: FFB  *** should be changed to Games"""
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

games = []

def time_in_week(t):  # TODO: change if there is more than one week
    return(t.end - t.start)

def get_end_time(shift):
    return shift.time.end
    
def get_start_day(t):
    r = int(t.start / hours_in_day)
    return r

def get_end_day(t):
    r = int(t.end / hours_in_day)
    return r

def time_in_day(t,d):
    """check the size of the intersection of a shift and a day"""
    #d_int = day_to_num(d)
    start_h = t.start - d * hours_in_day
    if(get_end_day(t) > d):  # the next day
        res = hours_in_day - start_h
    else:
        res = t.end - t.start
    return(max(res,0))

def collision(x,y):
    """check if the time x intersects with y"""
    if(x.end <= y.start):
        return(False)
    if(x.start >= y.end):
        return(False)
    return(True)

def in_time(x,y):  # check if x is in y
    """check whether the time x is in y"""
    if(x.start < y.start):
        return(False)
    if(x.end > y.end):
        return(False)
    return(True)

def could_do_this_job(s,e): #shift,start time,employee
    """
    check whether employee x can do the job s (in his job_id and time)
    """
    if(s.job_id not in e.jobs): #in array check employee tru and false
        return(False)
    for t in e.availability:
        if in_time(s.time, t):
            return(True)
    return(False)

def total_time(t):
    return(t.end - t.start)


def get_index(employee,shift,number_of_shifts):
    return(employee * number_of_shifts + shift)

def is_continious(t1,t2):
    """
    check whether t2 starts right after t1 (or with a decent break).
    """
    if(collision(t1,t2)):
        return(False)
    if(t1.end == t2.start):
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

def valid(v):  #this is a var, return true if it's valid.
    """
    a variable will be count as not valid if it is one of the soft variables (it is Continuous among other things)
    """
    if v.cat == "Continuous" :
        return(False)
    return(True)

def get_id_of_employee_from_var_name(name,number_of_shifts):
    """
    the var name starts from the 3rd char x_23 for example.
    """
    str = name[2:]
    var_num = int(str)
    employee = int(int(var_num) / int(number_of_shifts))
    return employees[employee].id

def get_variable_index_from_var_name(name,number_of_shifts):
    """
    the var name starts from the 3rd char x_23 for example.
    """
    str = name[2:]
    return int(str)

def normalize_pref(employees, games):
    """ 
    functio that move all the input from the json format (in lists) to my classes. 
    also changes the prefs to make it in a good format (spreading the tokens accordingly).
    note : not to call in the staff (until formatted with the server)
    returns the list of shifts from the games.
    """

    """
    for g in games:
       t = Time(s.time[0],s.time[1])
       s.time = t
    """
    for e in employees:
        s = 0
        for i in range(len(e.availability)):
            p = [Time(e.availability[i][0],e.availability[i][1]),e.availability[i][2]]
            e.availability[i] = p
            s+=p[1]    # sum of all the preferences.
        if s == 0 : #there are no preffered so it is same as all pref.
            for p in e.availability:
                p[1] = 1
                s+=p[1]    # sum of all the preferences.

        for p in e.availability:
            if p[1] == 0:
                p[1] = 1
            else: # p[1] == 1
                p[1] = 1 + (1 / s) * e.number_tokens

def create_shifts(games,ideal_shifts_times,number_of_shifts):
    shifts = []   
    #create preferred shifts:
    games.sort()  # assuming there is no intersecting games !!!!!!
    
    for ideal_shift_time in ideal_shifts_times:
        s = 0
        while(s <= number_of_shifts - ideal_shift_time[0]):
            b = True
            for i in range(ideal_shift_time[0] - 1):
                if(not is_continious(games[s + i].time,games[s + i + 1].time)):  #not continious so no extra shifts needed.
                    b = False
            if b:
                id = ""
                for i in range(ideal_shift_time[0] - 1):
                    id += str(games[s + i].id) + "-"
                id += str(shifts[s + ideal_shift_time[0] - 1].id)
                new_shift = Shift(id,Time(shifts[s].time.start,shifts[s + ideal_shift_time[0] - 1].time.end),1)
                new_shift.priority = ideal_shift_time[1]  # preferred job
                preffered_shifts.append(new_shift) 
            s += 1
    return shifts


def solution(employees,games):
    time_init = time.clock() - start_time
    custom_s1 = time.clock()
    custom_e1 = time.clock() - custom_s1
    
    if(ideal_shift_time == 3):
        ideal_shifts_times = [(2,3),(3,6),(4,8),(5,8),(6,8)]
    # elif(ideal_shift_time == 4):
    # elif(ideal_shift_time == 5):
    
    normalize_pref(employees,games)

    shifts = create_shifts(games,ideal_shift_times,number_of_games)
    
    number_of_employees = len(employees)
    number_of_games = len(games)

    number_variables = number_of_shifts * number_of_employees
        
    custom_s2 = time.clock()
    
    lp_prob_cont = pulp.LpProblem("schedule", pulp.LpMaximize)  # creating the Lp problem
        
    variables_int = pulp.LpVariable.dicts("y",range(number_variables),   0, 1,cat="Binary")  # the variables
    lp_prob_int = pulp.LpProblem("schedule_int", pulp.LpMaximize)
    # variables are : 0 - shifts-1 those for employee1, and so on.  to get
    # x_ij, do
    # i * number_of_shifts)+j [ using the function get_index ]
    
    custom_e2 = time.clock() - custom_s2
    custom_s3 = time.clock()
    
    # shifts constraints:
    for s in range(number_of_shifts):
        nc_int = []
        for e in range(number_of_employees):
            if(could_do_this_job(shifts[s], employees[e])):  # the employee can do it?
                nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))  # the employee works here once.

            else:  # should kill this variable: (so adding the constaint of xij==0
                nl_int = []
                nl_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
                lp_prob_int += pulp.LpAffineExpression(nl_int) == 0  # kill the variable
        lp_prob_int += pulp.LpAffineExpression(nc_int) <= shifts[s].number_employees_needed
        
    custom_e3 = time.clock() - custom_s3
    custom_s4 = time.clock()
    
    #week constraints:
    for e in range(number_of_employees):
        nc_int = []
        for s in range(number_of_shifts):
            nc_int.append((variables_int[get_index(e,s,number_of_shifts)],time_in_week(shifts[s].time)))
        lp_prob_int += pulp.LpAffineExpression(nc_int) <= employees[e].max_week
        
    custom_e4 = time.clock() - custom_s4
    custom_s5 = time.clock()

    #day constraints:
    for e in range(number_of_employees):
        for d in range(len(days)):
            nc_int = []
            for s in range(number_of_shifts):
                if(get_start_day(shifts[s].time) == day_to_num(days[d])):
                    nc_int.append((variables_int[get_index(e,s,number_of_shifts)],time_in_day(shifts[s].time,d)))
                    # CONT_SOL :
                    # nc_cont.append((variables_cont[get_index(e,s,number_of_shifts)],time_in_day(shifts[s].time,d)))
            lp_prob_int += pulp.LpAffineExpression(nc_int) <= employees[e].max_day[d]

    custom_e5 = time.clock() - custom_s5            
    custom_s6 = time.clock()
        
    #check that each employee is only in one place at a time [changed** , can't
    #work in diff of smallest_break_possible hours]
    # shifts_end = list(shifts)
    # shifts_end.sort(key=get_end_time)
    for s in np.arange(number_of_shifts):
        t = Time(shifts[s].time.start - smallest_break_possible, shifts[s].time.end + smallest_break_possible)
        # want to receive the indeces of those who intersects with s.
        l = np.zeros(number_of_shifts) 
        l[s] = 1
        for s2 in np.arange(number_of_shifts):
            if (collision(t,shifts[s2].time)):
                l[s2] = 1
        if(len(l) <= 1) : continue  # there is 0 or one shift in this time so there is no problem
        for e in np.arange(number_of_employees):
            nc_int = []
            for s in np.arange(number_of_shifts):
                if l[s] == 1:
                    nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))                    
            lp_prob_int += pulp.LpAffineExpression(nc_int) <= 1
                        
    custom_e6 = time.clock() - custom_s6
        
    c_int = []

    custom_s7 = time.clock()
    for e in range(number_of_employees):
        for s in range(number_of_shifts):
            bonus = np.random.uniform(epsilon_1 * shifts[s].priority,2 * epsilon_1 * shifts[s].priority)
            c_int.append((variables_int[get_index(e,s,number_of_shifts)], 1 + bonus))
                
    custom_e7 = time.clock() - custom_s7
    
    # soft constraints: !!!!  (they wouldn't surely be happening but there is a
    # fine if they won't (and the algorithm will try to avoid it but not at any
    # cost) [the bigger the fine the mroe important it is]
    # once a week:
    for e in range(number_of_employees):
        nc_int = []
        for s in range(number_of_shifts):
            nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
            ll = "week_-_" + str(e) # the starting name
        v1 = pulp.LpVariable(name = ll + "elastic_neg", upBound=0)
        nc_int.append((v1,1))  # if the value is big it gives more space
        lp_prob_int += pulp.LpAffineExpression(nc_int) <= 3
        
        c_int.append((v1,0.2))  # the fine is 0.2.

    # once a day:
    for e in range(number_of_employees):
        for d in range(len(days)):
            nc_int = []
    
            for s in range(number_of_shifts):
                if(get_start_day(shifts[s].time) == day_to_num(days[d])):
                    nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
            ll = str(e) + " day - " + str(d)
            v1 = pulp.LpVariable(name = ll + "elastic_neg", upBound=0)
            nc_int.append((v1,1))  # if the value is big it gives more space
            lp_prob_int += pulp.LpAffineExpression(nc_int) <= 1
        
            c_int.append((v1,0.5))  # the fine is 0.5.
    
    #everyone works atleast once a week:
    for e in range(number_of_employees):
        nc_int = []
        for s in range(number_of_shifts):
            nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
        ll = "love_to_work_-_" + str(e) # the starting name
        v1 = pulp.LpVariable(name = ll + "elastic_pos", lowBound = 0,upBound = number_of_shifts,cat = "Continuous")
        
        nc_int.append((v1,1))  # if the value is big it gives more space
        lp_prob_int += pulp.LpAffineExpression(nc_int) >= 1
        
        c_int.append((v1,-0.8))  # the fine is 0.8.
    
    custom_s8 = time.clock()
    lp_prob_int.setObjective(pulp.LpAffineExpression(c_int))
    custom_e8 = time.clock() - custom_s8
        
        
    custom_s11 = time.clock()
    lp_prob_int.solve()
    if(we_love_avi): print("int : " + str(pulp.value(lp_prob_int.objective)))
    if(we_love_avi): print(lp_prob_int)
    custom_e11 = time.clock() - custom_s11
        
    custom_s12 = time.clock()
    output = '['
    if pulp.LpStatus[lp_prob_int.status] != "Optimal":
        print("error the problem is: " + pulp.LpStatus[lp_prob_int.status])
    else:
        res = lp_prob_int.variables()
        for v in res:
            if(v.varValue == 0 or not valid(v)):
                if(not valid(v)):
                    if(we_love_avi): print("dd - " + v.cat + " " + str(v.name) + " - " + str(v.varValue))
                continue
            else:
                output += '{"shiftid":' + str(get_shift_id_from_var_name(v.name,number_of_shifts,shifts)) + ','
                output += '"employeeid":' + str(get_id_of_employee_from_var_name(v.name,number_of_shifts)) + '},'
                output += "\tvar: " + str(v.name) + " - " + str(v.varValue) + "\n"

    custom_e12 = time.clock() - custom_s12
    #output = output[:-1]
    end_time = time.clock()
    res_time = end_time - start_time
        
    if output:output+='{"time":[{"global_script_time":' + str(res_time) + '},{"custom_e1":' + str(custom_e1) + '},{"custom_e2":' + str(custom_e2) + '},{"custom_e3":' + str(custom_e3) + '},{"custom_e4":' + str(custom_e4) + '},{"custom_e5":' + str(custom_e5) + '},{"custom_e6":' + str(custom_e6) + '},{"custom_e7":' + str(custom_e7) + '},{"custom_e8":' + str(custom_e8) + '},{"custom_e11":' + str(custom_e11) + '},{"custom_e12":' + str(custom_e12) + '}]}]'
        
    return(output)
     
print(solution(employees,games))