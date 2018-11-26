"""
author: Nathan Berrebbi
test modification
Overview: find a shortest closed path or circuit that visits every edge of a (connected) undirected graph
This is a NP-Complete problem

More details here:
https://en.wikipedia.org/wiki/Route_inspection_problem

"""

import networkx as nx
import itertools as it
    

def findOddDegreeMatrix(graph):
    degrees = graph.degree()         
    odd_degree_nodes = [i for i in graph.nodes() if degrees[i]%2==1]
    maxi = max(odd_degree_nodes)
    #print 'maxi' , maxi
    #print 'odd nodes : ' ,odd_degree_nodes
    odd_paths_length = []
    comb = list(it.combinations(odd_degree_nodes,2))
    matrix_cost = [[0 for i in range(maxi+1)]  for j in range(maxi+1)]
    for couple_nodes in comb:
        i,j = couple_nodes[0],couple_nodes[1]
        matrix_cost[i][j] = nx.algorithms.dijkstra_path_length(graph,i,j)
        #matrix_cost[j][i] = nx.algorithms.dijkstra_path_length(graph,i,j)        
        odd_paths_length.append({'i':i , 'j':j , 'path_length':nx.algorithms.dijkstra_path_length(graph,i,j)})
    return {'odd_paths_length':odd_paths_length , 'odd_nodes':odd_degree_nodes , 'matrix_cost':matrix_cost}
    
"""
A matching is a set of edges without common vertices
The problem can be formulated as a Linear Programming problem (I used pulp library)
More details here: https://en.wikipedia.org/wiki/Matching_(graph_theory)
"""
from pulp import *   
   
def findMatching(odd_paths_length,odd_nodes,matrix_cost):    
    
    prob = LpProblem("chinese_postman", LpMinimize)    
    # Variables
    Rows = odd_nodes
    Cols = odd_nodes
    #Fi = range(len(fixed_cost))
    choices = LpVariable.dicts("Choice",(Rows,Cols),0,1,LpInteger)   
    obj = 0
    for r in Rows:
        for c in Cols:
            obj+= choices[r][c]*matrix_cost[r][c]
    # Objective
    prob += obj     
    # Constraints 
    for i in Rows:
        for j in Cols:
            if i>=j:
                prob+= choices[i][j] <= 0 ,""
    
    for k in odd_nodes:
        s = 0
        l1 = [choices[i][k] for i in odd_nodes if i<k]
        l2 = [choices[k][j] for j in odd_nodes if k<j]
        s+=sum(l1)
        s+=sum(l2)
        prob+= s == 1 , ""    
    status = prob.solve()
    #print LpStatus[status]
    res = []
    for r in Rows:
        for c in Cols:
            #print r,'-',c,'-',value(choices[r][c]) 
            res.append({'i':r , 'j':c , 'Xij':value(choices[r][c])})
    #print 'objective value : ' , value(obj)
    matching = [(r['i'],r['j']) for r in res if r['Xij']>0]
    return {'variables':res , 'obj': value(obj),'matching':matching}


"""
Chinese Postman algorithm:
- if the graph is already eulerian, just find an eulerian circuit
- otherwise: first find the nodes with odd degree and find a matching in the induced graph
We make the graph eulerian by doubling the edges of this matching, and then find a eulerian circuit in this new graph
"""


def chinesePostman(graph):
    if nx.algorithms.is_eulerian(graph):
        print 'graph already eulerian'
        return list(nx.algorithms.eulerian_circuit(graph))
    else:
        print 'graph not eulerian : need to add edges ' 
        odds = findOddDegreeMatrix(graph)
        ress =  findMatching(odds['odd_paths_length'],odds['odd_nodes'],odds['matrix_cost'])
        matching = ress['matching'] 
        for couple_node in matching:
            print couple_node
            shortest_path = nx.algorithms.dijkstra_path(graph,couple_node[0],couple_node[1])
            for i in range(len(shortest_path)-1):
                node1,node2 = shortest_path[i],shortest_path[i+1]
                print node1,'-',node2
                w = graph.get_edge_data(node1,node2)[0]['weight']
                print 'w : ' , w                
                graph.add_edge(node1,node2,weight = w)
    tour = list(nx.algorithms.eulerian_circuit(graph))
    weight_tour_list = [graph.get_edge_data(n[0],n[1])[0]['weight'] for n in tour]
    return {'tour':tour , 'weight_tour':sum(weight_tour_list)}           


########## tests #######################

G = nx.MultiGraph()

G.add_edge(0,1,weight=5)
G.add_edge(1,2,weight=4)
G.add_edge(3,4,weight=1)
G.add_edge(4,5,weight=2)
G.add_edge(6,7,weight=2)
G.add_edge(7,8,weight=1)
G.add_edge(0,3,weight=1)
G.add_edge(3,6,weight=2)
G.add_edge(1,4,weight=1)
G.add_edge(4,7,weight=6)
G.add_edge(2,5,weight=2)
G.add_edge(5,8,weight=1)

nx.draw(G)
odds = findOddDegreeMatrix(G)
#eulerian_circ_edges = [ e for e in nx.algorithms.eulerian_circuit(G)]
matching_dict =  findMatching(odds['odd_paths_length'],odds['odd_nodes'],odds['matrix_cost'])
matching = matching_dict['matching']
postman = chinesePostman(G)

