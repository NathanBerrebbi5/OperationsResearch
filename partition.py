"""
author: Nathan Berrebbi

Overview: deciding whether a given multiset S of positive integers can be partitioned
into two subsets S1 and S2 such that the sum of the numbers
in S1 equals the sum of the numbers in S2
This is a NP-Complete problem

More details here:
https://en.wikipedia.org/wiki/Partition_problem

"""
import numpy as np

"""
partition is a dynamic programming algorithm
We populate recursively the table P
p(i, j) be True if a subset of { x1, ..., xj } sums to i and False otherwise.
p(i, j) is True if either p(i, j − 1) is True or if p(i − xj, j − 1) is True
p(i, j) is False otherwise
"""

#OUTPUT: True if S can be partitioned into two subsets that have equal sum
#This algorithm doesn't give the actual partitition S1 and S2

def patition(integer_list):
     n = len(integer_list)
     N = sum(integer_list)
     P  = [[False for k1 in range(n+1)] for k2 in range(int(np.floor(N/2))+ 1)] 
     for j in range(n+1):
        P[0][j] = True                
     P[0][0] = True
     #initialize top row (P(0,x)) of P to True 
     #nitialize leftmost column (P(x, 0)) of P to False    
     for i in range(1,int(np.floor(N/2))+1):
         for j in range(1,n+1):             
             if integer_list[j - 1] <= i :
                 P[i][j] =  P[i][j-1] or  P[i-integer_list[j-1]][j-1]
             else:
                 P[i][j] =  P[i][j-1]
     return {'partition':P,'result_bool':P[int(np.floor(N/2))-1][n-1]}


# The greedy algorithm does the following:
#It first sorts the integer by decreasing order
#and then assign the integer to the set that has the smallest sum
def greedyHeuristic(integer_list):    
     A = []
     B = []
     integer_list_sorted = sorted(integer_list , key=lambda x:-x)    
     for element in integer_list_sorted:
         if sum(A) <= sum(B):
             A.append(element)
         else:
             B.append(element)
     return {'A': A , 'B':B}


########## tests ########################
     
integer_list = [3, 1, 1, 2, 2, 1]
part =  patition(integer_list)     
part_greedy = greedyHeuristic(integer_list)
    