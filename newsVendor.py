"""
author Nathan Berrebbi
https://en.wikipedia.org/wiki/Newsvendor_model
"""

from scipy.stats import norm
import numpy as np

def eoq(K,h,d ,c):
    q_opt = np.sqrt(2*K*d/h)
    cost_opt = np.sqrt(2*K*d*h) + c*d
    return {'q_opt':q_opt , 'cost_opt':cost_opt}
    
def epq(K,h,d,p,c):
    if p < d :
        return ' unfeasible '
    else:
        q_opt = np.sqrt(2*K*d/h) * np.sqrt(p/(p-d))
        cost_opt = np.sqrt(2*K*d*h)*np.sqrt(p/(p-d)) + c*d 
        return {'q_opt':q_opt , 'cost_opt':cost_opt}


def newsVendor(cu,co , mu, sigma): # with salvage price
    critical_ratio= float(cu)/(cu+co)
    print critical_ratio
    z = norm.ppf(critical_ratio)
    print z
    q = sigma*z + mu
    return np.round(q)
    

def findR(q,p,h,d_annual,d_lead_time,sigma_lead_time):
    tmp = 1-(q*h)/(p*d_annual)
    #print ('tmp :'+str(tmp))
    z = norm.ppf(tmp)
    return sigma_lead_time*z + d_lead_time 

def findQ(r,K,p,h,d_annual,d_lead_time,sigma_lead_time):
    print ('r:' + str(r))
    z = (r-d_lead_time)/sigma_lead_time
    print ('z : ' + str(z))
    phiZ = np.exp(-(z*z/2))/np.sqrt(2*np.pi)
    Lz = phiZ - z*(1-norm.cdf(z))
    print ('Lz : '+str(Lz))
    nR = sigma_lead_time * Lz
    return np.round(np.sqrt(2*d_annual*(K+p*nR)/h))
    
"""
The algorithm recursively updates Q and R and stops when Q_old = Q_new 
(or when R_old = R_new, this is equivalent)
"""


def QRpolicy(K,h,p ,d_annual , d_lead_time,sigma_lead_time):
    
    q = np.round(np.sqrt(2*K*d_annual/h))
    print ('q0 : ' + str(q))
    r = findR(q,p,h,d_annual,d_lead_time,sigma_lead_time)
    print ('r0 : ' + str(r))
    new_q = findQ(r,K,p,h,d_annual,d_lead_time,sigma_lead_time)
    new_r = findR(new_q,p,h,d_annual,d_lead_time,sigma_lead_time)
    while np.floor(abs(new_q-q)) > 0 :
        q = new_q
        print ('q : ' + str(q))
        new_q = findQ(new_r,K,p,h,d_annual,d_lead_time,sigma_lead_time)
        print ('new_q : ' + str(new_q))
        r = new_r
        print ('r : ' + str(r))
        new_r = findR(new_q,p,h,d_annual,d_lead_time,sigma_lead_time)
        print ('new_r : ' + str(new_r))
    return {'q':new_q , 'r':np.round(new_r)}

 ######## tests ####################      
  
q1 = newsVendor(40,50,5000,2000)
res = QRpolicy(15,1.8,10,336,90,14.38)
res2 = QRpolicy(70,0.6,1.5,10000,300,40)