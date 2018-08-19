import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import options, parse_command_line, parse_config_file
import logging
import json

# from pylinprogmaster import linprog
import numpy as np
import random
import pulp
import time

we_love_avi = False
epsilon_1 = 0.01
smallest_break_possible = 0
days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
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
    employee_ids = []
    number_employees_needed = 1
    priority = 1
    availableEmployees = []
    def is_eq(self,other):
        return (self.time.start == self.time.start and self.time.end == self.time.end)
    def __init__(self,id, time, job_id, employee_ids, number_employees_needed=1, priority=1):
        self.id = id
        self.time = time
        self.job_id = job_id
        self.employee_ids = employee_ids
        self.number_employees_needed = 1
    def __eq__(self,other):
        return self.time == other.time
    def __lt__(self,other):
        return self.time < other.time

# (my cute test) Working :)
example  = '{"params":{"shifts":[{"id":0,"time":[3,6],"jobId":1},{"id":1,"time":[6,9],"jobId":1},{"id":2,"time":[9,12],"jobId":1},{"id":3,"time":[100,102],"jobId":2},{"id":4,"time":[140,142],"jobId":2}],"employees":[{"id":0,"availability":[[0,1000,0]],"maxDayTime":[4,4,4,4,4,4,4],"maxWeekTime":"20","jobIds":[1,2,3]},{"id":1,"availability":[[0,1000,0]],"maxDayTime":[4,4,4,4,4,4,4],"maxWeekTime":"20","jobIds":[1,2,3]},{"id":2,"availability":[[0,1000,0]],"maxDayTime":[4,4,4,4,4,4,4],"maxWeekTime":"20","jobIds":[1,2,3]},{"id":3,"availability":[[0,1000,0]],"maxDayTime":[4,4,4,4,4,4,4],"maxWeekTime":"20","jobIds":[1,2,3]}]}}'
#    (a lot of shifts and employees) Working :)
# example = '{"params":{"shifts":[{"id":46062,"time":[10,13],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46063,"time":[13,16],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739]},{"id":46064,"time":[16,20],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739]},{"id":46065,"time":[20,24],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46066,"time":[41,44.5],"jobId":17,"employee_ids":[126,141,143,146,148,152,163,166,170,178,182,186,358,739,1341]},{"id":46067,"time":[44.5,47.98],"jobId":17,"employee_ids":[141,143,146,148,152,163,166,170,178,182,186,358,739,1341]},{"id":46068,"time":[68.5,71.5],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,358,739,1341]},{"id":46069,"time":[92.5,95.5],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,186,358,739]},{"id":46070,"time":[116.5,119.5],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46071,"time":[65,68.5],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,358,739]},{"id":46072,"time":[89,92.5],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,178,186,358,739,1341]},{"id":46073,"time":[113,116.5],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,166,170,178,182,186,358,739,1341]},{"id":46074,"time":[137,140.5],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,186,358,739,1341]},{"id":46075,"time":[140.5,143.5],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,186,358,739,1341]},{"id":46076,"time":[154,157],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46077,"time":[157,160],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739]},{"id":46078,"time":[160,163],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739]},{"id":46079,"time":[163,166],"jobId":17,"employee_ids":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,1341]},{"id":46080,"time":[10,13.5],"jobId":16,"employee_ids":[117,126,134,137,141,143,148,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46081,"time":[13.5,17],"jobId":16,"employee_ids":[117,126,134,137,141,143,148,152,160,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46082,"time":[17,20.5],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46083,"time":[20.5,24],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46084,"time":[30,33],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46085,"time":[54,57],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46086,"time":[78,81],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46087,"time":[102,105],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46088,"time":[126,129],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46089,"time":[33,36],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46090,"time":[57,60],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46091,"time":[81,84],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46092,"time":[105,108],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46093,"time":[129,132],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46094,"time":[36,39],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46095,"time":[60,63],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46096,"time":[84,87],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46097,"time":[108,111],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46098,"time":[132,135],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46099,"time":[39,42],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46100,"time":[63,66],"jobId":16,"employee_ids":[117,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46101,"time":[87,90],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46102,"time":[111,114],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1472,1475,1476,1570,1652,1669]},{"id":46103,"time":[135,138],"jobId":16,"employee_ids":[117,126,134,137,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46104,"time":[42,45],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46105,"time":[66,69],"jobId":16,"employee_ids":[117,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46106,"time":[90,93],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46107,"time":[114,117],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,160,163,166,167,170,178,180,182,184,186,358,739,1297,1472,1475,1476,1570,1652,1669]},{"id":46108,"time":[138,141],"jobId":16,"employee_ids":[117,134,137,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46109,"time":[45,48],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46110,"time":[69,71.5],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46111,"time":[93,95.5],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46112,"time":[117,119.5],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46113,"time":[141,143.5],"jobId":16,"employee_ids":[117,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46114,"time":[154,157.5],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46115,"time":[157.5,161],"jobId":16,"employee_ids":[117,126,134,137,141,146,148,152,160,163,166,167,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46116,"time":[161,164.5],"jobId":16,"employee_ids":[117,126,134,137,141,146,148,152,160,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46117,"time":[164.5,167.5],"jobId":16,"employee_ids":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]}],"employees":[{"id":126,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":141,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":143,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":146,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":148,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":152,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":160,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":163,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":166,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":170,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":178,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":182,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":186,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":358,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,20,24],"maxWeekTime":36,"jobIds":[]},{"id":739,"availability":[[0,168,0]],"maxDayTime":[24,24,24,20.5,24,24,24],"maxWeekTime":36.5,"jobIds":[]},{"id":1341,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":117,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":134,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":137,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":167,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":180,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":184,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":1297,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":1472,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":1475,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":1476,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":1570,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":1652,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]},{"id":1669,"availability":[[0,168,0]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":40,"jobIds":[]}],"interval_between_shifts":0}}'

data = json.loads(example)
days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

shifts = []
#setup shifts from data
for sh in range(len(data['params']['shifts'])):
    shifts.append(Shift(data['params']['shifts'][sh]['id'], data['params']['shifts'][sh]['time'], data['params']['shifts'][sh]['jobId'], data['params']['shifts'][sh]['employee_ids']))

#setup employees from data
employees = []
for emp in range(len(data['params']['employees'])):
                #id, name, availability, jobs, max_day, max_week = 20
    employees.append(Employee(data['params']['employees'][emp]['id'], 'EmployeeName', data['params']['employees'][emp]['availability'], data['params']['employees'][emp]['jobIds'], data['params']['employees'][emp]['maxDayTime'], int(data['params']['employees'][emp]['maxWeekTime'])))


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
    """check the sizr of the intersection of a shift and a day"""
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
    #if(s.job_id not in e.jobs): #in array check employee tru and false
    #    return(False)
    #print(s.employee_ids)
    if(e.id not in s.employee_ids):
        return(False)
    for t in e.availability:
        if in_time(s.time, t[0]):
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

def normalize_pref(employees,shifts):
    """
    functio that move all the input from the json format (in lists) to my classes.
    also changes the prefs to make it in a good format (spreading the tokens accordingly).
    """
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

def solution(employees,shifts):
    time_init = time.clock() - start_time
    custom_s1 = time.clock()
    normalize_pref(employees,shifts)
    custom_e1 = time.clock() - custom_s1

    number_of_employees = len(employees)
    number_of_shifts = len(shifts)

    number_variables = number_of_shifts * number_of_employees

    custom_s2 = time.clock()

    # lp_prob_cont = pulp.LpProblem("schedule", pulp.LpMaximize)  # creating the Lp problem

    variables_int = pulp.LpVariable.dicts("y",range(number_variables),   0, 1,cat="Binary")  # the variables
    lp_prob_int = pulp.LpProblem("schedule_int", pulp.LpMaximize)
    # variables are : 0 - shifts-1 those for employee1, and so on.  to
    # get x_ij, do
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
            lp_prob_int += pulp.LpAffineExpression(nc_int) <= employees[e].max_day[d]

    custom_e5 = time.clock() - custom_s5
    custom_s6 = time.clock()

    #check that each employee is only in one place at a time [changed**
    #, can't work in diff of smallest_break_possible hours]
    # shifts_end = list(shifts)
    # shifts_end.sort(key=get_end_time)
    big_const = max(number_of_shifts,100)
    for s in np.arange(number_of_shifts):
        t = Time(shifts[s].time.start - smallest_break_possible, shifts[s].time.end + smallest_break_possible)
        # want to receive the indeces of those who intersects with s.
        l = np.zeros(number_of_shifts)
        for s2 in np.arange(number_of_shifts):
            if (collision(t,shifts[s2].time)):
                l[s2] = 1
        if(len(l) <= 0) : continue  # there is 0 or one shift in this time so there is no problem
        for e in np.arange(number_of_employees):
            nc_int = []
            nc_int.append((variables_int[get_index(e,s,number_of_shifts)],big_const))
            for s3 in np.arange(number_of_shifts):
                if l[s] == 1:
                    nc_int.append((variables_int[get_index(e,s3,number_of_shifts)],1))
            lp_prob_int += pulp.LpAffineExpression(nc_int) <= big_const

    custom_e6 = time.clock() - custom_s6

    c_int = []

    custom_s7 = time.clock()
    for e in range(number_of_employees):
        for s in range(number_of_shifts):
            bonus = np.random.uniform(epsilon_1 * shifts[s].priority,2 * epsilon_1 * shifts[s].priority)
            c_int.append((variables_int[get_index(e,s,number_of_shifts)], 1 + bonus))

    custom_e7 = time.clock() - custom_s7

    # soft constraints: !!!!  (they wouldn't surely be happening but
    # there is a fine if they won't
    # (and the algorithm will try to avoid it but not at any cost) [the
    # bigger the fine the mroe important it is]
    # once a week:
    """
    for e in range(number_of_employees):
        nc_int = []
        for s in range(number_of_shifts):
            nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
            ll = "week_-_" + str(e) # the starting name
        v1 = pulp.LpVariable(name = ll + "elastic_neg", upBound=0)
        nc_int.append((v1,1))  # if the value is big it gives more space
        lp_prob_int += pulp.LpAffineExpression(nc_int) <= 1

        c_int.append((v1,0.2))  # the fine is 0.2.
    """

    # once a day:
    for e in range(number_of_employees):
        for d in range(len(days)):
            nc_int = []

            for s in range(number_of_shifts):
                if(get_start_day(shifts[s].time) == day_to_num(days[d])):
                    nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
                    # CONT_SOL :
                    # nc_cont.append((variables_cont[get_index(e,s,number_of_shifts)],time_in_day(shifts[s].time,d)))
            ll = str(e) + " day - " + str(d)
            v1 = pulp.LpVariable(name = ll + "elastic_neg", upBound=0)
            nc_int.append((v1,1))  # if the value is big it gives more space
            lp_prob_int += pulp.LpAffineExpression(nc_int) <= 1

            c_int.append((v1,0.5))  # the fine is 0.5.


    #everyone works atleast once a week:
    """
    for e in range(number_of_employees):
        nc_int = []
        for s in range(number_of_shifts):
            nc_int.append((variables_int[get_index(e,s,number_of_shifts)],1))
        ll = "love_to_work_-_" + str(e) # the starting name
        v1 = pulp.LpVariable(name = ll + "elastic_pos", lowBound = 0,upBound = number_of_shifts,cat = "Continuous")

        nc_int.append((v1,1))  # if the value is big it gives more space
        lp_prob_int += pulp.LpAffineExpression(nc_int) >= 1

        c_int.append((v1,-0.8))  # the fine is 0.8.
    """
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
                if(we_love_avi) : output += "\tvar: " + str(v.name) + " - " + str(v.varValue) + "\n"

    custom_e12 = time.clock() - custom_s12
    #output = output[:-1]
    end_time = time.clock()
    res_time = end_time - start_time

    # if output:output+='{"time":[{"global_script_time":' + str(res_time) + '},{"custom_e1":' + str(custom_e1) + '},{"custom_e2":' + str(custom_e2) + '},{"custom_e3":' + str(custom_e3) + '},{"custom_e4":' + str(custom_e4) + '},{"custom_e5":' + str(custom_e5) + '},{"custom_e6":' + str(custom_e6) + '},{"custom_e7":' + str(custom_e7) + '},{"custom_e8":' + str(custom_e8) + '},{"custom_e11":' + str(custom_e11) + '},{"custom_e12":' + str(custom_e12) + '}]}]'
    return(output)

print(solution(employees,shifts))
