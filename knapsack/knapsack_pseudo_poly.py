"""
author Nathan Berrebbi


Nore details: 
https://en.wikipedia.org/wiki/List_of_knapsack_problems
"""
import time
from pulp import *


def pseudoPolyKnapsack(weights,max_weight,volumes):
    t1 = time.time()
    n = len(weights)
    m = [[0 for i in range(max_weight+1)] for j in range(n+1)] 
    for i in range(1,n+1):
        for j in range(max_weight+1):
            if weights[i-1] <= j :
                m[i][j] = max(m[i-1][j], m[i-1][j-weights[i-1]] + volumes[i-1])
            else:    
                m[i][j] = m[i-1][j]
    t2 = time.time()
    print 'time pseudo' , t2-t1
    return m
    
    
volumes = [44,23,19,28,14]
weights = [19,8,7,11,6]
capacities = [5,8,2,2,14]
max_weight = 25

knap_pseudo_poly = pseudoPolyKnapsack(weights,max_weight,volumes)  
# the value is in the last element of the matrix  
print knap_pseudo_poly[-1][-1]    
    
    