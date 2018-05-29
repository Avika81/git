#!/usr/bin/env python
# encoding: utf-8

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

we_love_avi = False
d = False
d_1 = False
debug = False
debug2 = False
debug3 = False

epsilon_1 = 0.01
max_shift_time = 12.0
ideal_shift_time = 3
days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
hours_in_day = 24

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
        self.start = day_to_num(day) * 24 + start
        self.end = day_to_num(day) * 24 + end
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
    def __init__(self, id, name, availability, jobs, max_day = [4,4,4,4,4,4,4], max_week = 20, number_tokens = 10):
        self.id = id
        self.name = name
        self.availability = availability
        self.jobs = jobs
        self.max_day = max_day
        self.max_week = max_week

class Shift:
    id = 0
    # time = Time(0,0,"")
    time = []
    job_id = 0
    number_employees_needed = 1
    priority = 1
    availableEmployees = []
    def __init__(self,id, time, job_id): #availableEmployees):
        self.id = id
        self.time = time
        self.job_id = job_id
        #self.availableEmployees = availableEmployees
        self.number_employees_needed = 1
    def __eq__(self,other):
        return self.time == other.time
    def __lt__(self,other):
        return self.time < other.time


# Shift time in new range format - [0, 168]
# Employee time in new range format - [0, 10, 0] - sunday from 00.00 = 10.00 avaible
# Employee time in new range format - [25, 30, 1] - monday from 01.00 = 05.00 preferred
# jobsid in input be like before list -  [1,23,4] but for now i hardcoded in creating employee cycle
#example = '{"params":{"shifts":[{"id":46124,"time":[166,168],"jobId":4},{"id":46128,"time":[50,53],"jobId":4},{"id":44309,"time":[21.5,24],"jobId":7}],"employees":[{"id":384,"availability":[[0,87,0],[88,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,3,7,8,9,10,11,12,74,75,77]},{"id":110,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,2,7,8,9,10,11,12]},{"id":1501,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,7,8,9,10,11,12,73,74,75]},{"id":70,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,4]},{"id":111,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,3,7,8,9,10,11,12,74,77]},{"id":89,"availability":[[24,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,2,3,4,5,7,8,9,10,11,12,74,75,77]},{"id":1340,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,3,7,8,9,10,11,12,72,73,77]},{"id":86,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,7,8,9,10,11,12]},{"id":113,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,7,8,9,10,11,12,79]},{"id":107,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,7,8,9,10,11,12,72,73,74,75]},{"id":71,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,3,7,8,9,10,11,12,72,79]},{"id":371,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,3,7,8,9,10,11,12,72,79]},{"id":88,"availability":[[0,33,0],[37,57,0],[58.5,81,0],[85,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,2,3,7,8,9,10,11,12]},{"id":1677,"availability":[[0,6,0],[6,22.5,1],[22.5,61,0],[61,71,1],[71,129,0],[129,131.5,1],[131.5,133,0],[133,143,1],[143,150,0],[150,167,1],[167,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,7,9,11,12]},{"id":90,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,3,7,8,9,10,11,12,73]},{"id":104,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,3,7,8,9,10,11,12,74,75]},{"id":101,"availability":[[0,12,0],[22.5,34.5,0],[45.5,60,0],[66.5,82,0],[93.5,108,0],[114.5,129,0],[142,153,0],[164.5,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,7,8,9,10,11,12]},{"id":1767,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,4]},{"id":1496,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,2,3,7,8,9,10,11,12]},{"id":1562,"availability":[[0,32,0],[32,36,1],[36,56,0],[56,60,1],[60,80,0],[80,84,1],[84,104,0],[104,108,1],[108,128,0],[128,132,1],[132,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,4]},{"id":98,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,2,7,8,9,10,11,12]},{"id":361,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,3,7,8,9,10,11,12,72,73,74,75]},{"id":359,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,2,3,7,8,9,10,11,12,72,73,74,75,77]},{"id":1513,"availability":[[0,0,1],[24,32,0],[37.25,56,0],[64.5,80,0],[85,89.25,0],[96,104,0],[109,113.25,0],[144,168,1]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,3,7,8,9,10,11,12,74]},{"id":1507,"availability":[[0,10,0],[13,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,3,7,8,9,10,11,12]},{"id":347,"availability":[[0,89,0],[93.5,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,2,7,8,9,10,11,12,74,75]},{"id":102,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,2,3,7,8,9,10,11,12,74,75,77]},{"id":366,"availability":[[0,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,2,3,7,8,9,10,11,12,72,73,74]},{"id":73,"availability":[[0,33,0],[33.92,59,0],[60.5,81,0],[81.92,107,0],[108.5,129,0],[129.92,168,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,2,7,8,9,10,11,12]},{"id":1561,"availability":[[0,0.5,0],[0.5,3.5,1],[10,36,0],[36,41,1],[41,144,0]],"maxDayTime":[12,12,12,12,12,12,12],"maxWeekTime":"30","jobIds":[1,4]}]}}'
example = '{"params":{"shifts":[{"id":1,"time":[80,84],"jobId":84},{"id":2,"time":[84,88],"jobId":84},{"id":3,"time":[113.5,117.5],"jobId":84},{"id":4,"time":[109.5,113.5],"jobId":84},{"id":5,"time":[62.5,64.5],"jobId":84},{"id":6,"time":[60.5,62.5],"jobId":84},{"id":46281,"time":[64.5,66.5],"jobId":84},{"id":7,"time":[66.5,68.5],"jobId":84},{"id":8,"time":[68.5,70.5],"jobId":84},{"id":9,"time":[70.5,72],"jobId":84}],"employees":[{"id":1,"availability":[[59.5,127.5,0],[131.5,152,0],[162.5,168,0]],"maxDayTime":[4,4,4,4,4,4,4],"maxWeekTime":"20","jobIds":[13,14,15,16,17,64,65,83,84]},{"id":2,"availability":[[0,32,0],[35.5,58,0],[61,80,0],[83.5,106,0],[109,128,0],[131.5,168,0]],"maxDayTime":[4,4,4,4,4,4,4],"maxWeekTime":"20","jobIds":[13,14,15,16,17,64,65,83,84]}]}}'
data = json.loads(example) 
days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
#print(data)
shifts=[];
#setup shifts from data
for sh in range(len(data['params']['shifts'])): 
    shifts.append(Shift(data['params']['shifts'][sh]['id'], data['params']['shifts'][sh]['time'], data['params']['shifts'][sh]['jobId']))

#setup employees from data
employees=[]
for emp in range(len(data['params']['employees'])): 
    #tempavailability=[]
    
    #for index in range(len(data['params']['employees'][emp]['availability'])): 
        #tempavailability.append(Time(data['params']['employees'][emp]['availability'][index][0],data['params']['employees'][emp]['availability'][index][1],data['params']['employees'][emp]['availability'][index][2]))
                     #id,                                              name,          availability,    jobs, max_day,                                        max_week = 20
    employees.append(Employee(data['params']['employees'][emp]['id'], 'EmployeeName', data['params']['employees'][emp]['availability'], data['params']['employees'][emp]['jobIds'], data['params']['employees'][emp]['maxDayTime'], int(data['params']['employees'][emp]['maxWeekTime'])))

def time_in_week(t):  # TODO: change if there is more than one week
    return(t.end - t.start)

def get_start_day(t):
    r = int(t.start / 24)
    return r

def get_end_day(t):
    r = int(t.end / 24)
    return r

def time_in_day(t,d):   # d is day_num, t is time, returns how much time is in this day.
    # print("start: " + str(t.start) + "end: " + str(t.end))
    start_h = t.start - d * hours_in_day
    if(get_end_day(t) > d):  # the next day
        res = hours_in_day - start_h
    else:
        res = t.end - t.start
    return(max(res,0))

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
    #if e.id in s.availableEmployees:
    #    return(True)
    #else:
    #    return(False)
    if(s.job_id not in e.jobs): #in array check employee tru and false
        return(False)
    for t in e.availability:
        if in_time(s.time, t[0]):
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

def get_id_of_employee_from_var_name(name,number_of_shifts):
    str = name[2:]
    var_num = int(str)
    employee = int(int(var_num) / int(number_of_shifts))
    return employees[employee].id

def get_variable_index_from_var_name(name,number_of_shifts):
    str = name[2:]
    return int(str)

def normalize_pref(employees,shifts):
    for s in shifts:
        t = Time(s.time[0],s.time[1])
        s.time = t

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

normalize_pref(employees,shifts) #change to the format I like :)
# shifts.sort()

if(d_1): 
    for s in range(len(shifts)):
      print(str(s) + " :  " + str(total_time(shifts[s].time)) + "day :" + str(get_start_day(shifts[s].time)))   

if(d_1): 
    for s in shifts:
      print(s.time)

number_of_employees = len(employees)
number_of_shifts = len(shifts)

number_variables = number_of_shifts * number_of_employees 

variables_cont = pulp.LpVariable.dicts("x",range(number_variables),   0, 1,cat="Continuous")
lp_prob_cont = pulp.LpProblem("schedule", pulp.LpMaximize)

variables_int = pulp.LpVariable.dicts("y",range(number_variables),   0, 1,cat="Integer")
lp_prob_int = pulp.LpProblem("schedule_int", pulp.LpMaximize)
# variables are : 0 - shifts-1 those for employee1, and so on.  to get xij, do
# i * number_of_shifts)+j

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
        nc_int.append((variables_int[get_index(e,s,number_of_shifts)],time_in_week(shifts[s].time)))
        nc_cont.append((variables_cont[get_index(e,s,number_of_shifts)],time_in_week(shifts[s].time)))
    lp_prob_int += pulp.LpAffineExpression(nc_int) <= employees[e].max_week
    lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= employees[e].max_week

#day constraints:
for e in range(number_of_employees):
    for d in range(len(days)):
        nc_int = []
        nc_cont = []

        for s in range(number_of_shifts):
            if(get_start_day(shifts[s].time) == day_to_num(days[d])): 
                nc_int.append((variables_int[get_index(e,s,number_of_shifts)],time_in_day(shifts[s].time,d)))
                nc_cont.append((variables_cont[get_index(e,s,number_of_shifts)],time_in_day(shifts[s].time,d)))        
        if(debug) : print("employee: " + str(employees[e].id) + "nc_int :" + str(pulp.LpAffineExpression(nc_int)))
        lp_prob_int += pulp.LpAffineExpression(nc_int) <= employees[e].max_day[d]
        lp_prob_cont += pulp.LpAffineExpression(nc_cont) <= employees[e].max_day[d]

# each man is only in one place .
for d in days:  # the shifts should be on 5 mins break.
        for h_12 in range(hours_in_day * 12):
            t = tTime(d,h_12/12,(h_12 + 1)/12)
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

c_int = []
c_cont = []

for e in range(number_of_employees):
    for s in range(number_of_shifts):
        bonus = np.random.uniform(epsilon_1,2*epsilon_1)
        c_int.append((variables_int[get_index(e,s,number_of_shifts)],shifts[s].priority + bonus))
        c_cont.append((variables_cont[get_index(e,s,number_of_shifts)],shifts[s].priority + bonus))

lp_prob_int += pulp.LpAffineExpression(c_int) , "total_res_cont"
lp_prob_cont += pulp.LpAffineExpression(c_cont) , "total_res_int"

lp_prob_cont.solve()

if pulp.LpStatus[lp_prob_cont.status] != "Optimal":
    print("error the problem is: " + pulp.LpStatus[lp_prob_cont.status])

else:
    res = lp_prob_cont.variables()
    for v in res:
        if(debug3):
            if(v.varValue != 1 and v.varValue != 0):
                print("{} = {}".format(v.name, v.varValue))
        if(v.varValue == 1):
            ne = []
            index = get_variable_index_from_var_name(v.name,number_of_shifts)
            ne.append((variables_int[index],1))
            lp_prob_int += pulp.LpAffineExpression(ne) == 1 # we know it's value for sure. (1)
        if(v.varValue == 0):
            ne = []
            index = get_variable_index_from_var_name(v.name,number_of_shifts)
            ne.append((variables_int[index],1))
            lp_prob_int += pulp.LpAffineExpression(ne) == 0 # we know it's value for sure. (0)
        
cont_res = pulp.value(lp_prob_cont.objective)  # TODO : if the algorithm has too many errors add constraints to get more linear result in continous prob.
if(we_love_avi): print("cont : " + str(pulp.value(lp_prob_cont.objective)))

lp_prob_int.solve()

if(we_love_avi): print("int  : " + str(pulp.value(lp_prob_int.objective)))

output='['
if pulp.LpStatus[lp_prob_int.status] != "Optimal":
    print("error the problem is: " + pulp.LpStatus[lp_prob_int.status])
else:
    res = lp_prob_int.variables()
    if(debug):
        for i in range(len(res)):
            print("{} = {}".format(lp_prob_int.variables()[i].name, lp_prob_int.variables()[i].varValue))
    for v in res:
        if(v.varValue == 0):
            continue
        else:
            output += '{"shiftid":' + str(get_shift_id_from_var_name(v.name,number_of_shifts,shifts)) + ','
            output += '"employeeid":' + str(get_id_of_employee_from_var_name(v.name,number_of_shifts)) + '},'
            # if(d) : output += "\n"
            if(debug) : output += "\tvar: " + str(v.name) +"-"+ str(v.varValue)

output = output[:-1] 
if output:output+=']'            
print(output)