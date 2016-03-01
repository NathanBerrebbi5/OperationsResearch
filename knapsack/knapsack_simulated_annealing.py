"""
author: Nathan Berrebbi

More details: https://en.wikipedia.org/wiki/Simulated_annealing

"""

import numpy as np
import random 


def simulatedAnnealingStep(weights,max_weight,volumes,items_selected,t0):
    n = len(weights)
    t = t0    
    print ' start items selected ' , items_selected
    items_remaining = [i for i in range(n) if i not in items_selected]
    weight_selected = [weights[i] for i in items_selected]
    print 'starting weight selected' , weight_selected
    volume_start = [volumes[i] for i in items_selected] 
    print 'starting volume selected' , volume_start
    current_object = random.choice(items_remaining)
    temp_list = list(items_selected)
    print 'weight current object' ,  weights[current_object]
    if weights[current_object] + sum(weight_selected) <= max_weight :
        print ' no weight conflict; we add the object ' 
        temp_list.append(current_object)
        volume_end = [volumes[i] for i in temp_list]
    else:       
        print ' too heavy : we need to remove some objets '          
        temp_list.append(current_object)
        weight_temp= [weights[i] for i in temp_list]
        while sum(weight_temp) > max_weight:
            new_object = random.choice(temp_list)
            temp_list.remove(new_object)
            weight_temp= [weights[i] for i in temp_list]
            volume_end = [volumes[i] for i in temp_list]
        print 'after removing objects weight_selected : ' , weight_temp
    delta = sum(volume_end) - sum(volume_start)
    print 'delta : ' , delta 
    if  delta > 0 or (delta < 0 and random.random() < np.exp(delta/float(t))):
        items_selected = list(temp_list)
    
    return items_selected

def simulatedAnnealing(weights,max_weight,volumes,t0,a,nb_steps):
    t = t0
    n = len(weights)
    items_selected = [random.randint(0,n-1)]
    best_ixs = []
    best_volumes = [volumes[i] for i in best_ixs]
    for i in range(nb_steps):
            print 'step' , i
            items_selected = simulatedAnnealingStep(weights,max_weight,volumes,items_selected,t)
            print 'new item_selected : ' , items_selected
            t = a*t
            new_volumes = [volumes[i] for i in items_selected]
            if sum(best_volumes) < sum(new_volumes):
                best_ixs = items_selected
    return {'best_ixs':best_ixs , 'best_value':sum([volumes[i] for i in best_ixs]),
    'best_sum_weight':sum([weights[i] for i in best_ixs])}
     
volumes = [44,23,19,28,14]
weights = [19,8,7,11,6]
capacities = [5,8,2,2,14]
max_weight = 25

###############  tests ####################

sim = simulatedAnnealing(weights,max_weight,volumes,100,0.9,50)
print sim
