import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import glob
import matplotlib
import matplotlib.pyplot as plt


# Read file
morning_csv = pd.read_csv("./app_data/MorningSleepDiary.csv")
evening_csv = pd.read_csv("./app_data/EveningSleepDiary.csv")
# morning_csv = pd.read_csv("./strange_app.csv")
morning_df = pd.DataFrame(morning_csv)

TST = {}
TIB = {}
SE = {}
WASO = {}
SOL = {}

full_count = 0
total_count = 0
analysed_subjects = 0
day_count = {}
TOTAL_DAYS = 0 

mapping = {
"642f782b-00f7-47aa-94f1-620d14722184": "SRI 0200",
"7d926fb7-e8d9-45c7-85f2-2a380fb3861a": "SRI 0202",
"79da6eaa-ac9b-4085-901b-a4bb4eeb2bcf": "SRI 0203",
"f63893c4-d456-46bf-b071-b8a3bc219c04": "SRI 0204",
"b98c56cd-64d3-40e7-a287-7d04ccacfb8f": "SRI 0205",
"93419595-76a7-4f1c-a0a5-da415e83f6a7": "SRI 0206",
"f2b01c24-c77b-4146-b84e-5405ea4c83b0": "SRI 0207",
"0150bbcd-b6de-4af0-b528-cb2be7a3a242": "SRI 0208",
"b42387a1-14c6-47c0-9c3d-8acf3d37712a": "SRI 0209",
"b1c64377-8d37-4e11-83bc-1fc86f0bea7f": "SRI 0210",
"8601f265-1ddd-4e31-a963-3241ccec305f": "SRI 0211",
"885901a8-c02d-402e-b362-d70cc79f1c77": "SRI 0212",
"24ff1797-1688-4ea5-870a-575d4637a80e": "SRI 0213",
"33a5fe5f-3ea8-47b1-ad73-25f43240cda6": "SRI 0214",
"a7d3746f-3d16-49f3-9503-97d4b736e8df": "SRI 0216",
"fb980b2f-6cfb-471f-931e-03899ec83e1d": "SRI 0217"
}
def to_minutes(value):
  value = value / 10000000
  return ((value/60)/60)%24 * 60

def duration(val1, val2):
  return abs(to_minutes(val2) - to_minutes(val1))

for i in range(len(morning_df)):
  if morning_df.iat[i, 19] not in TST:
    analysed_subjects = analysed_subjects + 1
    TST[morning_df.iat[i, 19]] = []
    SE[morning_df.iat[i, 19]] = []
    WASO[morning_df.iat[i, 19]] = []
    SOL[morning_df.iat[i, 19]] = []
    TIB[morning_df.iat[i, 19]] = []
  
  # TST
  TST_val = to_minutes(morning_df.iat[i, 11])
  print("------")
  print(TST)

  if TST_val == 0:
    print("error", TST_val, morning_df.iat[i, 11])
    continue

  day = (morning_df.iat[i, 2] / 10000000) % 365
  if day not in day_count:
    day_count[day] = 0
  day_count[day] = day_count[day] + 1
  
  full_count += 1
  TST[morning_df.iat[i, 19]].append(TST_val)
  print(TST)

  # TIB 

  TIB_val = duration(morning_df.iat[i, 10], morning_df.iat[i, 0])

  TIB[morning_df.iat[i, 19]].append(TIB_val)
  print(TIB)

  # SOL
  print()
  SOL_val = to_minutes(morning_df.iat[i, 3])
  SOL[morning_df.iat[i, 19]].append(SOL_val)

  # WASO
  WASO_val = duration(morning_df.iat[i, 5], morning_df.iat[i, 0])
  WASO_val = to_minutes(morning_df.iat[i, 5])
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

print("full_count", full_count)
print("analysed_subjects", analysed_subjects)


f = open("SE_app_Results.txt", "w")
f.write("")
f.close()

app_se = {}

day_count_average = []
for key in TST.keys():
  TST_average[key] = sum(TST[key]) / len(TST[key]) 
  SE_average[key] = sum(SE[key]) / len(SE[key]) 
  WASO_average[key] = sum(WASO[key]) / len(WASO[key]) 
  SOL_average[key] = sum(SOL[key]) / len(SOL[key]) 
  TIB_average[key] = sum(TIB[key]) / len(TIB[key]) 
  day_count_average.append(len(TST[key]) / 7)
  app_se[mapping[key]] = SE_average[key]
  # print('mapping[key]', mapping[key])
  
  f = open("SE_app_Results.txt", "a")
  f.write("SUBJECT: " + str(mapping[key]))
  f.write('\n')
  f.write("Filled out days for subject during the app period: " + str(len(TST[key])))
  f.write('\n')
  f.write("TST_average: " + str(TST_average[key]))
  f.write('\n')
  f.write("TST: " + str(TST[key]))
  f.write('\n')
  f.write("SE_average: " + str(SE_average[key]))
  f.write('\n')
  f.write("SE: " + str(SE[key]))
  f.write('\n')
  f.write("WASO_average: " + str(WASO_average[key]))
  f.write('\n')
  f.write("WASO: " + str(WASO[key]))
  f.write('\n')
  f.write("SOL_average: " + str(SOL_average[key]))
  f.write('\n')
  f.write("SOL: " + str(SOL[key]))
  f.write('\n')
  f.write("TIB_average: " + str(TIB_average[key]))
  f.write('\n')
  f.write("TIB: " + str(TIB[key]))
  f.write('\n')
  f.write('\n')
  f.close()


print(day_count_average)
print(sum(day_count_average) / len(day_count_average))

# compare app and 
print('===========================')

paper_se = {
'SRI 0207': 88.58950031625554,
'SRI 0208': 94.50638896467304,
'SRI 0205': 93.81432838676072,
'SRI 0209': 82.97546051867248,
'SRI 0214': 95.08349926247257,
'SRI 0200': 84.85883522850102,
'SRI 0203': 83.74545220387004,
'SRI 0216': 95.04414103934853,
'SRI 0202': 72.83593599383073,
'SRI 0217': 94.24226825565192,
'SRI 0210': 89.6551186017478,
'SRI 0211': 81.71052631578947,
'SRI 0213': 95.95675234598123,
# 'SRI 0215': 81.77435353905942
}

del app_se['SRI 0204']
del app_se['SRI 0206']
del app_se['SRI 0212']

print('====================')
print(len(paper_se))
print('====================')
print(len(app_se))
print('====================')

# # SL plot
# plt.figure(figsize=(14, 7))
# X = np.arange(len(app_se))
# colors = {'SE from app diary':'b', 'SE from paper diary':'r'}         
# labels = list(colors.keys())
# handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
# plt.legend(handles, labels)

# plt.bar(X-0.125, app_se.values(), align='center', color = 'b', width = 0.25, label='SL from SAS')
# plt.bar(X+0.125, paper_se.values(), align='center', color = 'r', width = 0.25, label='SL from Sleep Diary')
# plt.xticks(X, list(app_se.keys()))

# plt.xlabel('Subjects (Research Number)')
# plt.ylabel('SE (%)')
# plt.title('Comparison of SE from Paper and App Diary')

# plt.savefig('app_vs_paper.png')

print('======YOO')
print(app_se)
print(paper_se)
print('======')

app_se_list = []
paper_se_list = []
indexes = []
i = 1

for key in paper_se.keys():
  print(key, app_se[key], paper_se[key])
  app_se_list.append(app_se[key])
  paper_se_list.append(paper_se[key])
  indexes.append(str(i))
  i += 1

print(paper_se_list)
print(app_se_list)
plotdata = pd.DataFrame({
    "SE from Paper Diary": paper_se_list,
    "SE from App Diary": app_se_list
    }, 
    index=indexes
)

plotdata.plot(kind="bar")
plt.title("Mince Pie Consumption Study")
plt.xlabel("Subject")
plt.ylabel("Sleep Efficiency (SE)")

plt.savefig('app_vs_paper_df.png')