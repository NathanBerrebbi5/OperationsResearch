"""
author: Nathan Berrebbi

Overview: Given a Universe and a list of Subsets, find the minimum number of Sets needed
to cover the whole universe.
This is a NP-Complete problem

More details here:
https://en.wikipedia.org/wiki/Set_cover_problem

"""

#linear programming algorithm: find the optimal solution but is computationnaly costly (Set cover is NP-complete)
# I used the linear programming library pulp

from pulp import * 

def setCoverLP(big_set , list_sets):
    prob = LpProblem("set cover", LpMinimize)    
    # Variables
    Rows = range(len(list_sets))    
    choices = LpVariable.dicts("Choice",(Rows) ,0,1,LpInteger)         
    obj = 0
    for i in Rows:        
            obj+= choices[i]       
    # Objective
    prob += obj     
    # Constraints    
    for element in big_set:  
        l = [choices[i] for i in Rows if element in list_sets[i]]                      
        prob += sum(l) >= 1, ""     
    status = prob.solve()    
    print LpStatus[status]
    res = []
    for i in Rows:        
            #print i,'-',j,'-',value(choices[i][j]) 
            res.append({'i':i , 'Xi':value(choices[i])})
    print 'objective value : ' , value(obj)
    sets_selectionned = [list_sets[r['i']] for r in res if r['Xi']==1 ]
    return {'sets_selectionned':sets_selectionned , 'nb_set': value(obj) }

#The greedy algorithm for set covering chooses sets according to one rule: at each stage,
#choose the set that contains the largest number of uncovered elements. 

def max_uncov_set(remaining_sets,uncovered_element):
    nb_remaining = [{'remaining_set':remaining_set , 'nb_uncov':len(remaining_set.intersection(uncovered_element))}for remaining_set in remaining_sets]
    return max(nb_remaining,key = lambda x:x['nb_uncov'])['remaining_set']


def greedySetCover(big_set , list_sets):
    uncovered_elements = big_set
    remaining_sets = list_sets
    result = []
    while len(uncovered_elements) > 0 and len(remaining_sets)>0 :
        maxi = max_uncov_set(remaining_sets,uncovered_elements)
        result.append(maxi)
        remaining_sets.remove(maxi)
        uncovered_elements = uncovered_elements.difference(maxi)
    return {'sets_selectionned':result , 'nb_set': len(result) }

########## tests #################

big_set = set(range(1,6))
list_sets = [
set([1,2,3]),
set([2,4]),
set([3,4]),
set([4,5]),
]

# Comparing the results given by the linear programming method and the greedy algorithm
setCov_lp = setCoverLP(big_set , list_sets)
setCov_greedy = greedySetCover(big_set , list_sets)


