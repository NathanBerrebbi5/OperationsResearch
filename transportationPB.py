"""
author: Nathan Berrebbi


More details here:
https://www.utdallas.edu/~scniu/OPRE-6201/documents/TP1-Formulation.pdf

"""



from pulp import *

def transportationPB(production,demand,shipping_cost):
    prob = LpProblem("transportation", LpMinimize)
    
    # Variables
    Rows = range(len(production))
    Cols = range(len(demand))
    choices = LpVariable.dicts("Choice",(Rows,Cols))   
    # LpVariable.dicts("Choice",(Rows,Cols),0,100000,LpInteger)
    obj = 0
    for r in Rows:
        for c in Cols:
            obj+= choices[r][c]*shipping_cost[r][c]
        
    # Objective
    prob += obj     
    # Constraints    
    for r in Rows:    
            prob += lpSum([choices[r][c] for c in Cols]) == production[r] , ""
    for c in Cols:    
            prob += lpSum([choices[r][c] for r in Rows]) == demand[c] , ""    
    for r in Rows:
        for c in Cols:
            prob+= choices[r][c] >=0
    
    status = prob.solve()
    print LpStatus[status]
    res = []
    for r in Rows:
        for c in Cols:
            print r,'-',c,'-',value(choices[r][c]) 
            res.append({'i':r , 'j':c , 'Xij':value(choices[r][c])})
    print 'objective value : ' , value(obj)
    return {'variables':res , 'obj': value(obj)}


shipping = [[250,420,380,280],[1280,990,1440,1520],[1550,1420,1660,1730]]
production = [45,120,95]
demand = [80,78,47,55]

res1 = transportationPB(production,demand,shipping)

