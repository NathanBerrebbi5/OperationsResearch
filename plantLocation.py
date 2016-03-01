"""
author: Nathan Berrebbi

Overview: 

More details here:
https://en.wikipedia.org/wiki/Vertex_cover

"""

from pulp import *


def plantLocationPB(production,demand,shipping_cost,fixed_cost):
    prob = LpProblem("transportation", LpMinimize)
    
    # Variables
    Rows = range(len(production))
    Cols = range(len(demand))
    #Fi = range(len(fixed_cost))
    choices = LpVariable.dicts("Choice",(Rows,Cols))   
    y = LpVariable.dicts("Fixed",(Rows),0,1,LpInteger)
    # LpVariable.dicts("Choice",(Rows,Cols),0,100000,LpInteger)
    obj = 0
    for r in Rows:
        for c in Cols:
            obj+= choices[r][c]*shipping_cost[r][c]
    for r in Rows:
        obj+= fixed_cost[r]*y[r]
    # Objective
    prob += obj     
    # Constraints    
    for r in Rows:    
            prob += lpSum([choices[r][c] for c in Cols]) <= production[r]*y[r]   , ""
    for c in Cols:    
            prob += lpSum([choices[r][c] for r in Rows]) == demand[c] , ""    
    for r in Rows:
        for c in Cols:
            prob+= choices[r][c] >=0
    
    status = prob.solve()
    print LpStatus[status]
    resX = []
    resY =[]
    for r in Rows:
        resY.append({'i':r , 'Yi': value(y[r])})
        for c in Cols:
            print r,'-',c,'-',value(choices[r][c]) 
            resX.append({'i':r , 'j':c , 'Xij':value(choices[r][c])})
    print 'objective value : ' , value(obj)
    return {'X':resX , 'Y':resY , 'obj': value(obj)}

fixed_cost = [110,44,130]
res2 = plantLocationPB(production,demand,shipping,fixed_cost)
