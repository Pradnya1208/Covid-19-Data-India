import requests
import csv
import json
import pandas as pd
from pandas import DataFrame as df
import os
from nameCorrection import name_correction

JSON_URL = 'https://api.covid19india.org/v4/min/timeseries.min.json'

DIR_NAME = 'Indian_States'

state_name  = []
dtcolNames =[]
covidData =[]
covidRec = []
covidDeath = []


#df = pd.read_json(JSON_URL)
req = requests.get(JSON_URL)


stateNames = df(req.json())
statesData = stateNames.T


for st in statesData.index:
    state_name.append(st)

unwanted_st = {'UN', 'Other State', 'Other Region', 'Other', 'Unknown'} 
state_name = [ele for ele in state_name if ele not in unwanted_st]


# # In case of fixed Dates
date_ = df(req.json()['TT'])
for dt in date_.index:
    dtcolNames.append(dt + ",")
    
dir_path = os.path.isdir(DIR_NAME)
if not dir_path:
    os.mkdir(DIR_NAME)

for state in state_name:   
    
    st_name = name_correction(state)
    print(st_name)
  
    i=0
    covidData.append('\n')
    covidData.append(st_name + "," + state + "," )
    
    covidRec.append('\n')
    covidRec.append(st_name + "," + state + "," )
    
    covidDeath.append('\n')
    covidDeath.append(st_name + "," + state + "," )
    
    covid = df(req.json()[state])

     
            
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
          
    if dt != dtcolNames[len(dtcolNames)-1]:
          diff = len(dtcolNames) - dtcolNames.index(dt)
          for n in range(diff):
              covidData.append(covidData[len(covidData)-1])
              covidDeath.append(covidDeath[len(covidRec)-1])
              covidRec.append(covidRec[len(covidRec)-1])         
# TODO: Delta and no of tests
                                

    
with open(DIR_NAME + '/Indian_States_total_confirmed_cases.csv', 'w') as f:
    f.writelines("State, State Code,")
    f.writelines(dtcolNames)
    f.writelines(covidData)
    
with open(DIR_NAME + '/Indian_States_total_recovered_cases.csv', 'w') as f:
    f.writelines("State, State Code,")
    f.writelines(dtcolNames)
    f.writelines(covidRec)

with open(DIR_NAME + '/Indian_States_total_Death_toll.csv', 'w') as f:
    f.writelines("State, State Code,")
    f.writelines(dtcolNames)
    f.writelines(covidDeath)


    


