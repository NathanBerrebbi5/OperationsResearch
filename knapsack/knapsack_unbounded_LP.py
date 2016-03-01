"""
author Nathan Berrebbi

Unbounded knapsack: As opposed to 0-1 knapsack, we can take in the knapsack a non integer number of an object

Nore details: 
https://en.wikipedia.org/wiki/List_of_knapsack_problems
"""

import time
from pulp import *



def unboundedKnapsackLP(weights,max_weight,volumes):
    t1 = time.time()
    prob = LpProblem("unbounded", LpMaximize) 
    n = len(weights)
    # Variables
    Rows = range(n)    
    #Fi = range(len(fixed_cost))
    choices = LpVariable.dicts("Choice",(Rows))   
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
    
    #print 'objective value : ' , value(obj)
    t2 = time.time()
    print 'time  unbounded LP = %.2f'  %float(t2-t1)
    return {'variables':res , 'obj': value(obj), 'sum_weight':value(summ)}
    
############ tests ######################

volumes = [44,23,19,28,14]
weights = [19,8,7,11,6]
capacities = [5,8,2,2,14]
max_weight = 25    
knap_unbounded = unboundedKnapsackLP(weights,max_weight,volumes)

print knap_unbounded