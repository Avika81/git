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

debug = False
debug2 = False
epsilon = 0.01
max_shift_time = 12.0
ideal_shift_time = 3
days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

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
    availableEmployees = []
    def __init__(self,id, time, job_id, availableEmployees):
        self.id = id
        self.time = time
        self.job_id = job_id
        self.availableEmployees = availableEmployees
        self.number_employees_needed = 1
    def __eq__(self,other):
        return self.time == other.time
    def __lt__(self,other):
        return self.time < other.time


from settings import settings


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        logging.info('get')
        self.write('ssssssss')
        self.write(self.request.body)

    def post(self):
        logging.info('post')
        data = json.loads(self.request.body) 
        days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

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
            if e.id in s.availableEmployees:
                return(True)
            else:
                return(False)
            #if(s.job_id not in e.jobs): #in array check employee tru and false
            #    return(False)
            #for t in e.availability:
            #    if in_time(s.time, t):
            #        return(True)
            #return(False)

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

        def get_id_of_employee_from_var_name(name,number_of_shifts):
            str = name[2:]
            var_num = int(str)
            employee = var_num % number_of_shifts
            return employees[employee].id

        #employees = [Employee(33,"Employee1",[ Time("Sun",0,24), Time("Mon",0,24), Time("Tue",0,24), Time("Wed",0,24), Time("Thu",0,24)], [1,2,3,4]),
        #Employee(12,"Employee33",[ Time("Sun",0,24), Time("Mon",0,24), Time("Tue",0,24), Time("Wed",0,24), Time("Thu",0,24)], [1,2,3,4])]

        #shifts = [Shift(0,Time("Sun",8,10),1),
        #Shift(1,Time("Sun",8,10),1), #same is easy here **
        #Shift(2,Time("Sun",11,13),1),
        #Shift(3,Time("Sun",8,10),2),
        #Shift(4,Time("Sun",8,10),3),
        #Shift(5,Time("Sun",11,13),4),
        #Shift(6,Time("Mon",8,10),1),
        #Shift(7,Time("Tue",8,10),1),
        #Shift(8,Time("Tue",11,13),1),
        #Shift(9,Time("Wed",8,10),2),
        #Shift(10,Time("Thu",8,10),3),
        #Shift(11,Time("Thu",11,13),4)]
        
        number_of_employees = len(employees)
        number_of_shifts = len(shifts)

        number_variables = number_of_shifts * number_of_employees 

        variables = pulp.LpVariable.dicts("x",range(number_variables), 0, 1, cat = 'Integer') #create integer values of 0 or one for the employment of employee in a shift
        lp_prob = pulp.LpProblem("schedule", pulp.LpMaximize)

        # variables are : 0 - shifts-1 those for employee1, and so on.  to get xij, do
        # i * number_of_shifts)+j


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
        output='['
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
                    output += '{"shiftid":' + str(get_shift_id_from_var_name(v.name,number_of_shifts,shifts)) + ','
                    output += '"employeeid":' + str(get_id_of_employee_from_var_name(v.name,number_of_shifts)) + '},'
                    if(debug) : output += "\tvar: " + str(v.name) +"-"+ str(v.varValue)

        output = output[:-1] 
        if output:output+=']'            
        self.write(output)

url_patterns = [
    (r"/", MainHandler),
]

class MainApplication(tornado.web.Application):

    def __init__(self):
        logging.info("init MainApplication with settings: %s and %s" % (str(settings),url_patterns))
        tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
    parse_command_line()
    if options.config:
        parse_config_file(options.config)
    app = MainApplication()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
