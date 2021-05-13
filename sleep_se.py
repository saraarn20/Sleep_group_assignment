import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import glob

# =============================
# = Info & example from paper =
# =============================

# SE = TST / DSE (× 100)
# DSE = SOL + TST + WASO + TASAFA

# DSE, duration of the sleep episode SCT, stimulus control therapy
# SE, sleep efficiency
# SOL, sleep onset latency
# SRT, sleep restriction therapy
# TASAFA, time attempting to sleep after the final awakening TIB, time in bed
# TST, total sleep time
# WASO, time awake after initial sleep onset but before final awakening

# into bed 22:15
# tries to go to sleep 23:30
# falls a sleep 55 later
# wakes up 3 times
# wakes for 70 minutes
# final awakening 6:35
# stays in bed till 7:20
# ==== >
# TST = 300 minutes 
# TIB = 545 minutes
# SOL = 55 minutes
# TST = 300 minutes
# WASO = 70 minutes
# TASAFA = 45 minutes

# Helpercle
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

print("YO")

TST_dic = {}
SE_dic = {}
WASO_dic = {}
SL_dic = {}

# ===================
# = Data Processing =
# ===================
yo = []

empty_count = 0
full_count = 0
total_count = 0
analysed_subjects = 0

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

  for day in range(1, 4):
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


    # print("TST_total" ,TST_total)
    # print("TST", TST)
    
    time_to_bed = datetime.strptime(sleep_df.iat[1,day], FMT)
    time_out_of_bed = datetime.strptime(sleep_df.iat[8,day], FMT)


    # If the sleep time is before midnight - prevent negative value.. 
    if time_out_of_bed < time_to_bed:
      time_out_of_bed += timedelta(days=1)

    TIB = time_out_of_bed - time_to_bed
    TIB = TIB.total_seconds() / 60 # set to minutes

    # print(time_to_bed, time_out_of_bed, TIB)
    # print("TIB: ", TIB)
    # print("TIB minutes: ", TIB.total_seconds() / 60)

    # =======
    # = SOL =
    # =======

    SOL_data = sleep_df.iat[3,day] 
    SOL = data_to_minutes(SOL_data)
    # print('SOL', SOL)

    # ========
    # = WASO =
    # ========

    WASO_data = sleep_df.iat[5,day] 
    WASO = data_to_minutes(WASO_data)
    # print(WASO)


    # ==========
    # = TASAFA =
    # ==========

    leaves_bed = datetime.strptime(sleep_df.iat[8,day], FMT) # 7. Klukkan hvað fórstu þú á fætur? 
    final_awake = datetime.strptime(sleep_df.iat[6,day], FMT) # 6.  Klukkan hvað vaknaðir þú endanlega

    if leaves_bed < final_awake:
      leaves_bed += timedelta(days=1)

    TASAFA = leaves_bed - final_awake
    TASAFA = TASAFA.total_seconds() / 60 # set to minutes

    # print("TASAFA", TASAFA)

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

  f = open("SE_Results.txt", "a")
  f.write(
"""SUBJECT: {subject}
SE for all days: {SE_list}
Average: {se}
First three: {three}

""".format(three=3, subject=subject, SE_list=str(SE_list), se=str(sum(SE_list) / len(SE_list))))
  f.close()

  yo.append((subject, str(sum(SE_list) / len(SE_list))))


# for each file in folder: 
csv_files_in_folder = glob.glob("./sleep_diaries/*.csv")


for fil in csv_files_in_folder:
  # print(fil)
  analyse_file(fil)
# analyse_file("./sleep_diaries/210.csv")

# print to copy over to sas_vs_diary.. 
print('--------')
print("SE_dic", len(SE_dic), SE_dic)
print('--------')
print("TST_dic", len(TST_dic), TST_dic)
print('--------')
print("SL_dic", len(SL_dic), SL_dic)
print('--------')
print("WASO_dic", len(WASO_dic), WASO_dic)

print()

print("empty_count", empty_count)
print("full_count", full_count)
print("total_count", total_count)
print("analysed_subjects", analysed_subjects)


# 'SRI 0202': [120, 60, 60], 
# 'SRI 0203': [30, 30, 30], 
# 'SRI 0205': [10, 2, 20], 
# {'SRI 0208': [5, 3, 3], 
# 'SRI 0209': [20, 0, 0], 
# 'SRI 0210': [20, 10, 5], 
# 'SRI 0211': [10, 30, 15], 
# 'SRI 0213': [15, 5, 5], 
# 'SRI 0215': [1, 1, 1]}
# 'SRI 0217': [20, 3, 3], 