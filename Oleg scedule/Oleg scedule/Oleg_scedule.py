from pylinprogmaster import linprog
import numpy as np

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
    max_day = [4,4,4,4,4,4,4]
    max_week = 6
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

employees = [Employee(1,"Employee1",
[Time("Sun",8,12),
Time("Sun",14,18),
Time("Mon",8,12),
Time("Sun",14,18),
Time("Tue",6,23)],
[1,2,3,4]),
Employee(2,"Employee2",
[Time("Wed",8,12),
Time("Thu",14,18),
Time("Fri",6,23)],
[1,2,3]),

Employee(3,"Employee3",
[Time("Wed",8,12),
Time("Thu",14,18),
Time("Sat",6,23)],
[1])]

shifts = [Shift(0,Time("Sun",8,10),1),
Shift(1,Time("Sun",8,10),1), #same is easy here **
Shift(2,Time("Sun",11,13),1),
Shift(3,Time("Sun",8,10),2),
Shift(4,Time("Sun",8,10),3),
Shift(5,Time("Sun",11,13),4),
Shift(6,Time("Mon",8,10),1),
Shift(7,Time("Tue",8,10),1),
Shift(8,Time("Tue",11,13),1),
Shift(9,Time("Wen",8,10),2),
Shift(10,Time("Fri",8,10),3),
Shift(11,Time("Fri",11,13),4)]

number_of_employees = len(employees)
number_of_shifts = len(shifts)

def in_time(x,y):  # check if x is in y
    if(x.day!=y.day):
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

#Ax<=b,max <c,x>
A = []
b = []  
c = []
eq_right = []
eq_left = []

number_variables = number_of_shifts * number_of_employees 
# variables are : 0 - shifts-1 those for employee1, and so on.  to get xij, do
# i*number_of_shifts)+j

#shifts constraints:
shift_num = -1
for s in range(number_of_shifts):
    shift_num += 1
    new_line = np.zeros(number_variables).tolist()
    for e in range(number_of_employees):
        if(could_do_this_job(shifts[s], employees[e])):  # the employee can do it?
            new_line[e * number_of_shifts + s] = 1 # he is only one employee
            A.append(new_line)
            b.append(shifts[s].number_employees_needed) 

        else:  # should kill this variable: (so adding the constaint of xij==0
            nl = np.zeros(number_variables).tolist()
            nl[e * number_of_shifts + s] = 1
            eq_left.append(nl)
            eq_right.append(0)

#week constraints:
for e in range(number_of_employees):
    new_line = np.zeros(number_variables).tolist()
    for s in range(number_of_shifts):
        new_line[e * number_of_shifts + s] = total_time(shifts[s].time)  # the length of this shift
    A.append(new_line)
    b.append(employees[e].max_week)

#day constaints
for e in range(number_of_employees):
    for d in range(len(days)):
        new_line = np.zeros(number_variables).tolist()
        for s in range(number_of_shifts):
            if(shifts[s].time.day == days[d]):
                new_line[e * number_of_shifts + s] = total_time(shifts[s].time)
        A.append(new_line)
        b.append(employees[e].max_day[d])

#check that each employee is only in one place at a time
for e in range(number_of_employees):
    for d in range(len(days)):
        for h in range(0,24):
            new_line = np.zeros(number_variables).tolist()
            for s in range(number_of_shifts):
                t = Time(days[d],s,s+1)
                if(in_time(t,shifts[s].time)):
                    new_line[e * number_of_shifts + s] = 1
            A.append(new_line)
            b.append(1)
             


c = np.zeros(number_variables).tolist()
for i in range(number_variables):
    c[i] = -1

resolution,sol = linprog.linsolve(c,A,b,eq_left,eq_right,range(number_variables))

if resolution!= "solved":
    print(resolution)
else:
    for s in range(number_of_shifts):
        l = []
        print('shift' + str(shifts[s].id))
        for e in range(number_of_employees):
            if sol[e*number_of_shifts + s] > 1/2:
                l.append(employees[e])
            output = ""
            for e in l:
                output += str(e.id) + "," 
        print("employees: " + output) 
        
