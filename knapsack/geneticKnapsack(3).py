# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 17:33:57 2015

@author: root
"""
import random 
import numpy as np
from collections import Counter

def flipUntilpossible(weights,max_weight,chromosome):
    n = len(weights)
    weight_chrom = [weights[i] for i in range(n) if chromosome[i]==1]
    while sum(weight_chrom) > max_weight:
        chromosome_ix_of_ones = [i for i in range(n) if chromosome[i] == 1]
        ix_swich = random.choice(chromosome_ix_of_ones)
        chromosome[ix_swich] = 0
        weight_chrom = [weights[i] for i in range(len(weights)) if chromosome[i]==1] 
    return chromosome
    
#we perform single point crossover
def crossOver(chr1,chr2):
    n = len(chr1)
    ix_crossover = random.randint(0,n-1)
    #print 'ix cross ' , ix_crossover
    new_chr_11 = chr1[:ix_crossover]
    new_chr_12 = chr1[ix_crossover:]
    new_chr_21 = chr2[:ix_crossover]
    new_chr_22 = chr2[ix_crossover:]
    #print new_chr_12
    new_chr_11.extend(new_chr_22)
    new_chr_21.extend(new_chr_12)
    return {'new_chr_1':new_chr_11 , 'new_chr_2':new_chr_21 , 'ix_cross':ix_crossover}

def newGeneration(percentage,list_chrom):
    population_size = len(list_chrom)
    number_crossover = np.round(percentage*population_size)  
    if number_crossover%2 == 1:
        number_crossover+=1  
    print 'number of crossover : ' , number_crossover
    chrom_crossovered_ix = random.sample(range(population_size),int(number_crossover))
    chrom_crossovered = [list_chrom[i] for i in chrom_crossovered_ix ]
    chrom_untouched_ix = [i for i in range(population_size) if i not in chrom_crossovered_ix]
    chrom_untouched = [list_chrom[i] for i in chrom_untouched_ix ]
    for i in range(int(number_crossover/2)):
        chr1,chr2 = chrom_crossovered[i],chrom_crossovered[i+1]
        print 'chr1', chr1 , 'chr2' , chr2
        cr = crossOver(chr1,chr2)
        new1,new2,ix_cross = cr['new_chr_1'], cr['new_chr_2'], cr['ix_cross']
        print 'ix_cross', ix_cross        
        print 'new1', new1 , 'new2' , new2
        chrom_untouched.append(new1)
        chrom_untouched.append(new2)
    return chrom_untouched
    
def wheelSelection(list_chrom):
    sum_fitness = sum([fitnessValue(ch,weights) for ch in list_chrom ])
    #print 'sum_fitness' , sum_fitness
    population_size = len(list_chrom)
    limit = random.randint(0, sum_fitness)  
    #print 'limit' ,limit
    current_total_fitness = 0
    i = 0
    while current_total_fitness < limit and i < population_size :
        #print 'current before' ,current_total_fitness
        current_total_fitness+= fitnessValue(list_chrom[i],weights)
        #print 'chrom ' , list_chrom[i]
        #print 'current after' ,current_total_fitness
        i+=1
    chrom_1_selected = list_chrom[i-1]
    #print 'chrom1', chrom_1_selected 
    list_chrom.pop(i-1)
    #print '############ phase 2 ##################'
    sum_fitness = sum([fitnessValue(ch,weights) for ch in list_chrom ])
    #print 'sum_fitness' , sum_fitness
    population_size = len(list_chrom)
    limit = random.randint(0, sum_fitness)  
    #print 'limit' ,limit
    current_total_fitness = 0
    i = 0
    while current_total_fitness < limit and i < population_size :
        #print 'current before' ,current_total_fitness
        current_total_fitness+= fitnessValue(list_chrom[i],weights)
        #print 'chrom ' , list_chrom[i]
        #print 'current after' ,current_total_fitness
        i+=1   
    chrom_2_selected = list_chrom[i-1]
    #print 'chrom2', chrom_2_selected
    list_chrom.pop(i-1)
    return {'chrom1':chrom_1_selected , 'chrom2': chrom_2_selected,'list_without_2':list_chrom}
    
# we perform mutation on each bit with probability 0.1
def mutation(chrom):
    new_chrom = []
    n = len(chrom)
    for i in range(n):
        if random.random() < 0.1 :
            new_chrom.append(1-chrom[i])
        else:
            new_chrom.append(chrom[i])
    return new_chrom

def fitnessValue(chromosome,weights):
    n = len(chromosome)
    weights_objects_taken = [weights[i] for i in range(n) if chromosome[i]==1]
    return sum(weights_objects_taken)

def isPopulationFit(chrom_list,weights):
    #first we make the chromosomes possible
    #print' list before ' , chrom_list
    chrom_list = [flipUntilpossible(weights,max_weight,ch) for ch in chrom_list]
    #print' list after ' , chrom_list    
    fit_value = [fitnessValue(chrom,weights)for chrom in chrom_list]
    counts = Counter(fit_value) 
    most_common = counts.most_common(1)  
    print ' most common element ' , most_common
    print 'percentage ' , most_common[0][1]/float(len(chrom_list))
    if most_common[0][1]/float(len(chrom_list)) > 0.9:
        return True
    else:
        return False
        

def geneticKnapsack(weights,max_weight,volumes,N,nb_generation_min,nb_generation_max):
    n = len(weights)
    chrom_list = [[random.randint(0,1) for k in range(n)]for k2 in range(N)]
    print 'start list' , chrom_list
    chrom_list = [flipUntilpossible(weights,max_weight,ch) for ch in chrom_list]
    print 'start possible list' , chrom_list
    nb_generation = 0  
    while (nb_generation < nb_generation_min and nb_generation >=nb_generation_max) and not isPopulationFit(chrom_list,weights):
        #print 'old chrom list' , chrom_list          
        nb_generation+=1
        wheel = wheelSelection(chrom_list)
        chrom1,chrom2,list_without_2 = wheel['chrom1'],wheel['chrom2'],wheel['list_without_2']
        #print 'old chr ' , chrom1 , chrom2
        cross = crossOver(chrom1,chrom2)
        new1,new2 = cross['new_chr_1'],cross['new_chr_2']
        #print 'new chr ' , new1,new2 , 'ix' , cross['ix_cross']
        list_without_2.append(new1)
        list_without_2.append(new2)
        chrom_list = list(list_without_2)
        #print 'new chrom list ' , chrom_list
    return chrom_list
    

########## tests #######################   
     
volumes = [44,23,19,28,14]
weights = [19,8,7,11,6]
capacities = [5,8,2,2,14]
max_weight = 25
N = 6
nb_steps = 5


ga = geneticKnapsack(weights,max_weight,volumes,N,2,100) 
#chro = flipUntilpossible(weights,max_weight,[1,1,1,1,1])
#cross =  crossOver([1,1,1,0,0],[1,0,0,1,1])                        
#new_cr = mutation([1,1,1,0,1])
#fitness_value = fitnessValue([0,1,1,0,1],weights)
#list_chrom = [[random.randint(0,1) for k in range(len(weights))]for k2 in range(N)]
#cross2 = newGeneration(0.85,list_chrom)
#isFit =  isPopulationFit(list_chrom,weights)
#wheel = wheelSelection(list_chrom)


def volume(chromosome,volumes):
    n = len(chromosome)
    volumes_objects_taken = [volumes[i] for i in range(n) if chromosome[i]==1]
    return sum(volumes_objects_taken)

for ch in ga:
    print volume(ch,volumes)
