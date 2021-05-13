import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import glob
import matplotlib
import matplotlib.pyplot as plt
import statistics

def data_to_minutes(data):
  if data.lower().endswith("klst") or data.lower().endswith("tíma"):
    value = data.split()[0]
    value = int(value)*60
  elif data.lower().endswith("min") or data.endswith("mín"):
    value = data.split()[0]
    value = int(value)
  elif str(data) == "0" or str(data) == "":
    value = 0 
  else: 
    print("ERROR", data)
  return value

TST_dic = {}
SE_dic = {}
WASO_dic = {}
SL_dic = {}

empty_count = 0
full_count = 0
total_count = 0
analysed_subjects = 0
day_count = {}

def analyse_file(csv_file):
  global empty_count
  global full_count
  global total_count
  global analysed_subjects

  # Read file
  sleep_csv = pd.read_csv(csv_file)
  sleep_df = pd.DataFrame(sleep_csv)

  f = open(csv_file, "r")
  subject = f.readline().split(",")[1]
  f.close()
  analysed_subjects += 1

  print('------------------------------------------------')
  print('SUBJECT', subject)
  print(sleep_csv)
  print('------------------------------------------------')

  day = 1
  SE_list = []

  global day_count 

  for day in range(1, 8):
    FMT = '%H:%M'

    # total sleep time 
    TST_total = sleep_df.iat[9,day]
    print(sleep_df.iat[9,day], str(sleep_df.iat[9,day]))

    total_count += 1
    if sleep_df.iat[9,day] == 'x' or sleep_df.iat[9,day] == 0 or sleep_df.iat[9,day] == '' or str(sleep_df.iat[9,day]) == 'nan':
      TST = 'x'
      print('empty entry x', subject)
      empty_count += 1
      continue
    else:
      full_count += 1
      print(TST_total)
      TST = int(TST_total.split(':')[0]) * 60 + int(TST_total.split(':')[1])

    if day not in day_count:
      day_count[day] = 0
    day_count[day] = day_count[day] + 1

    time_to_bed = datetime.strptime(sleep_df.iat[1,day], FMT)
    time_out_of_bed = datetime.strptime(sleep_df.iat[8,day], FMT)


    # If the sleep time is before midnight - prevent negative value.. 
    if time_out_of_bed < time_to_bed:
      time_out_of_bed += timedelta(days=1)

    TIB = time_out_of_bed - time_to_bed
    TIB = TIB.total_seconds() / 60 # set to minutes

    # =======
    # = SOL =
    # =======

    SOL_data = sleep_df.iat[3,day] 
    SOL = data_to_minutes(SOL_data)

    # ========
    # = WASO =
    # ========

    WASO_data = sleep_df.iat[5,day] 
    WASO = data_to_minutes(WASO_data)


    # ==========
    # = TASAFA =
    # ==========

    leaves_bed = datetime.strptime(sleep_df.iat[8,day], FMT) # 7. Klukkan hvað fórstu þú á fætur? 
    final_awake = datetime.strptime(sleep_df.iat[6,day], FMT) # 6.  Klukkan hvað vaknaðir þú endanlega

    if leaves_bed < final_awake:
      leaves_bed += timedelta(days=1)

    TASAFA = leaves_bed - final_awake
    TASAFA = TASAFA.total_seconds() / 60 # set to minutes


    # ==============================
    # = Calculate Sleep Efficiency =
    # ==============================

    DSE = SOL + TST + WASO + TASAFA
    SE = (TST / DSE) * 100
    SE_list.append(SE)

    if subject in TST_dic:
      TST_dic[subject].append(TST)
      SL_dic[subject].append(SOL)
      WASO_dic[subject].append(WASO)
      SE_dic[subject].append(SE)
    else: 
      TST_dic[subject] = [TST]
      SL_dic[subject] = [SOL]
      WASO_dic[subject] = [WASO]
      SE_dic[subject] = [SE]



# for each file in folder: 
csv_files_in_folder = glob.glob("./sleep_diaries/*.csv")


for fil in csv_files_in_folder:
  analyse_file(fil)



# day_count = {1: 10, 2: 10, 3: 10, 4: 9, 5: 9, 6: 7, 7: 7, 8: 16 , 9: 14 , 10: 13 , 11: 15 , 12: 15 , 13: 13 , 14: 11 }
# keys = day_count.keys()
# values = day_count.values()
# plt.bar(keys, values)
# plt.savefig("paper_perday.png")


# 135.0: 14, 290.0: 8, 185.0: 11, 340.0: 8, 235.0: 7, 30.0: 10, 80.0: 11


# 8: 14 +, 9: 8 +, 10: 11 +, 11: 8 +, 12: 7 +, 13: 10 +, 14: 11 +

# 14 +8 +11 +8 +7 +10 +11 +

paper = [1.0, 1.0, 1.0, 1.0, 0.7142857142857143, 0.7142857142857143, 1.0, 0.42857142857142855, 1.0, 1.0]
app = [1.0, 0.8571428571428571, 0.8571428571428571, 1.0, 0.8571428571428571, 1.1428571428571428, 0.8571428571428571, 0.5714285714285714, 0.8571428571428571, 1.0, 0.7142857142857143, 0.8571428571428571, 0.5714285714285714, 1.0, 1.0, 1.0]

print(statistics.mean(paper), statistics.stdev(paper))
print(statistics.mean(app), statistics.stdev(app))