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
yet_count_as_continous = 1  # the legnth of maximal break

days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
    
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
    def __init__(self, start, end, day=""):
        self.start = day_to_num(day) * 24 + start
        self.end = day_to_num(day) * 24 + end
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
    def __init__(self, id, name, availability, jobs, max_day=[4,4,4,4,4,4,4], max_week=20):
        self.id = id
        self.name = name
        self.availability = availability
        self.jobs = jobs
        self.max_day = max_day
        self.max_week = max_week

def __repr__(self):
    return "<__main__.Employee: id = " + str(self.id) + "; name = " + str(self.name) + ";>"

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

    #like server loads json string
datas = '{"params":{"shifts":[{"id":46062,"time":["Sun",10,13],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46063,"time":["Sun",13,16],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46064,"time":["Sun",16,20],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46065,"time":["Sun",20,23.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46080,"time":["Sun",10,13.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46081,"time":["Sun",13.5,17],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46082,"time":["Sun",17,20.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46083,"time":["Sun",20.5,23.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46066,"time":["Mon",17,20.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46067,"time":["Mon",20.5,23.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46084,"time":["Mon",6,9],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46089,"time":["Mon",9,12],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46094,"time":["Mon",12,15],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46099,"time":["Mon",15,18],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46104,"time":["Mon",18,21],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46109,"time":["Mon",21,23.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46068,"time":["Tue",20.5,23.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46071,"time":["Tue",17,20.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46085,"time":["Tue",6,9],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46090,"time":["Tue",9,12],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46095,"time":["Tue",12,15],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46100,"time":["Tue",15,18],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46105,"time":["Tue",18,21],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46110,"time":["Tue",21,23.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46069,"time":["Wed",20.5,23.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46072,"time":["Wed",17,20.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46086,"time":["Wed",6,9],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46091,"time":["Wed",9,12],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46096,"time":["Wed",12,15],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46101,"time":["Wed",15,18],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46106,"time":["Wed",18,21],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46111,"time":["Wed",21,23.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46070,"time":["Thu",20.5,23.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46073,"time":["Thu",17,20.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46087,"time":["Thu",6,9],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46092,"time":["Thu",9,12],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46097,"time":["Thu",12,15],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46102,"time":["Thu",15,18],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46107,"time":["Thu",18,21],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46112,"time":["Thu",21,23.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46074,"time":["Fri",17,20.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46075,"time":["Fri",20.5,23.5],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46088,"time":["Fri",6,9],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46093,"time":["Fri",9,12],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46098,"time":["Fri",12,15],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46103,"time":["Fri",15,18],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46108,"time":["Fri",18,21],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46113,"time":["Fri",21,23.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46076,"time":["Sat",10,13],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46077,"time":["Sat",13,16],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46078,"time":["Sat",16,19],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46079,"time":["Sat",19,22],"jobId":17,"availableEmployees":[126,141,143,146,148,152,160,163,166,170,178,182,186,358,739,1341]},{"id":46114,"time":["Sat",10,13.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46115,"time":["Sat",13.5,17],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46116,"time":["Sat",17,20.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]},{"id":46117,"time":["Sat",20.5,23.5],"jobId":16,"availableEmployees":[117,126,134,137,141,143,146,148,152,160,163,166,167,170,178,180,182,184,186,358,739,1297,1341,1472,1475,1476,1570,1652,1669]}],"employees":[{"id":126,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":141,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":143,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":146,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":148,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":152,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":160,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":163,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":166,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":170,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":178,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":182,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":186,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":358,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":739,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":1341,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":117,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":134,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":137,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":167,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":180,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":184,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":1297,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":1472,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":1475,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":1476,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":1570,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":1652,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20},{"id":1669,"availability":[["Sun",0,24],["Mon",0,24],["Tue",0,24],["Wed",0,24],["Thu",0,24],["Fri",0,24],["Sat",0,24]],"maxDayTime":[24,24,24,24,24,24,24],"maxWeekTime":20}]}}'
data = json.loads(datas) 
shifts=[];
#setup shifts from data
for sh in range(len(data['params']['shifts'])): 
    shifts.append(Shift(data['params']['shifts'][sh]['id'], Time(data['params']['shifts'][sh]['time'][0],data['params']['shifts'][sh]['time'][1],data['params']['shifts'][sh]['time'][2]), data['params']['shifts'][sh]['jobId'], data['params']['shifts'][sh]['availableEmployees']))

#setup employees from data
employees=[]
for emp in range(len(data['params']['employees'])): 
    tempavailability=[]
    
    for index in range(len(data['params']['employees'][emp]['availability'])): 
        tempavailability.append(Time(data['params']['employees'][emp]['availability'][index][0],data['params']['employees'][emp]['availability'][index][1],data['params']['employees'][emp]['availability'][index][2]))
#id,                                              name,          availability,    jobs, max_day,                                        max_week = 20
    employees.append(Employee(data['params']['employees'][emp]['id'], 'EmployeeName', tempavailability, [], data['params']['employees'][emp]['maxDayTime'], int(data['params']['employees'][emp]['maxWeekTime'])))

'''
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
""" test 1: BB """
shifts = [Shift(0,tTime("Sun",12,13),1),
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
Shift(28,tTime("Thu",22,23),1)]

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
'''




def time_in_day(t,d):
    d_int = day_to_num(d)
    start_h = t.start - d_int * hours_in_day
    if(get_end_day(t) > d_int):  # the next day
        res = hours_in_day - start_h
    else:
        res = t.end - t.start
    return(max(res,0))

def time_in_week(t):  # TODO: change if there is more than one week
    return(t.end - t.start)

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

def get_index(employee,shift,number_of_shifts):
    return(employee * number_of_shifts + shift)

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

#create preferred shifts:
shifts.sort()
number_of_employees = len(employees)
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
            if(get_start_day(shifts[s].time) == day_to_num(days[d]) or get_end_day(shifts[s].time) == day_to_num(days[d])):  # TODO : make it work for half a shift of time (the shift may continue to
                                                                                                                             # next day)
                nc_int.append((variables_int[get_index(e,s,number_of_shifts)],time_in_day(shifts[s].time,days[d])))
                nc_cont.append((variables_cont[get_index(e,s,number_of_shifts)],time_in_day(shifts[s].time,days[d])))        
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
            if(debug_var) : output += "\tvar: " + str(v.name) + "-" + str(v.varValue)
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

