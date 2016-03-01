"""
author: Nathan Berrebbi

Overview: A vertex cover of a graph is a set of vertices such that each edge of the graph is incident to at least one vertex of the set. 
This optimization problem consists in finding a minimum vertex cover of a graph
This is a NP-Complete problem

More details here:
https://en.wikipedia.org/wiki/Vertex_cover

"""

from pulp import *
import networkx as nx

def matrix2Graph(dist_matrix):
    G = nx.Graph()
    n = len(dist_matrix)
    for i in range(n):
        for j in range(n):
            if dist_matrix[i][j] != 0 :
                G.add_edge(i,j,weight = dist_matrix[i][j] )
    return G
    
def graph2Matrix(graph): 
    n = len(graph.nodes())
    dist_matrix = [[0 for i in range(n)] for j in range(n)]
    for edge in graph.edges():
        i,j = edge[0],edge[1]
        w = graph.get_edge_data(i,j)['weight']
        dist_matrix[j][i] = w
        dist_matrix[i][j] = w
    return dist_matrix
    
#linear programming algorithm: find the optimal solution but is computationnaly costly (Set cover is NP-complete)
# I used the linear programming library pulp
    
def vertexCoverLP(dist_matrix,vertex_weights):
    prob = LpProblem("vertex cover", LpMinimize)    
    # Variables
    Rows = range(len(dist_matrix))    
    choices = LpVariable.dicts("Choice",(Rows) ,0,1,LpInteger)         
    obj = 0
    for i in Rows:        
            obj+= choices[i]*vertex_weights[i]        
    # Objective
    prob += obj     
    # Constraints    
    for i in Rows:    
            for j in Rows: 
                if dist_matrix[i][j] > 0 : 
                    prob += choices[i] + choices[j] >= 1, ""       
    status = prob.solve()    
    print LpStatus[status]
    res = []
    for i in Rows:        
            #print i,'-',j,'-',value(choices[i][j]) 
            res.append({'i':i , 'Xi':value(choices[i])})
    print 'objective value : ' , value(obj)
    vertices = [r['i'] for r in res if r['Xi']==1 ]
    return {'vertices':vertices , 'obj': value(obj) }
    
    
"""
The below approximation algorithm finds a solution that is in the worst case twice the optimal solution
in other words approx_solution < 2*optimal_solution
The algorithm consists in taking the endpoints of every edge of a maximal matching 
More details on maximal matching: https://en.wikipedia.org/wiki/Matching_(graph_theory)
"""

def twoOptApprox(graph):
    max_matching = list(nx.maximal_matching(graph))
    res = [x[0] for x in max_matching]
    res.extend([x[1] for x in max_matching])
    return res

########## tests ####################
    
G = nx.Graph()
G.add_edge(0,1,weight = 1)
G.add_edge(0,4,weight = 1)
G.add_edge(1,2,weight = 1)
G.add_edge(2,3,weight = 1)
G.add_edge(3,4,weight = 1)
G.add_edge(4,1,weight = 1)
G.add_edge(2,5,weight = 1)


dist_matrix = graph2Matrix(G)
vertex_weights = [1 for i in range(len(G.nodes()))]  
vcov_lp = vertexCoverLP(dist_matrix,vertex_weights)
vcov_approx = twoOptApprox(G)

    