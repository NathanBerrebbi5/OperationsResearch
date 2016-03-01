"""
author: Nathan Berrebbi

More details: https://en.wikipedia.org/wiki/Branch_and_bound

"""
import networkx as nx
import numpy as np


def relaxedKnapsack2(weights,max_weight,volumes,variables_already_set):
    print 'start relaxedKnapsack2'           
    variables_already_set_ix = [v['ix_var'] for v in variables_already_set]
    print 'set ix' , variables_already_set_ix      
    upper_bound = 0  
    for v in variables_already_set:
        if v['value_var'] == 1 :
            print 'v : ' , v , weights[v['ix_var']]
            upper_bound+=volumes[v['ix_var']]
            max_weight-=weights[v['ix_var']]   
    n = len(weights)
    utilities = [{'w':weights[i],'vol':volumes[i],'utility':volumes[i]/float(weights[i])} for i in range(n) if i not in variables_already_set_ix]    
    utilities_sorted = sorted(utilities,key=lambda x:-x['utility'])    
    sum_weights = 0
    sum_volumes = 0
    i = 0     
    objects_taken =[]
    while sum_weights + utilities_sorted[i]['w'] < max_weight:
        objects_taken.append({'quantity':1 , 'object':utilities_sorted[i]})
        sum_weights+= utilities_sorted[i]['w']
        sum_volumes+= utilities_sorted[i]['vol']        
        i+=1
    sum_volumes+=(max_weight-sum_weights)/float(utilities_sorted[i]['w']) * utilities_sorted[i]['vol']  
    objects_taken.append({'object':utilities_sorted[i] , 'quantity':(max_weight-sum_weights)/float(utilities_sorted[i]['w'])})    
    upper_bound += np.floor(sum_volumes)   
    ix_variable_split = volumes.index(utilities_sorted[i]['vol'])
    if objects_taken[-1]['quantity'] == 1 :
        feasable = 1
    else:
        feasable = 0    
    return {'objects_taken':objects_taken , 'feasable':feasable, 'ix_split':ix_variable_split,'upper_bound':int(upper_bound)}


def subProblem(weights,max_weight,volumes,ix_variable_split,variables_already_set2):
    print'start subprob'   
    variables_already_set_copy_1 = list(variables_already_set2)    
    variables_already_set_copy_2 = list(variables_already_set2)
    variables_already_set_copy_1.append({'ix_var': ix_variable_split , 'value_var':0})
    variables_already_set_copy_2.append({'ix_var': ix_variable_split , 'value_var':1})
    print 'var set 1 : ' , variables_already_set_copy_1
    print 'var set 2 : ' , variables_already_set_copy_2    
    relaxed_0 = relaxedKnapsack2(weights,max_weight,volumes,variables_already_set_copy_1)
    relaxed_1 = relaxedKnapsack2(weights,max_weight,volumes,variables_already_set_copy_2)
    return {'relaxed_0':relaxed_0 , 'relaxed_1':relaxed_1}
   

def findNextCurrentNode(unexplored_nodes,tree):
    no = tree.node
    m = max(unexplored_nodes,key = lambda x:no[x]['upper_bound'])
    return m
   
def isPossible(tree,node_ix,max_weight,weights,lower_bound):
    sum_weight = 0
    variables_already_set = tree.node[node_ix]['variables_set']
    for v in variables_already_set:
        if v['value_var']==1:
            sum_weight+=weights[v['ix_var']]
    return sum_weight <=max_weight and tree.node[node_ix]['upper_bound']> lower_bound


def branchAndBound(weights,max_weight,volumes):
    lower_bound = 0   
    tree = nx.DiGraph()
    nodes_explored = []
    current_node = 1
    knap_0 = relaxedKnapsack2(weights,max_weight,volumes,[])
    upper_bound_0  ,feasable_0 = knap_0['upper_bound'] , knap_0['feasable']              
    tree.add_node(1,upper_bound =upper_bound_0 , feasable = feasable_0 ,variables_set = [])
    print 'upper bound 0 : ' ,upper_bound_0
    variables_already_set = []
    ix_split= relaxedKnapsack2(weights,max_weight,volumes,[])['ix_split']
    print 'ix_split' , ix_split    
    cpt = 0
    nodes_unexplored = [2,3]
   
    while cpt < np.power(2,len(weights)) and len(nodes_unexplored)>0:
        cpt+=1
        print ' ############### new while ###########################' 
        print 'current_node' , current_node
        nodes_explored.append(current_node)       
        variables_already_set = tree.node[current_node]['variables_set']
        print 'var already set ' , variables_already_set     
        sub_prob = subProblem(weights,max_weight,volumes,ix_split,variables_already_set)        
        upper_bound_1 ,feasable_1 = sub_prob['relaxed_0']['upper_bound'],sub_prob['relaxed_0']['feasable']
        if feasable_1 == 1 and upper_bound_1 > lower_bound:
            lower_bound = upper_bound_1
            node_feasible = 2*current_node
        upper_bound_2 ,feasable_2 = sub_prob['relaxed_1']['upper_bound'],sub_prob['relaxed_1']['feasable']
        if feasable_2 == 1 and upper_bound_2 > lower_bound:
                lower_bound = upper_bound_2 
                node_feasible = 2*current_node+1
        print 'upper bound 1 ' ,  upper_bound_1
        print 'upper bound 2 ' ,  upper_bound_2 
        variables_set_1,variables_set_2 = list(variables_already_set),list(variables_already_set)
        variables_set_1.append({'ix_var': ix_split , 'value_var':0})
        variables_set_2.append({'ix_var': ix_split , 'value_var':1})       
        tree.add_node(2*current_node,upper_bound =upper_bound_1,feasable = feasable_1 , variables_set= variables_set_1)
        tree.add_node(2*current_node+1,upper_bound =upper_bound_2,feasable = feasable_2,variables_set = variables_set_2)
        tree.add_edge(current_node,2*current_node,ix_split = ix_split , value_split = 0)
        tree.add_edge(current_node,2*current_node+1,ix_split = ix_split , value_split = 1)
        nodes_unexplored = [n for n in tree.nodes() if n not in nodes_explored and isPossible(tree,n,max_weight,weights,lower_bound)]
        print 'node unexplored' ,nodes_unexplored 
        if len(nodes_unexplored) == 0 :
            break
        if upper_bound_1 > upper_bound_2:
            ix_split = sub_prob['relaxed_0']['ix_split']
            value_var = 0
        else:             
            ix_split = sub_prob['relaxed_1']['ix_split']
            value_var = 1
        current_node = findNextCurrentNode(nodes_unexplored,tree)        
        print 'nextttttt current node = ' , current_node
        print 'possible ? : ' , isPossible(tree,current_node,max_weight,weights,lower_bound)
           
        variables_already_set.append({'ix_var':ix_split , 'value_var':value_var})       
    objects_taken = relaxedKnapsack2(weights,max_weight,volumes,tree.node[node_feasible]['variables_set'])
    return {'tree':tree , 'node_feasible':node_feasible,'objects_taken':objects_taken , 'max':lower_bound}

############  tests ##################
   
volumes = [44,23,19,28,14]
weights = [19,8,7,11,6]
capacities = [5,8,2,2,14]
max_weight = 25


bb = branchAndBound(weights,max_weight,volumes)
print bb
