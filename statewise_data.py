import requests
import csv
import json
import pandas as pd
import os
from pandas import DataFrame as df
from nameCorrection import name_correction

JSON_URL = 'https://api.covid19india.org/v4/min/timeseries-MH.min.json'
URL = 'https://api.covid19india.org/v4/min/timeseries-'
EXT = '.min.json'
JSON_INDIA = 'https://api.covid19india.org/v4/min/timeseries.min.json'
DIR_NAME = 'Indian_Cities_Stateswise'

state_name = []


req_date = requests.get(JSON_URL)
req_India = requests.get(JSON_INDIA)

stateNames = df(req_India.json())
statesData = stateNames.T

for st in statesData.index:
    state_name.append(st)

unwanted_st = {'UN', 'TT', 'Other State', 'Other Region', 'Other', 'Unknown'} 
state_name = [ele for ele in state_name if ele not in unwanted_st]


    

dtcolNames =[]


dates = df(req_date.json()['MH']['districts']['Mumbai'])
for dt in dates.index:
    dtcolNames.append(dt + ",")


dir_path = os.path.isdir(DIR_NAME)
if not dir_path:
    os.mkdir(DIR_NAME)


for st in state_name:
    st_name = name_correction(st)
    
    state_dir = st_name.replace(' ', '_')
    state_dir_path = DIR_NAME + "/" + state_dir
    isdir = os.path.isdir(state_dir_path)
    if not isdir:
        os.mkdir(state_dir_path)
        
   
    dist_name  = []
    covidData =[]
    covidRec = []
    covidDeath = []
  
    JSON_URL = URL + st + EXT
    req = requests.get(JSON_URL)
  
    distNames = df(req.json())
    if 'districts' in distNames.index:
        distNames = df(req.json()[st]['districts'])
        distNames = distNames.T

        for dis in distNames.index:
            #print (st + " : " + dis)
            dist_name.append(dis)
 
  
        # items to be removed 
        unwanted_elem = {'Foreign Evacuees', 'Other State', 'Other Region', 'Others', 'Other', 'Unknown'} 
  
        dist_name = [ele for ele in dist_name if ele not in unwanted_elem]
            
        file_t = DIR_NAME + "/" + state_dir + "/" + state_dir + '_total_confirmed_cases.csv'
        file_r = DIR_NAME + "/" + state_dir + "/" + state_dir + '_total_recovered_cases.csv'
        file_d = DIR_NAME + "/" + state_dir + "/" + state_dir + '_total_Death_toll.csv'
                        
               
                
         
        for dist  in dist_name:   
            
            i=0
            covidData.append('\n')
            covidData.append(st_name + "," + st + "," + dist + ",")
            
            covidRec.append('\n')
            covidRec.append(st_name + "," + st + "," + dist + ",")
            
            covidDeath.append('\n')
            covidDeath.append(st_name + "," + st + "," + dist + ",")
    
            covid = df(req.json()[st]['districts'][dist])
            
            
            for conf, dt in zip(covid.dates, covid.index):
                dt = dt + ","
                i+=1
                index = dtcolNames.index(dt) + 1
                if i!= index:
                    #print(st + ":" + dist + ":" + dt + ":  Ind: " + str(index) + ":" +  "i :" + str(i))
                    if i == 1:
                        for n in range(index-1):
                            covidData.append("0,")
                            covidRec.append("0,")
                            covidDeath.append("0,")
                    else:    
                        for n in range(index-i+1):
                            covidData.append("0,")
                            covidRec.append("0,")
                            covidDeath.append("0,")
                            
                    i = index
                
               
                    
                for t in conf.keys():
                    if 'total' in t:
                        if 'confirmed' in (conf['total'].keys()):
                            covidData.append(str(conf['total']['confirmed']) + ",")
                        if not 'confirmed' in (conf['total'].keys()):
                            covidData.append("0,")
                    
                        if 'recovered' in (conf['total'].keys()):
                            covidRec.append(str(conf['total']['recovered']) + ",")
                        if not 'recovered' in (conf['total'].keys()):
                            covidRec.append("0,")
                    
                        if 'deceased' in (conf['total'].keys()):
                            covidDeath.append(str(conf['total']['deceased']) + ",")
                        if not 'deceased' in (conf['total'].keys()):
                            covidDeath.append("0,")
            
                            
            # Data updatation for NODATA
          
            if dt != dtcolNames[len(dtcolNames)-1]:
                diff = len(dtcolNames) - dtcolNames.index(dt)
                for n in range(diff):
                    covidData.append(covidData[len(covidData)-1])
                    covidDeath.append(covidDeath[len(covidRec)-1])
                covidRec.append(covidRec[len(covidRec)-1])
            
       
            
            with open(file_t, 'w') as f:
                f.writelines("State, State Code, Cities,")
                f.writelines(dtcolNames)
                f.writelines(covidData)
        
            with open(file_r, 'w') as f:
                f.writelines("State, State Code, Cities,")
                f.writelines(dtcolNames)
                f.writelines(covidRec)
    
            with open(file_d, 'w') as f:
                f.writelines("State, State Code, Cities,")
                f.writelines(dtcolNames)
                f.writelines(covidDeath)            
        
    else:
        print("State without sistrict's data : "+ st)
    
        
    
    
    
