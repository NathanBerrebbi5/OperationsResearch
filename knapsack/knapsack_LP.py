"""
author Nathan Berrebbi


Nore details: 
https://en.wikipedia.org/wiki/List_of_knapsack_problems
"""

import time
from pulp import *


#0-1 knapscack
def knapsackLP(weights,max_weight,volumes):
    t1 = time.time()
    prob = LpProblem("knapsack 0-1", LpMaximize) 
    n = len(weights)
    # Variables
    Rows = range(n)    
    #Fi = range(len(fixed_cost))
    choices = LpVariable.dicts("Choice",(Rows),0,1,LpInteger)   
    obj = 0
    for r in Rows:        
            obj+= choices[r]*volumes[r]
    # Objective
    prob += obj 
    #print prob    
    # Constraints 
    summ = sum([choices[r]*weights[r] for r in Rows])
    prob+= summ <= max_weight
    #print prob
    status = prob.solve()
    print LpStatus[status]
    res = []
    for r in Rows:        
            #print r,'-',c,'-',value(choices[r][c]) 
            res.append({'i':r ,'Xi':value(choices[r])})
    t2 = time.time()
    print 'time  0-1 LP = %.2f'  %float(t2-t1)
    #print 'objective value : ' , value(obj)
    return {'variables':res , 'obj': value(obj), 'sum_weight':value(summ)}


############ tests ######################

volumes = [44,23,19,28,14]
weights = [19,8,7,11,6]
capacities = [5,8,2,2,14]
max_weight = 25    
knap = knapsackLP(weights,max_weight,volumes)

print knap