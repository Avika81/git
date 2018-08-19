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
        # setup shifts from data
        for sh in range(len(data['params']['shifts'])): 
            shifts.append(Shift(data['params']['shifts'][sh]['id'], Time(data['params']['shifts'][sh]['time'][0],data['params']['shifts'][sh]['time'][1],data['params']['shifts'][sh]['time'][2]), data['params']['shifts'][sh]['jobId'], data['params']['shifts'][sh]['availableEmployees']))

        # setup employees from data
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
            employee = int(int(var_num) / int(number_of_shifts))
            return employees[employee].id
        
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
                

        cont_res = print("cont : " + str(pulp.value(lp_prob_cont.objective)))

        lp_prob_int.solve()
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
