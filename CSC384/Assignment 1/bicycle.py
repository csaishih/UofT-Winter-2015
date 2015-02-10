#Shihan Ai
#g3aishih
#999700649

#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the bicycle domain.  

'''
bicycle STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
from math import sqrt

class bicycle(StateSpace):
    def __init__(self, action, gval, carrying, loc, time, earned, unstarted, map, job_list, parent = None):
#IMPLEMENT
        '''Initialize a bicycle search state object.'''
        if action == 'START':   #NOTE action = 'START' is treated as starting the search space
            StateSpace.n = 0
        StateSpace.__init__(self, action, gval, parent)
        #implement the rest of this function.
        self.carrying = carrying
        self.loc = loc
        self.time = time
        self.earned = earned
        self.unstarted = unstarted
        self.map = map
        self.job_list = job_list
        
    def successors(self): 
#IMPLEMENT
        '''Return list of bicycle objects that are the successors of the current object'''
        States = list()
        if self.action == 'START':
            for i in range(0, len(self.unstarted)):
                new_carrying = []
                for j in range(0, len(self.carrying)):
                    new_carrying.append(self.carrying[j])
                new_carrying.append(self.unstarted[i])

                for j in range(0, len(self.job_list)):
                    if self.unstarted[i] == self.job_list[j][0]:
                        new_loc = self.job_list[j][1]
                        new_time = self.job_list[j][2]

                new_unstarted = self.unstarted[:i] + self.unstarted[i + 1:]
                States.append(bicycle('first_pickup({})'.format(self.unstarted[i]), self.gval, new_carrying, new_loc, new_time, self.earned, new_unstarted, self.map, self.job_list, self))

        if self.action != 'START' and self.carrying != []:
            for i in range(0, len(self.carrying)):
                job = self.carrying[i]
                for j in range(0, len(self.job_list)):
                    if job == self.job_list[j][0]:
                        loc1 = self.job_list[j][1]
                        loc2 = self.job_list[j][3]
                        new_loc = loc2
                        distance = 0
                        for k in range(0, len(self.map[1])):
                            if loc1 in self.map[1][k] and loc2 in self.map[1][k]:
                                distance = self.map[1][k][2]
                        new_time = self.time + distance
                        new_earned = self.earned
                        for k in range(0, len(self.job_list[j][5])):
                            if new_time <= self.job_list[j][5][k][0]:
                                new_earned = new_earned + self.job_list[j][5][k][1]
                                break
                        
                new_carrying = self.carrying[:i] + self.carrying[i+1:]                        
                States.append(bicycle('deliver({})'.format(job), self.gval, new_carrying, new_loc, new_time, new_earned, self.unstarted, self.map, self.job_list, self))

        if self.action != 'START' and self.get_load() < 10000:
            for i in range(0, len(self.unstarted)):
                new_carrying = []
                for j in range(0, len(self.carrying)):
                    new_carrying.append(self.carrying[j])

                for j in range(0, len(self.job_list)):
                    if self.unstarted[i] == self.job_list[j][0]:
                        if (self.get_load() + self.job_list[j][4]) < 10000:
                            job = self.unstarted[i]
                            new_carrying.append(job)

                for j in range(0, len(self.job_list)):
                    if job == self.job_list[j][0]:
                        loc1 = self.job_list[j][1]
                        new_loc = loc1
                        distance = 0
                        for k in range(0, len(self.map[1])):
                            if loc1 in self.map[1][k] and self.loc in self.map[1][k]:
                                distance = self.map[1][k][2]           
                        new_time = self.time + distance
                        if self.job_list[j][2] > new_time:
                            new_time = self.job_list[j][2]
                new_unstarted = self.unstarted[:i] + self.unstarted[i+1:]
            
                States.append(bicycle('pickup({})'.format(job), self.gval, new_carrying, new_loc, new_time, self.earned, new_unstarted, self.map, self.job_list, self))


        return States

    def hashable_state(self) :
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        
    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output. 
        #Note that if you implement the "get" routines below properly, 
        #This function should work irrespective of how you represent
        #your state. 

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
            
        print("    Carrying: {} (load {} grams)".format(
                      self.get_carrying(), self.get_load()))
        print("    State time = {} loc = {} earned so far = {}".format(
                      self.get_time(), self.get_loc(), self.get_earned()))
        print("    Unstarted Jobs.{}".format(self.get_unstarted()))

    def get_loc(self):
#IMPLEMENT
        '''Return location of courier in this state'''
        return self.loc

    def get_carrying(self):
#IMPLEMENT
        '''Return list of NAMES of jobs being carried in this state'''
        return self.carrying
    
    def get_load(self):
#IMPLEMENT
        '''Return total weight being carried in this state'''
        load = 0
        for i in range(0, len(self.job_list)):
            if self.job_list[i][0] in self.carrying:
                load += self.job_list[i][4]
        return load        
        
    def get_time(self):
#IMPLEMENT
        '''Return current time in this state'''
        return self.time
    
    def get_earned(self):
#IMPLEMENT
        '''Return amount earned so far in this state'''
        return self.earned;
    
    def get_unstarted(self):
#IMPLEMENT
        '''Return list of NAMES of jobs not yet stated in this state''' 
        return self.unstarted
    
def heur_null(state):
    '''Null Heuristic use to make A* search perform uniform cost search'''
    return 0

def heur_sum_delivery_costs(state):
#IMPLEMENT
    '''Bicycle Heuristic sum of delivery costs.'''
    #Sum over every job J being carried: Lost revenue if we
    #immediately travel to J's dropoff point and deliver J.
    #Plus 
    #Sum over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
    #point then to J's dropoff poing and then deliver J.
    

def heur_max_delivery_costs(state):
#IMPLEMENT
    '''Bicycle Heuristic sum of delivery costs.'''
    #m1 = Max over every job J being carried: Lost revenue if we immediately travel to J's dropoff
    #point and deliver J.
    #m2 = Max over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
    #point then to J's dropoff poing and then deliver J.
    #heur_max_delivery_costs(state) = max(m1, m2)


def bicycle_goal_fn(state):
#IMPLEMENT
    '''Have we reached the goal (where all jobs have been delivered)?'''
    return state.carrying == [] and state.unstarted == []

def make_start_state(map, job_list):
#IMPLEMENT
    '''Input a map list and a job_list. Return a bicycle StateSpace object
    with action "START", gval = 0, and initial location "home" that represents the 
    starting configuration for the scheduling problem specified'''
    unstarted = []
    for i in range(0, len(job_list)):
        unstarted.append(job_list[i][0])
    return bicycle('START', 0, [], 'home', 420, 0, unstarted, map, job_list, parent = None)

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################

def make_rand_map(nlocs):
    '''Generate a random collection of locations and distances 
    in input format'''
    lpairs = [(randint(0,50), randint(0,50)) for i in range(nlocs)]
    lpairs = list(set(lpairs))  #remove duplicates
    nlocs = len(lpairs)
    lnames = ["loc{}".format(i) for i in range(nlocs)]
    ldists = list()

    for i in range(nlocs):
        for j in range(i+1, nlocs):
            ldists.append([lnames[i], lnames[j],
                           int(round(euclideandist(lpairs[i], lpairs[j])))])
    return [lnames, ldists]

def dist(l1, l2, map):
    '''Return distance from l1 to l2 in map (as output by make_rand_map)'''
    ldist = map[1]
    if l1 == l2:
        return 0
    for [n1, n2, d] in ldist:
        if (n1 == l1 and n2 == l2) or (n1 == l2 and n2 == l1):
            return d
    return 0
    
def euclideandist(p1, p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def make_rand_jobs(map, njobs):
    '''input a map (as output by make_rand_map) object and output n jobs in input format'''
    jobs = list()
    for i in range(njobs):
        name = 'Job{}'.format(i)
        ploc = map[0][randint(0,len(map[0])-1)]
        ptime = randint(7*60, 16*60 + 30) #no pickups after 16:30
        dloci = randint(0, len(map[0])-1)
        if map[0][dloci] == ploc:
            dloci = (dloci + 1) % len(map[0])
        dloc = map[0][dloci]
        weight = randint(10, 5000)
        job = [name, ploc, ptime, dloc, weight]
        payoffs = list()
        amount = 50
        #earliest delivery time
        time = ptime + dist(ploc, dloc, map)
        for j in range(randint(1,5)): #max of 5 payoffs
            time = time + randint(5, 120) #max of 120mins between payoffs
            amount = amount - randint(5, 25)
            if amount <= 0 or time >= 19*60:
                break
            payoffs.append([time, amount])
        job.append(payoffs)
        jobs.append(job)
    return jobs

def test(nloc, njobs):
    map = make_rand_map(nloc)
    jobs = make_rand_jobs(map, njobs)
    print("Map = ", map)
    print("jobs = ", jobs)
    s0 = make_start_state(map, jobs)
    print("heur Sum = ", heur_sum_delivery_costs(s0))
    print("heur max = ", heur_max_delivery_costs(s0))
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, bicycle_goal_fn, heur_max_delivery_costs)
    

