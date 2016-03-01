"""
author Nathan Berrebbi

"""
import numpy as np
import random

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"


def possibleNextObject(current_knapsack_ix,weights,max_weight):
    n = len(weights)
    current_weight = sum([weights[i] for i in current_knapsack_ix ])
    possible_obj = []    
    for i in range(n):
        if i not in current_knapsack_ix and weights[i] + current_weight <= max_weight:
            possible_obj.append(i)
    return possible_obj

def antsKnapsack(weights,volumes,max_weight,nb_cycles,nb_ants,alpha,beta,evap_coef):
   n = len(weights)
   tau = [1 for i in range(n)]
   mu = [float(volumes[i])/(weights[i]*weights[i]) for i in range(n)]
   best_volume_global = 0
   best_items_global = []
   while nb_cycles > 0 :
        print 'nb cycles remaining' , nb_cycles       
        nb_cycles-=1
        nb_remaining_ants = nb_ants
        while nb_remaining_ants >0 :
            print '############## nb ants remaining ############' , nb_remaining_ants        
            nb_remaining_ants-=1
            best_volume_ant = 0
            best_items_ants = []
            selected_items = []
            weight_selected = [weights[i] for i in selected_items]           
            neighboring_objects = range(n)
            while sum(weight_selected) < max_weight and len(neighboring_objects)>0:
                proba_neighbor = []
                denominator = sum([np.power(tau[k],alpha)*np.power(mu[k],beta) for k in neighboring_objects ])
                #print 'den list ' , [np.power(tau[k],alpha)*np.power(mu[k],beta) for k in neighboring_objects ]
                for j in neighboring_objects:   #we construc the proba list                 
                    numerator = np.power(tau[j],alpha)*np.power(mu[j],beta)
                    proba_neighbor.append({'j':j , 'pr':float(numerator)/denominator})
                    choices = [(p['j'],p['pr']) for p in proba_neighbor]
                #population = [val for val, cnt in weighted_choices for i in range(int(cnt))]
                #print 'population' , population
                chosen_j = weighted_choice(choices)              
                print 'chosen_j' , chosen_j
                selected_items.append(chosen_j)
                weight_selected = [weights[i] for i in selected_items]
                neighboring_objects = possibleNextObject(selected_items,weights,max_weight) 
                print 'neighb objects' , neighboring_objects
            print 'selected items ' , selected_items
            total_volume = sum([volumes[i] for i in selected_items ])
            print 'total_volume ' , total_volume
            if total_volume > best_volume_ant:
                best_volume_ant = total_volume 
                best_items_ants = selected_items
        if best_volume_global < best_volume_ant:
            best_volume_global = best_volume_ant
            best_items_global = best_items_ants
        tau = [evap_coef * t for t in tau] #evporation
        delta = [float(1)/(1+(best_volume_global-v)/float(best_volume_global)) for v in volumes]
        #print 'new delta ' , delta
        tau = [tau[i] + delta[i] for i in range(len(tau))]
        print 'new tau ' , tau
   return {'best_volume':best_volume_global , 'best_items':best_items_global}            
              
############ tests #####################################
                
volumes = [44,23,19,28,14]
weights = [19,8,7,11,6]
max_weight = 25
nb_cycles = 4
nb_ants = 2
alpha,beta = 1 , 1
evap_coef = 0.8


possible = possibleNextObject([3,4],weights,max_weight)
ants = antsKnapsack(weights,volumes,max_weight,nb_cycles,nb_ants,alpha,beta,evap_coef)
   


