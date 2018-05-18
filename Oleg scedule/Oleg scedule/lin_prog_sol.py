""" the linprog.py solution: """
#Ax<=b,max <c,x>
A = []
b = []  
c = []
eq_left = []
eq_right = []


number_variables = number_of_shifts * number_of_employees 
# variables are : 0 - shifts-1 those for employee1, and so on.  to get xij, do
# i * number_of_shifts)+j

#preffered with preffered intersection:
for s1 in range(old_number_of_shifts,number_of_shifts):
    l_collisions = []
    for s2 in range(old_number_of_shifts,number_of_shifts):
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

# preffered shifts with the regular shift intersection:
for new_eq in preffered_eq:
    eq = np.zeros(number_variables)
    for i in range(new_eq[1]):
        eq[new_eq[0]+i] = 1
    eq[new_eq[2]] = 1
    A.append(eq)
    b.append(1)
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
        print('shift ' + str(shifts[s].id))
        for e in range(number_of_employees):
            if sol[get_index(e,s,number_of_shifts)] > 1 - 1/max_shift_time:
                l.append(employees[e])
            output = ""
            for e in l:
                output += str(e.name) + "," 
        print("employees: " + output)
