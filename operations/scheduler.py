'''----------------------------------------------------------------------------
                    Matthew Bowyer Account Generator
----------------------------------------------------------------------------'''
from django.contrib.auth.models import User
from operations.models import *
from infrastructure.models import *
import random
import numpy as np
import csv
import datetime


class UserTester():
    first_names = [
        'Emma', 'Noah', 'Olivia', 'Liam', 'Sophia', 'Mason', 'Ava	Jacob',
        'Isabella', 'William', 'Mia', 'Ethan', 'Abigail', 'James', 'Emily',
        'Alexander', 'Charlotte', 'Michael', 'Harper', 'Benjamin', 'Madison',
        'Elijah', 'Amelia', 'Daniel', 'Elizabeth', 'Aiden', 'Sofia', 'Logan',
        'Evelyn', 'Matthew', 'Avery', 'Lucas', 'Chloe', 'Jackson', 'Ella',
        'David', 'Grace', 'Oliver', 'Victoria', 'Jayden', 'Aubrey', 'Joseph',
        'Scarlett', 'Gabriel', 'Zoey', 'Samuel', 'Addison', 'Carter', 'Lily',
        'Anthony', 'Lillian', 'John', 'Natalie', 'Dylan', 'Hannah', 'Luke',
        'Aria', 'Henry', 'Layla', 'Andrew', 'Brooklyn', 'Isaac', 'Alexa',
        'Christopher', 'Zoe', 'Joshua', 'Penelope', 'Wyatt', 'Riley',
        'Sebastian', 'Leah', 'Owen', 'Audrey', 'Caleb', 'Savannah', 'Nathan',
        'Allison', 'Ryan', 'Samantha', 'Jack', 'Nora', 'Hunter', 'Skylar',
        'Levi', 'Camila', 'Christian', 'Anna', 'Jaxon', 'Paisley', 'Julian',
        'Ariana', 'Landon', 'Ellie', 'Grayson', 'Aaliyah', 'Jonathan', 'Claire',
        'Isaiah', 'Violet', 'Charles'
    ]

    last_names = [
        'Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller',
        'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White',
        'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson',
        'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen',
        'Young', 'Hernandez', 'King', 'Wright', 'Lopez', 'Hill', 'Scott',
        'Green', 'Adams', 'Baker', 'Gonzalez', 'Nelson', 'Carter', 'Mitchell',
        'Perez', 'Roberts', 'Turner', 'Phillips', 'Campbell', 'Parker', 'Evans',
        'Edwards', 'Collins', 'Stewart', 'Sanchez', 'Morris', 'Rogers', 'Reed',
        'Cook', 'Morgan', 'Bell', 'Murphy', 'Bailey', 'Rivera', 'Cooper',
        'Richardson', 'Cox', 'Howard', 'Ward', 'Torres', 'Peterson', 'Gray',
        'Ramirez', 'James', 'Watson', 'Brooks', 'Kelly', 'Sanders', 'Price',
        'Bennett', 'Wood', 'Barnes', 'Ross', 'Henderson', 'Coleman', 'Jenkins',
        'Perry', 'Powell', 'Long', 'Patterson', 'Hughes', 'Flores',
        'Washington', 'Butler', 'Simmons', 'Foster', 'Gonzales', 'Bryant',
        'Alexander', 'Russell', 'Griffin', 'Diaz', 'Hayes'
    ]
    def generate_user(self):
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        self.create_user(first_name, last_name)

    def create_user(self,first_name, last_name):
        done = False
        attempt = 1
        while not done:
            try:
                username = (last_name+first_name+str(attempt)).lower()
                password = (first_name+'password').lower()
                user = User.objects.create_user(username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                done = True
                print 'Created User Cridentials => '+username+':'+password
            except IntegrityError as e:
                attempt += 1

    def generate_names(self, num_of_names):
        names = []
        for i in range(num_of_names):
            name = {}
            name['first'] = random.choice(self.first_names)
            name['last'] = random.choice(self.last_names)
            names.append(name)
        return names


    def create_program(self, program_type, program_name, group_capacity, start_date, end_date, guest_names):
        program = Program(
            name=program_name,
            program_type=program_type,
            group_capacity=group_capacity,
            start_date=start_date,
            end_date=end_date
        )
        program.save()
        num_of_groups = (len(guest_names)/group_capacity)+1
        for group_id in range(num_of_groups):
            group = Group(
                program=program,
                number=(group_id+1)
            )
            group.save()
            for name in guest_names[group_id::num_of_groups]:
                guest = Guest(
                    group=group,
                    first_name=name['first'],
                    last_name=name['last']
                )
                guest.save()

    def generate_program(self, program_type, program_name, group_capacity, start_date, end_date, number_of_guests):
        return self.create_program(
            program_type=program_type,
            program_name=program_name,
            group_capacity=group_capacity,
            start_date=start_date,
            end_date=end_date,
            guest_names=self.generate_names(number_of_guests)
        )

'''
from scheduler.generator import *
from operations.models import *
test = UserTester()
test.generate_program(
    program_type=Program.CODE['Youth Program'],
    program_name='My First Program',
    group_capacity=25,
    start_date='2017-01-01',
    end_date='2017-01-02',
    number_of_guests=100
)
'''

def print_structure(structure, depth):
    ret = ""
    if structure is None:
        ret += '\n'
    if isinstance(structure, type('a')):
        ret += ('\t'*depth) + (structure) + ('\n')
    if isinstance(structure, type(1)):
        ret += ('\t'*depth) + (str(structure)) + ('\n')
    if isinstance(structure, type(1.0)):
        ret += ('\t'*depth) + (str(structure)) + ('\n')
    if isinstance(structure, type((1,2))):
        ret += ('\t'*depth) + str(structure[0]) + (": ") + print_structure(structure[1], depth)[depth:]
    if isinstance(structure, type([])):
        ret += ('\t'*depth) + ('[') + ('\n')
        for i in range(0,len(structure)): ret += print_structure((i,structure[i]), depth+1)
        ret = ret[:len(ret)-1] + (']') + ('\n')
    if isinstance(structure, type({})) and len(structure):
        ret += ('\t'*depth) + ('{') + ('\n')
        for (k,v) in structure.iteritems(): ret += print_structure((k,v), depth+1)
        ret = ret[:len(ret)-1] + ('}') + ('\n')
    return ret

def print_struct(structure):
    print print_structure(structure, 0)


def floydwarshall(graph):
    dist = {}
    pred = {}
    for u in graph:
        dist[u] = {}
        pred[u] = {}
        for v in graph:
            dist[u][v] = 1000
            pred[u][v] = -1
        dist[u][u] = 0
        for neighbor in graph[u]:
            dist[u][neighbor] = graph[u][neighbor]
            pred[u][neighbor] = u
    for t in graph:
        for u in graph:
            for v in graph:
                newdist = dist[u][t] + dist[t][v]
                if newdist < dist[u][v]:
                    dist[u][v] = newdist
                    pred[u][v] = pred[t][v]
    return dist


def format_choices(zone_query):
    zones = {}
    graph = {}
    for zone in zone_query:
        name = zone.name.encode('ascii','ignore')
        zones[name] = {'capacity':0,'level':0}
        zones[name]['capacity'] = 0
        zones[name]['level'] = 0
        for activity in zone.activities.all():
            zones[name]['capacity'] += activity.capacity
            zones[name]['level'] += activity.level * activity.capacity
        zones[name]['capacity'] = (1.0*zones[name]['capacity'])
        zones[name]['level'] = (1.0*zones[name]['level'])/zones[name]['capacity']
        graph[name] = {adjacent_zones.name.encode('ascii','ignore') : 1  for adjacent_zones in zone.adjacent_zones.all()}
    proximity = floydwarshall(graph)
    for name in zones.keys():
        zones[name]['proximity'] = proximity[name]
    return zones


def calculate_factors(period, group, zones, schedule):
    f = {}
    visits = {zone:0.0 for zone in zones.keys()}
    for prev_period in range(period):
        visits[schedule[prev_period][group]] += 1
    visitors = {zone:0.0 for zone in zones.keys()}
    for prev_group in range(group):
        visitors[schedule[period][prev_group]] += 1
    prev_zone = 'White Tent'
    if period > 0:
        prev_zone = schedule[period-1][group]
    for zone in zones.keys():
        f[zone] = {}
        f[zone]['level'] = zones[zone]['level']/5.0
        f[zone]['capacity'] = zones[zone]['capacity']
        f[zone]['visits'] = visits[zone]
        f[zone]['visitors'] = visitors[zone]
        f[zone]['vacancy'] = (1.0*f[zone]['capacity'] - 1.0*f[zone]['visitors']) / f[zone]['capacity']
        f[zone]['proximity'] = 1.0 - 1.0*zones[prev_zone]['proximity'][zone]/5
        f[zone]['hueristic'] = 0.0
        if f[zone]['vacancy'] != 0.0 and f[zone]['visits'] == 0.0 and f[zone]['level'] != 0.0:
            f[zone]['hueristic'] = 1#(10.0*f[zone]['proximity']) + (1.0*f[zone]['vacancy']) + (1.0*f[zone]['level'])
    return f

def print_schedule(schedule, zones):
    nickname = {
        'Adventure Woods' : 'Adventure Woods\t',
        'Adventure Base Camp' :'Adventure Base Camp',
        'Waterside Village' :'Waterside Village',
        'Waterside Tent' :'Waterside Tent\t',
        'The Plateau' :'The Plateau\t',
        'Waterfront' :'Waterfront\t',
        'White Tent' :'White Tent\t',
        'The Valley':'The Valley\t',
        'Moose Lodge Area' :'Moose Lodge Area\t',
        'Mountain View Field' :'Mountain View Field',
    }

    visitors = {zone:[0 for p in range(len(schedule))] for zone in zones}
    for p in range(len(schedule)):
        for g in range(len(schedule[0])):
            z = schedule[p][g]
            visitors[z][p] += 1

    for period in range(len(schedule)):
        print '\t\t\tPERIOD: [', str(1+period), ']',
    for group in range(len(schedule[0])):
        print '\nGROUP: [', str(group), ']\t',
        for period in range(len(schedule)):
            z = schedule[period][group]
            print ('['+str(visitors[z][p])+'/'+str(int(zones[z]['capacity']))+']'), nickname[z], '\t',
    print '\n'

def create_schedule(periods, groups, choices):
    keys = choices.keys()
    schedule = [[ 'White Tent' for group in range(groups)] for period in range(periods)]
    factors = [[ None for group in range(groups)] for period in range(periods)]
    period = 0
    group = 0
    trial_time = time.time()
    start_time = time.time()
    while period < periods:
        group = 0
        while group < groups:
            if factors[period][group] is None:
                factors[period][group] = calculate_factors(period, group, choices, schedule)
            t = sum([factors[period][group][key]['hueristic'] for key in keys])
            while t == 0.0:
                factors[period][group] = None
                if group is not 0:
                    group -=1
                elif period is not 0:
                    group = groups-1
                    period -=1
                else:
                    print 'NO POSSIBLE SCHEDULES'
                    return schedule, factors
                prev_assignment = schedule[period][group]
                schedule[period][group] = 'White Tent'
                factors[period][group][prev_assignment]['hueristic'] = 0.0
                t = sum([factors[period][group][key]['hueristic'] for key in keys])
                if (time.time() - trial_time) > 60:
                    schedule = [[ 'White Tent' for group in range(groups)] for period in range(periods)]
                    factors = [[ None for group in range(groups)] for period in range(periods)]
                    period = 0
                    group = 0
                    trial_time = time.time()
                if (time.time() - start_time) > 300:
                    print 'NO POSSIBLE SCHEDULES'
                    return schedule, factors
                print 'BACKWARD\t['+str(period)+']['+str(group)+']\t',
            p = [(factors[period][group][key]['hueristic']/t) for key in keys]
            schedule[period][group] = keys[np.random.choice(range(len(p)), p=p)]
            group += 1
        period += 1
    print_schedule(schedule, choices)
    return schedule, factors



def create_csv():
    employees = [{'last': 'Cooper', 'first': 'Jack'}, {'last': 'James', 'first': 'William'}, {'last': 'Morris', 'first': 'Charles'}, {'last': 'Powell', 'first': 'Daniel'}, {'last': 'Phillips', 'first': 'Mason'}, {'last': 'Evans', 'first': 'Aiden'}, {'last': 'Powell', 'first': 'Samantha'}, {'last': 'Mitchell', 'first': 'Christian'}, {'last': 'Clark', 'first': 'Jack'}, {'last': 'Cox', 'first': 'Carter'}, {'last': 'Carter', 'first': 'Lillian'}, {'last': 'Lopez', 'first': 'Allison'}, {'last': 'Rogers', 'first': 'Gabriel'}, {'last': 'Bennett', 'first': 'Landon'}, {'last': 'Hernandez', 'first': 'Harper'}, {'last': 'Rivera', 'first': 'Grayson'}, {'last': 'Adams', 'first': 'Grayson'}, {'last': 'Hernandez', 'first': 'Samantha'}, {'last': 'Lopez', 'first': 'Michael'}, {'last': 'Parker', 'first': 'Ella'}, {'last': 'Young', 'first': 'Benjamin'}, {'last': 'Anderson', 'first': 'Dylan'}, {'last': 'Griffin', 'first': 'Skylar'}, {'last': 'Bennett', 'first': 'Natalie'}, {'last': 'Patterson', 'first': 'Benjamin'}, {'last': 'Murphy', 'first': 'Joseph'}, {'last': 'Robinson', 'first': 'Samantha'}, {'last': 'Kelly', 'first': 'Leah'}, {'last': 'Lee', 'first': 'Addison'}, {'last': 'Martinez', 'first': 'Michael'}, {'last': 'Hughes', 'first': 'Chloe'}, {'last': 'Hernandez', 'first': 'Elizabeth'}, {'last': 'Ward', 'first': 'Hannah'}, {'last': 'Jones', 'first': 'Gabriel'}, {'last': 'Campbell', 'first': 'Hannah'}, {'last': 'Murphy', 'first': 'Jaxon'}, {'last': 'Clark', 'first': 'Liam'}, {'last': 'Davis', 'first': 'Christopher'}, {'last': 'Lee', 'first': 'Carter'}, {'last': 'Anderson', 'first': 'Lily'}, {'last': 'Powell', 'first': 'Carter'}, {'last': 'Brown', 'first': 'Lily'}, {'last': 'Coleman', 'first': 'Liam'}, {'last': 'Smith', 'first': 'Ryan'}, {'last': 'Gonzalez', 'first': 'Paisley'}, {'last': 'White', 'first': 'Chloe'}, {'last': 'Smith', 'first': 'William'}, {'last': 'White', 'first': 'Levi'}, {'last': 'Phillips', 'first': 'Victoria'}, {'last': 'Torres', 'first': 'Lucas'}, {'last': 'Stewart', 'first': 'Skylar'}, {'last': 'Jones', 'first': 'Abigail'}, {'last': 'Hall', 'first': 'Caleb'}, {'last': 'Peterson', 'first': 'Logan'}, {'last': 'Ramirez', 'first': 'Zoey'}, {'last': 'Wilson', 'first': 'Evelyn'}, {'last': 'Coleman', 'first': 'Elijah'}, {'last': 'Rodriguez', 'first': 'Andrew'}, {'last': 'Barnes', 'first': 'Lillian'}, {'last': 'Ross', 'first': 'Jayden'}, {'last': 'Griffin', 'first': 'Caleb'}, {'last': 'Martinez', 'first': 'Mason'}, {'last': 'Gonzales', 'first': 'James'}, {'last': 'James', 'first': 'Carter'}, {'last': 'Murphy', 'first': 'Alexa'}, {'last': 'Sanchez', 'first': 'Jack'}, {'last': 'Mitchell', 'first': 'Matthew'}, {'last': 'Foster', 'first': 'Violet'}, {'last': 'Bryant', 'first': 'Zoey'}, {'last': 'Anderson', 'first': 'Jayden'}, {'last': 'Garcia', 'first': 'Natalie'}, {'last': 'Clark', 'first': 'Gabriel'}, {'last': 'Diaz', 'first': 'Scarlett'}, {'last': 'Bell', 'first': 'Violet'}, {'last': 'Jackson', 'first': 'Aubrey'}, {'last': 'Flores', 'first': 'Jackson'}, {'last': 'Reed', 'first': 'Nathan'}, {'last': 'Kelly', 'first': 'James'}, {'last': 'Walker', 'first': 'Harper'}, {'last': 'Green', 'first': 'Mason'}, {'last': 'Gray', 'first': 'Jonathan'}, {'last': 'Hall', 'first': 'Dylan'}, {'last': 'Ward', 'first': 'Gabriel'}, {'last': 'Wright', 'first': 'Charles'}, {'last': 'Jones', 'first': 'Mason'}, {'last': 'Alexander', 'first': 'Joshua'}, {'last': 'Washington', 'first': 'Ethan'}, {'last': 'Martin', 'first': 'Victoria'}, {'last': 'Torres', 'first': 'Aria'}, {'last': 'Clark', 'first': 'Charlotte'}, {'last': 'Jenkins', 'first': 'Aiden'}, {'last': 'Cooper', 'first': 'Elijah'}, {'last': 'Sanders', 'first': 'Noah'}, {'last': 'Coleman', 'first': 'James'}, {'last': 'Carter', 'first': 'Skylar'}, {'last': 'Bailey', 'first': 'Natalie'}, {'last': 'Washington', 'first': 'Alexa'}, {'last': 'Bryant', 'first': 'Isabella'}, {'last': 'Johnson', 'first': 'William'}, {'last': 'Davis', 'first': 'Ethan'}]

    schedule = [['Arrival', 'Moose Lodge Area', 'Waterside Tent', 'Waterfront', 'Mountain View Field', 'Adventure Base Camp'], ['Arrival', 'The Plateau', 'Waterfront', 'The Valley', 'Adventure Base Camp', 'Mountain View Field'], ['Arrival', 'Waterfront', 'The Valley', 'The Plateau', 'Mountain View Field', 'Adventure Base Camp'], ['Arrival', 'Waterfront', 'Waterside Village', 'Adventure Woods', 'The Plateau', 'Adventure Base Camp'], ['Arrival', 'Moose Lodge Area', 'Adventure Woods', 'Waterside Village', 'Waterside Tent', 'The Plateau'], ['Arrival', 'Adventure Base Camp', 'Waterside Tent', 'Mountain View Field', 'Waterside Village', 'Moose Lodge Area'], ['Arrival', 'The Plateau', 'Waterside Tent', 'The Valley', 'Moose Lodge Area', 'Waterfront'], ['Arrival', 'Waterside Village', 'The Plateau', 'The Valley', 'Waterside Tent', 'Adventure Base Camp'], ['Arrival', 'Waterside Tent', 'Mountain View Field', 'Adventure Base Camp', 'The Valley', 'Waterside Village'], ['Arrival', 'Mountain View Field', 'Adventure Woods', 'Waterside Village', 'The Valley', 'Waterfront'], ['Arrival', 'Adventure Base Camp', 'Adventure Woods', 'Mountain View Field', 'Waterside Tent', 'Waterfront'], ['Arrival', 'Waterside Tent', 'The Plateau', 'Adventure Base Camp', 'The Valley', 'Mountain View Field'], ['Arrival', 'Waterfront', 'The Valley', 'Moose Lodge Area', 'Adventure Base Camp', 'Waterside Tent'], ['Arrival', 'Adventure Base Camp', 'Adventure Woods', 'Waterside Village', 'Waterside Tent', 'Waterfront'], ['Arrival', 'Waterside Village', 'Adventure Woods', 'Waterfront', 'Waterside Tent', 'The Valley'], ['Arrival', 'The Valley', 'The Plateau', 'Moose Lodge Area', 'Mountain View Field', 'Waterfront'], ['Arrival', 'Waterfront', 'Waterside Tent', 'The Plateau', 'Adventure Woods', 'Moose Lodge Area'], ['Arrival', 'Mountain View Field', 'Waterside Tent', 'Adventure Woods', 'Moose Lodge Area', 'The Plateau'], ['Arrival', 'Adventure Woods', 'Mountain View Field', 'Waterside Tent', 'The Plateau', 'Waterside Village'], ['Arrival', 'Waterside Tent', 'Adventure Base Camp', 'The Plateau', 'Moose Lodge Area', 'The Valley'], ['Arrival', 'Adventure Woods', 'Waterfront', 'The Valley', 'Waterside Village', 'Mountain View Field'], ['Arrival', 'Adventure Base Camp', 'Waterside Tent', 'Mountain View Field', 'The Valley', 'Moose Lodge Area'], ['Arrival', 'Mountain View Field', 'Adventure Base Camp', 'Adventure Woods', 'The Plateau', 'Waterside Village'], ['Arrival', 'Waterside Village', 'The Plateau', 'Adventure Base Camp', 'Waterfront', 'Moose Lodge Area'], ['Arrival', 'The Plateau', 'Adventure Woods', 'The Valley', 'Mountain View Field', 'Waterside Village'], ['Arrival', 'Moose Lodge Area', 'The Valley', 'Waterside Village', 'The Plateau', 'Adventure Woods'], ['Arrival', 'Adventure Woods', 'Waterside Village', 'Adventure Base Camp', 'Moose Lodge Area', 'Waterside Tent'], ['Arrival', 'The Plateau', 'Waterside Tent', 'Moose Lodge Area', 'Waterside Village', 'Adventure Base Camp'], ['Arrival', 'Waterfront', 'Adventure Base Camp', 'Adventure Woods', 'Waterside Village', 'The Valley'], ['Arrival', 'Waterside Village', 'Waterfront', 'The Valley', 'Moose Lodge Area', 'Adventure Woods'], ['Arrival', 'Adventure Base Camp', 'The Valley', 'Adventure Woods', 'Moose Lodge Area', 'The Plateau'], ['Arrival', 'Adventure Base Camp', 'Moose Lodge Area', 'Mountain View Field', 'Adventure Woods', 'The Plateau'], ['Arrival', 'Moose Lodge Area', 'Mountain View Field', 'Waterfront', 'Waterside Tent', 'The Valley'], ['Arrival', 'The Plateau', 'Waterfront', 'Waterside Tent', 'Mountain View Field', 'Moose Lodge Area'], ['Arrival', 'The Plateau', 'Waterfront', 'Mountain View Field', 'Adventure Base Camp', 'Waterside Village'], ['Arrival', 'Moose Lodge Area', 'The Valley', 'Mountain View Field', 'Adventure Base Camp', 'Adventure Woods'], ['Arrival', 'Waterside Village', 'The Valley', 'Waterside Tent', 'The Plateau', 'Moose Lodge Area'], ['Arrival', 'Adventure Base Camp', 'Waterside Tent', 'Waterfront', 'The Valley', 'Adventure Woods'], ['Arrival', 'Mountain View Field', 'Moose Lodge Area', 'Adventure Base Camp', 'Waterside Village', 'The Valley'], ['Arrival', 'Waterside Village', 'Adventure Woods', 'Adventure Base Camp', 'The Plateau', 'Waterside Tent'], ['Arrival', 'The Plateau', 'Waterside Village', 'Waterfront', 'Waterside Tent', 'Moose Lodge Area'], ['Arrival', 'Moose Lodge Area', 'Mountain View Field', 'The Plateau', 'Adventure Woods', 'The Valley'], ['Arrival', 'Adventure Base Camp', 'The Valley', 'Mountain View Field', 'Adventure Woods', 'Waterside Village'], ['Arrival', 'Adventure Woods', 'Moose Lodge Area', 'The Valley', 'Waterfront', 'Adventure Base Camp'], ['Arrival', 'Mountain View Field', 'Adventure Base Camp', 'Adventure Woods', 'The Valley', 'Waterside Tent'], ['Arrival', 'Mountain View Field', 'Adventure Base Camp', 'Waterside Tent', 'The Valley', 'Adventure Woods'], ['Arrival', 'Waterside Tent', 'The Plateau', 'Adventure Woods', 'Moose Lodge Area', 'Mountain View Field'], ['Arrival', 'Mountain View Field', 'Adventure Base Camp', 'Moose Lodge Area', 'The Plateau', 'Waterside Tent'], ['Arrival', 'Moose Lodge Area', 'Mountain View Field', 'The Plateau', 'Adventure Base Camp', 'Waterside Tent'], ['Arrival', 'Adventure Woods', 'Adventure Base Camp', 'Moose Lodge Area', 'The Valley', 'Mountain View Field'], ['Arrival', 'The Valley', 'Adventure Woods', 'Mountain View Field', 'Adventure Base Camp', 'Waterside Tent'], ['Arrival', 'The Valley', 'Moose Lodge Area', 'Waterside Village', 'Mountain View Field', 'The Plateau'], ['Arrival', 'Adventure Woods', 'Waterside Village', 'Moose Lodge Area', 'Mountain View Field', 'The Valley'], ['Arrival', 'Adventure Woods', 'The Valley', 'Waterside Tent', 'Adventure Base Camp', 'Mountain View Field'], ['Arrival', 'Waterside Tent', 'Adventure Base Camp', 'Waterside Village', 'Mountain View Field', 'The Plateau'], ['Arrival', 'Adventure Woods', 'The Plateau', 'Adventure Base Camp', 'Mountain View Field', 'Waterside Tent'], ['Arrival', 'Mountain View Field', 'Waterside Village', 'Waterside Tent', 'Adventure Woods', 'The Valley'], ['Arrival', 'The Valley', 'The Plateau', 'Moose Lodge Area', 'Adventure Woods', 'Mountain View Field'], ['Arrival', 'Waterside Tent', 'Mountain View Field', 'The Plateau', 'Waterside Village', 'The Valley'], ['Arrival', 'Mountain View Field', 'Waterside Village', 'The Plateau', 'Waterfront', 'Adventure Base Camp']]
    schedule_date = '3/10/2017'
    prefered_lunch = '14:00'
    first_period = '9:30'
    period_length = 90

    with open('schedule2.0.csv', 'wb') as csvfile:
        schedule_writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        periods = len(schedule[0])
        month = int(schedule_date[:schedule_date.index('/')])
        day = int(schedule_date[schedule_date.index('/')+1:schedule_date.index('/',2)])
        year = int(schedule_date[schedule_date.index('/',2)+1:])
        hrs = int(first_period[:first_period.index(':')])
        mins = int(first_period[first_period.index(':')+1:])
        date = datetime.datetime(year,month,day,hrs,mins,0)
        time_display = [str(date.date()),'',] + [ (date+datetime.timedelta(minutes=(p*period_length))).strftime("%I:%M %p") for p in range(periods)]
        employee_assignments = np.random.choice(employees, len(schedule))
        schedule_writer.writerow(time_display)
        for group_id in range(len(schedule)):
            group_name = 'Group ('+str(group_id)+')'
            employee_name = employee_assignments[group_id]['last']+', '+employee_assignments[group_id]['first']
            group_assignment_display = [employee_name,group_name]+schedule[group_id]
            schedule_writer.writerow(group_assignment_display)

'''
#[PERIOD][GROUP]
from scheduler.scheduler import *
choices = format_choices(Zone.objects.all())
s = create_schedule(5,60, choices)


Assigment = {
    Period = int,
    Group = int,
    Zone = key,
    Prev Assignment = {self},
    Next Assignment = {self},
    Potential Next = [self...]
}

'''