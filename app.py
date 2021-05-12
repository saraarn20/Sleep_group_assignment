import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import glob
import matplotlib
import matplotlib.pyplot as plt


# Read file
morning_csv = pd.read_csv("./app_data/MorningSleepDiary.csv")
evening_csv = pd.read_csv("./app_data/EveningSleepDiary.csv")
morning_df = pd.DataFrame(morning_csv)

TST = {}
TIB = {}
SE = {}
WASO = {}
SOL = {}


def to_minutes(value):
  return ((value/60)/60)%24 * 60

def duration(val1, val2):
  return to_minutes(val2) - to_minutes(val1)

for i in range(len(morning_df)):
  if morning_df.iat[i, 19] not in TST:
    TST[morning_df.iat[i, 19]] = []
    SE[morning_df.iat[i, 19]] = []
    WASO[morning_df.iat[i, 19]] = []
    SOL[morning_df.iat[i, 19]] = []
    TIB[morning_df.iat[i, 19]] = []
  
  # TST
  TST_val = to_minutes(morning_df.iat[i, 11])
  print(TST)
  if TST_val == 0:
    continue

  TST[morning_df.iat[i, 19]].append(TST_val)
  print(TST)

  # TIB 
  TIB_val = duration(morning_df.iat[i, 10], morning_df.iat[i, 0])
  TIB[morning_df.iat[i, 19]].append(TIB_val)
  print(TIB)

  # SOL
  SOL_val = duration(morning_df.iat[i, 3], morning_df.iat[i, 0])
  SOL[morning_df.iat[i, 19]].append(SOL_val)

  # WASO
  WASO_val = duration(morning_df.iat[i, 5], morning_df.iat[i, 0])
  WASO[morning_df.iat[i, 19]].append(WASO_val)

  # TASAFA
  TASAFA_val = duration(morning_df.iat[i, 6], morning_df.iat[i, 10])
  print(TASAFA_val)

  DSE = SOL_val + TST_val + WASO_val + TASAFA_val
  SE_val = (TST_val / DSE) * 100
  SE[morning_df.iat[i, 19]].append(SE_val)



def av_dic(d):
  avgDict = {}
  for k,v in d.items():
    avgDict[k] = sum(v)/ float(len(v))
  return avgDict


#average 
TST_average = {}
SE_average = {}
WASO_average = {}
SOL_average = {}
TIB_average = {}


for key in TST.keys():
  TST_average[key] = sum(TST[key]) / len(TST[key]) 
  SE_average[key] = sum(SE[key]) / len(SE[key]) 
  WASO_average[key] = sum(WASO[key]) / len(WASO[key]) 
  SOL_average[key] = sum(SOL[key]) / len(SOL[key]) 
  TIB_average[key] = sum(TIB[key]) / len(TIB[key]) 

  f = open("SE_app_Results.txt", "a")
  f.write("SUBJECT: " + str(key))
  f.write('\n')
  f.write("TST_average: " + str(TST_average[key]))
  f.write("TST: " + str(TST[key]))
  f.write('\n')
  f.write("SE_average: " + str(SE_average[key]))
  f.write("SE: " + str(SE[key]))
  f.write('\n')
  f.write("WASO_average: " + str(WASO_average[key]))
  f.write("WASO: " + str(WASO[key]))
  f.write('\n')
  f.write("SOL_average: " + str(SOL_average[key]))
  f.write("SOL: " + str(SOL[key]))
  f.write('\n')
  f.write("TIB_average: " + str(TIB_average[key]))
  f.write("TIB: " + str(TIB[key]))
  f.write('\n')
  f.write('\n')
  f.close()



  





