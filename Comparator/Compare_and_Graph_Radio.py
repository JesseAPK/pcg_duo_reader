# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:18:17 2019

@author: jknox
"""
from matplotlib.ticker import MaxNLocator
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches

pcg_file = "Exports\pcg_radio_export.txt"
duo_file = "Exports\duo_radio_export.txt"

pcg_log = open(pcg_file, "r")
pcg_data = pcg_log.read()
pcg_log.close()

duo_log = open(duo_file, "r")
duo_data = duo_log.read()
duo_log.close()

pcg_split = pcg_data.split("\n")
duo_split = duo_data.split('\n')
del pcg_split[-1]
del pcg_split[0]
del duo_split[-1]
del duo_split[0]

pcg_color = []
pcg_type = []
pcg_date_time = []
pcg_rsrp = []
pcg_rsrq = []
for entry in pcg_split:
    entry_split = entry.split()
    pcg_color.append('orangered')
    pcg_type.append(entry_split[0])
    pcg_date_time.append(entry_split[1])
    pcg_rsrp.append(int(entry_split[2]))
    pcg_rsrq.append(int(entry_split[3]))

duo_color = []
duo_type = []
duo_date_time = []
duo_rsrp = []
duo_rsrq = []
for entry in duo_split:
    entry_split = entry.split()
    duo_color.append('blue')
    duo_type.append(entry_split[0]) 
    duo_date_time.append(entry_split[1])
    duo_rsrp.append(int(entry_split[2]))
    duo_rsrq.append(int(entry_split[3]))
    
#------------------------------------------------------------------------------
#Create Data Frame    
#------------------------------------------------------------------------------    
pd.set_option('display.max_rows', 1000)
data = {'Type':pd.Series(pcg_type + duo_type),'Color':pd.Series(pcg_color + duo_color), 
        'Date_Time':pd.Series(pcg_date_time + duo_date_time), 
        'rsrp':pd.Series(pcg_rsrp + duo_rsrp), 'rsrq':pd.Series(pcg_rsrq + duo_rsrq)}
df = pd.DataFrame(data)
df = df.sort_values(by=['Date_Time'])
df = df.reset_index(drop=True)
k = 0
indx = []
for elem in df['Type']:
    if df['Type'][k] != df['Type'][k+1]:
        indx.append(k)
    if k+2 == len(df['Type']):
        break
    k+=1

df.drop(df.index[indx[-1]:-1], inplace=True)
df.drop(df.index[-1], inplace=True)
df.drop(df.index[0:indx[0]], inplace=True)
df = df.reset_index(drop=True)

#------------------------------------------------------------------------------
#Calulate RSRP Deviation
#------------------------------------------------------------------------------
i = 0
rsrp_diff = []
rsrp_times = []
for elem in df['rsrp']:
    if df['Type'][i] != df['Type'][i+1]:
        rsrp_diff.append(abs(df['rsrp'][i+1] - df['rsrp'][i]))
        #print (df['rsrp'][i+1], df['rsrp'][i])
        rsrp_times.append(df['Date_Time'][i])
        i+=1
        if i+1 == len(df['rsrp']):
            break
    i+=1
    if i+1 == len(df['rsrp']):
        break

i = 0
rsrp_ave = 0
for d in rsrp_diff:
    rsrp_ave = rsrp_ave + abs(d)
if len(rsrp_diff) != 0:
    rsrp_ave = rsrp_ave/len(rsrp_diff)
else:
    rsrp_ave = 0
rsrp_ave = int(abs(rsrp_ave))

#Imput allowed deviation------------------------------------------------------
rsrp_deviation = 20

rsrp_check_index = [] 
for elem in df['rsrp']:
    if df['Type'][i] != df['Type'][i+1]:
        if abs(df['rsrp'][i+1] - df['rsrp'][i]) > rsrp_deviation:
            rsrp_check_index.append(i)
    i+=1
    if i+1 == len(df['rsrp']):
        break
    
#------------------------------------------------------------------------------
#Calulate RSRQ Deviation
#------------------------------------------------------------------------------
i = 0
rsrq_diff = []
rsrq_times = []
for elem in df['rsrq']:
    if df['Type'][i] != df['Type'][i+1]:
        rsrq_diff.append(abs(df['rsrq'][i+1] - df['rsrq'][i]))
        #print (df['rsrq'][i+1], df['rsrq'][i])
        rsrq_times.append(df['Date_Time'][i])
        i+=1
        if i+1 == len(df['rsrq']):
            break
    i+=1
    if i+1 == len(df['rsrq']):
        break

i = 0
rsrq_ave = 0
for d in rsrq_diff:
    rsrq_ave = rsrq_ave + abs(d)
if len(rsrq_diff) != 0:
    rsrp_ave = rsrq_ave/len(rsrq_diff)
rsrq_ave = int(abs(rsrq_ave))

#Imput allowed deviation------------------------------------------------------
rsrq_deviation = 10

rsrq_check_index = [] 
for elem in df['rsrq']:
    if df['Type'][i] != df['Type'][i+1]:
        if abs(df['rsrq'][i+1] - df['rsrq'][i]) > rsrq_deviation:
            rsrq_check_index.append(i)
    i+=1
    if i+1 == len(df['rsrq']):
        break
    
#------------------------------------------------------------------------------
#rsrp graphing
#------------------------------------------------------------------------------
fig, ax = plt.subplots()
color = [str(item) for item in df['Color']]
plt.scatter(df['Date_Time'],df['rsrp'], c=color, s=3)
plt.figure(figsize=(20,10))
duo_patch = mpatches.Patch(color='Blue', label='DUO')
pcg_patch = mpatches.Patch(color='orangered', label='PCG')
ax.legend(handles=[pcg_patch,duo_patch])
ax.xaxis.set_major_locator(MaxNLocator(21))
ax.yaxis.set_major_locator(MaxNLocator(22))
ax.set(xlabel='Date and Time', ylabel='rsrp')
fig.autofmt_xdate()
plt.show()
fig.savefig('Exports\Graph_rsrp.pdf')
        
plt.rcParams.update({'font.size': 8})
fig, ax = plt.subplots()
color = [str(item) for item in df['Color']]
plt.scatter(rsrp_times,rsrp_diff, s=3)
plt.plot(rsrp_times,rsrp_diff, '-k', linewidth=.5)
plt.figure(figsize=(20,10))
ax.xaxis.set_major_locator(MaxNLocator(21))
ax.yaxis.set_major_locator(MaxNLocator(22))
ax.set(xlabel='Date and Time', ylabel='rsrp differance')
fig.autofmt_xdate()
plt.show()
fig.savefig('Exports\Graph_rsrp_diff.pdf')

#------------------------------------------------------------------------------
#rsrq graphing
#------------------------------------------------------------------------------
fig, ax = plt.subplots()
color = [str(item) for item in df['Color']]
plt.scatter(df['Date_Time'],df['rsrq'], c=color, s=3)
plt.figure(figsize=(20,10))
duo_patch = mpatches.Patch(color='Blue', label='DUO')
pcg_patch = mpatches.Patch(color='orangered', label='PCG')
ax.legend(handles=[pcg_patch,duo_patch])
ax.xaxis.set_major_locator(MaxNLocator(21))
ax.yaxis.set_major_locator(MaxNLocator(22))
ax.set(xlabel='Date and Time', ylabel='rsrq')
fig.autofmt_xdate()
plt.show()
fig.savefig('Exports\Graph_rsrq.pdf')

plt.rcParams.update({'font.size': 8})
fig, ax = plt.subplots()
color = [str(item) for item in df['Color']]
plt.scatter(rsrq_times,rsrq_diff, s=3)
plt.plot(rsrq_times,rsrq_diff, '-k', linewidth=.5)
plt.figure(figsize=(20,10))
ax.xaxis.set_major_locator(MaxNLocator(21))
ax.yaxis.set_major_locator(MaxNLocator(22))
ax.set(xlabel='Date and Time', ylabel='rsrq differance')
fig.autofmt_xdate()
plt.show()
fig.savefig('Exports\Graph_rsrq_diff.pdf')

#------------------------------------------------------------------------------
#Writing Data to Files
#------------------------------------------------------------------------------
df.to_csv('Exports/radio_data_frame.txt', sep='\t', index=True)
radio_check = open("Exports/radio_check.txt", "w")

print("Index " + str(rsrp_check_index))
radio_check.write("Index " + str(rsrp_check_index) + "\n")
print("Average rsrp Delta:", rsrp_ave)
radio_check.write("Average rsrp Delta:" + str(rsrp_ave) + "\n")
print("Outliers with a deviation rsrp constraint:", rsrp_deviation)
radio_check.write("Outliers with a deviation rsrp constraint:" + str(rsrp_deviation) + "\n" + "\n")
for t in rsrp_check_index:
    print(df['Type'][t] + "\t" + df['Date_Time'][t] + "\t" + str(df['rsrp'][t]))
    radio_check.write(df['Type'][t] + "\t" + df['Date_Time'][t] + "\t" + str(df['rsrp'][t]) + "\n")
    print(df['Type'][t+1] + "\t" + df['Date_Time'][t+1] + "\t" + str(df['rsrp'][t+1]))
    radio_check.write(df['Type'][t+1] + "\t" + df['Date_Time'][t+1] + "\t" + str(df['rsrp'][t+1]) + "\n" + "\n")
    print()

print()

print("Index", rsrq_check_index)
radio_check.write("Index" + str(rsrq_check_index) + "\n")
print("Average rsrq Delta:", rsrq_ave)
radio_check.write("Average rsrq Delta:" + str(rsrq_ave) + "\n")
print("Outliers with a deviation rsrq constraint:", rsrq_deviation)
radio_check.write("Outliers with a deviation rsrq constraint:" + str(rsrq_deviation) + "\n" + "\n")
for t in rsrq_check_index:
    print(df['Type'][t] + "\t" + df['Date_Time'][t] + "\t" + str(df['rsrq'][t]))
    radio_check.write(df['Type'][t] + "\t" + df['Date_Time'][t] + "\t" + str(df['rsrq'][t]) + "\n")
    print(df['Type'][t+1] + "\t" + df['Date_Time'][t+1] + "\t" + str(df['rsrq'][t+1]))
    radio_check.write(df['Type'][t+1] + "\t" + df['Date_Time'][t+1] + "\t" + str(df['rsrq'][t+1]) + "\n" + "\n")
    print()
    
radio_check.close()