import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import glob
import matplotlib
import matplotlib.pyplot as plt


# Read file
sas_csv = pd.read_csv("sas_data clean.csv")
sas_df = pd.DataFrame(sas_csv)

print(sas_df)


def data_to_minutes(data):
  yo = data.split(' ')

  value = int(yo[0])*60
  value = value + int(yo[1])

  return value

TST = {}
SE = {}
WASO = {}
SL = {}


for i in range(len(sas_df)):
  if sas_df.iat[i, 0] in TST:
    TST[sas_df.iat[i, 0]].append(int(data_to_minutes(sas_df.iat[i, 2])))
    SE[sas_df.iat[i, 0]].append(int(sas_df.iat[i, 3]))
    WASO[sas_df.iat[i, 0]].append(int(sas_df.iat[i, 4]))
    SL[sas_df.iat[i, 0]].append(int(sas_df.iat[i, 5]))
  else: 
    TST[sas_df.iat[i, 0]] = [int(data_to_minutes(sas_df.iat[i, 2]))]
    SE[sas_df.iat[i, 0]] = [int(sas_df.iat[i, 3])]
    WASO[sas_df.iat[i, 0]] = [int(sas_df.iat[i, 4])]
    SL[sas_df.iat[i, 0]] = [int(sas_df.iat[i, 5])]
  

#average 
TST_average = {}
SE_average = {}
WASO_average = {}
SL_average = {}


for key in TST.keys():
  TST_average[key] = sum(TST[key]) / len(TST[key]) 
  SE_average[key] = sum(SE[key]) / len(SE[key]) 
  WASO_average[key] = sum(WASO[key]) / len(WASO[key]) 
  SL_average[key] = sum(SL[key]) / len(SL[key]) 

# =============================================
# PLOT
def av_dic(d):
  avgDict = {}
  for k,v in d.items():
    avgDict[k] = sum(v)/ float(len(v))
  return avgDict

SE_dic = {'SRI 0209': [78.46153846153847, 81.35593220338984, 89.10891089108911], 'SRI 0202': [53.84615384615385, 78.94736842105263, 85.71428571428571], 'SRI 0217': [89.36170212765957, 96.5909090909091, 96.7741935483871], 'SRI 0203': [80.95238095238095, 87.93103448275862, 82.35294117647058], 'SRI 0210': [81.25, 93.33333333333333, 94.3820224719101], 'SRI 0205': [94.6236559139785, 97.45762711864407, 89.36170212765957], 'SRI 0211': [92.5, 78.94736842105263, 73.68421052631578], 'SRI 0213': [94.18604651162791, 96.84210526315789, 96.84210526315789]}
TST_dic = {'SRI 0209': [510, 480, 450], 'SRI 0202': [315, 450, 480], 'SRI 0217': [420, 510, 540], 'SRI 0203': [510, 510, 420], 'SRI 0210': [390, 420, 420], 'SRI 0205': [440, 460, 420], 'SRI 0211': [370, 300, 420], 'SRI 0213': [405, 460, 460]}
SL_dic = {'SRI 0209': [60, 20, 40], 'SRI 0202': [60, 30, 20], 'SRI 0217': [15, 15, 15], 'SRI 0203': [20, 10, 60], 'SRI 0210': [60, 15, 15], 'SRI 0205': [10, 5, 5], 'SRI 0211': [20, 30, 15], 'SRI 0213': [10, 10, 10]}
WASO_dic = {'SRI 0209': [20, 0, 0], 'SRI 0202': [120, 60, 60], 'SRI 0217': [20, 3, 3], 'SRI 0203': [30, 30, 30], 'SRI 0210': [20, 10, 5], 'SRI 0205': [10, 2, 20], 'SRI 0211': [10, 30, 15], 'SRI 0213': [15, 5, 5]}

SE_dic_av = av_dic(SE_dic)
TST_dic_av = av_dic(TST_dic)
SL_dic_av = av_dic(SL_dic)
WASO_dic_av = av_dic(WASO_dic)


# TST plot
plt.figure(figsize=(10, 7))
X = np.arange(len(TST_average))
plt.bar(X-0.125, TST_average.values(), align='center', color = 'b', width = 0.25, label='TST from SAS')
plt.bar(X+0.125, TST_dic_av.values(), align='center', color = 'r', width = 0.25, label='TST from Sleep Diary')
plt.xticks(X, list(TST_average.keys()))

plt.xlabel('Subjects (Research Number)')
plt.ylabel('Total Sleep Time (minutes)')
plt.title('Comparison of Total Sleep Time (TST) from SAS and Sleep Diary')

plt.savefig('TST.png')

# SE plot
plt.figure(figsize=(10, 7))
X = np.arange(len(SE_average))
plt.bar(X-0.125, SE_average.values(), align='center', color = 'b', width = 0.25, label='SE from SAS')
plt.bar(X+0.125, SE_dic_av.values(), align='center', color = 'r', width = 0.25, label='SE from Sleep Diary')
plt.xticks(X, list(SE_average.keys()))

plt.xlabel('Subjects (Research Number)')
plt.ylabel('Sleep Efficiency (%)')
plt.title('Comparison of Sleep Efficiency (SE) from SAS and Sleep Diary')

plt.savefig('SE.png')

# WASO plot
plt.figure(figsize=(10, 7))
X = np.arange(len(WASO_average))
plt.bar(X-0.125, WASO_average.values(), align='center', color = 'b', width = 0.25, label='WASO from SAS')
plt.bar(X+0.125, WASO_dic_av.values(), align='center', color = 'r', width = 0.25, label='WASO from Sleep Diary')
plt.xticks(X, list(WASO_average.keys()))

plt.xlabel('Subjects (Research Number)')
plt.ylabel('WASO (minutes)')
plt.title('Comparison of WASO from SAS and Sleep Diary')

plt.savefig('WASO.png')

# SL plot
plt.figure(figsize=(10, 7))
X = np.arange(len(SL_average))
plt.bar(X-0.125, SL_average.values(), align='center', color = 'b', width = 0.25, label='SL from SAS')
plt.bar(X+0.125, SL_dic_av.values(), align='center', color = 'r', width = 0.25, label='SL from Sleep Diary')
plt.xticks(X, list(SL_average.keys()))

plt.xlabel('Subjects (Research Number)')
plt.ylabel('SOL (minutes)')
plt.title('Comparison of SOL from SAS and Sleep Diary')

plt.savefig('SL.png')

print("      =   SAS    |    DIARY")
print('SL', sum(SL_average.values()) / len(SL_average), sum(SL_dic_av.values()) / len(SL_dic_av))
print('SE', sum(SE_average.values()) / len(SE_average), sum(SE_dic_av.values()) / len(SE_dic_av))
print('WASO', sum(WASO_average.values()) / len(WASO_average), sum(WASO_dic_av.values()) / len(WASO_dic_av))
print('TST', sum(TST_average.values()) / len(TST_average), sum(TST_dic_av.values()) / len(TST_dic_av))