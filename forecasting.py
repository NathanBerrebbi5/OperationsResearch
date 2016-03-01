"""
author: Nathan Berrebbi

Time Series forecasting methods including:
- moving average
- exponential smoothing
- Holt Winters method

For each method, the forecast accuracy is measured by 3 metrics:
- mae: Mean Absolute Error
- mse: Mean Squarred Error
- mape: Mean Absolute Percentage Error

More details here:
https://en.wikipedia.org/wiki/Mean_absolute_error
https://en.wikipedia.org/wiki/Mean_squared_error
https://en.wikipedia.org/wiki/Mean_absolute_percentage_error

"""
import numpy as np

def movingAverage(n , demand_list):    
    forecast_dem = list(np.zeros(len(demand_list)))
    error = list(np.zeros(len(demand_list)))
    mape_error = list(np.zeros(len(demand_list)))
    for i in range(n,len(demand_list)):
        forecast_dem[i] = np.rint(sum(demand_list[i-n:i])/float(n))
        error[i] = forecast_dem[i] - demand_list[i]
        mape_error[i] = abs(error[i])/demand_list[i]
    abs_error = [abs(e) for e in error ]
    square_error = [e*e for e in error ]    
    mae = sum(abs_error)/(len(demand_list)-n)
    mse = sum(square_error)/(len(demand_list)-n)
    mape = 100*sum(mape_error)/(len(demand_list)-n)
    return {'forecast_dem':forecast_dem , 'mae':mae , 'mse':mse , 'mape':mape} 


def exponSmoothing(alpha , demand_list):
    forecast_dem = list(np.zeros(len(demand_list)))
    error = list(np.zeros(len(demand_list)))
    mape_error = list(np.zeros(len(demand_list)))
    forecast_dem[0] = demand_list[0]
    for i in range(1,len(demand_list)):
        forecast_dem[i] = np.round( (1-alpha)*forecast_dem[i-1]+ alpha*demand_list[i-1] )
        error[i] = forecast_dem[i] - demand_list[i]
        mape_error[i] = abs(error[i])/demand_list[i]
    abs_error = [abs(e) for e in error ]
    square_error = [e*e for e in error ]    
    mae = sum(abs_error)/len(demand_list)
    mse = sum(square_error)/len(demand_list)
    mape = 100*sum(mape_error)/len(demand_list)
    return {'forecast_dem':forecast_dem , 'mae':mae , 'mse':mse , 'mape':mape}      
 

def linearReg(demand_list):
    n = len(demand_list)
    x = range(1,n+1)
    y= demand_list
    return np.polyfit(x,y,1)


def HoltMethod(alpha,beta,demand_list):
    
    s0 = linearReg(demand_list)[1]
    g0 = linearReg(demand_list)[0]    
    s_list =[s0]
    g_list =[g0]
    forecast_dem = [s0+g0]
    error = list(np.zeros(len(demand_list)))
    mape_error = list(np.zeros(len(demand_list)))    
    for i in range(1,len(demand_list)):
               s_list.append(alpha*demand_list[i-1]+(1-alpha)*(s_list[i-1]+g_list[i-1]))
               #print s_list[i]
               g_list.append(beta*(s_list[i]-s_list[i-1])+(1-beta)*g_list[i-1])
               forecast_dem.append(s_list[i]+g_list[i])
               error[i] = forecast_dem[i] - demand_list[i]
               mape_error[i] = abs(error[i])/demand_list[i]
    abs_error = [abs(e) for e in error ]
    square_error = [e*e for e in error ]    
    mae = sum(abs_error)/len(demand_list)
    mse = sum(square_error)/len(demand_list)
    mape = 100*sum(mape_error)/len(demand_list)
    return {'forecast_dem':forecast_dem , 'mae':mae , 'mse':mse , 'mape':mape}
 

################  tests ############################################# 

demand = [200,250,175,186,225,285,305,190]
forecast_ma = movingAverage(3,demand)
forecast_es = exponSmoothing(0.1,demand)                 
forecast_holt = HoltMethod(0.1,0.1,demand)             

 
 
 