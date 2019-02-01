# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:18:17 2019

@author: jknox
"""
from matplotlib.ticker import MaxNLocator
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches

pcg_file = "Exports/pcg_location_export.txt"
duo_file = "Exports/duo_location_export.txt"

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
pcg_lat = []
pcg_lon = []
for entry in pcg_split:
    entry_split = entry.split()
    pcg_color.append('orangered')
    pcg_type.append(entry_split[0])
    pcg_date_time.append(entry_split[1])
    pcg_lat.append(float(entry_split[2]))
    pcg_lon.append(float(entry_split[3]))

duo_color = []
duo_type = []
duo_date_time = []
duo_lat = []
duo_lon = []
for entry in duo_split:
    entry_split = entry.split()
    duo_color.append('blue')
    duo_type.append(entry_split[0])
    duo_date_time.append(entry_split[1])
    duo_lat.append(float(entry_split[2]))
    duo_lon.append(float(entry_split[3]))

#------------------------------------------------------------------------------
#Create Data Frame    
#------------------------------------------------------------------------------  
pd.set_option('display.max_rows', 10000)
data = {'Type':pd.Series(pcg_type + duo_type),'Color':pd.Series(pcg_color + duo_color),
        'Date_Time':pd.Series(pcg_date_time + duo_date_time), 
        'Latitude':pd.Series(pcg_lat + duo_lat), 'Longitude':pd.Series(pcg_lon + duo_lon)}
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
#Calculating Latitude Deviation
#------------------------------------------------------------------------------  
i = 0
Latitude_diff = []
for elem in df['Latitude']:
    if df['Type'][i] != df['Type'][i+1]:
        Latitude_diff.append(df['Latitude'][i+1] - df['Latitude'][i])
        i+=1
        if i+1 == len(df['Latitude']):
            break
    i+=1
    if i+1 == len(df['Latitude']):
        break
i = 0
Latitude_ave = 0.0
for d in Latitude_diff:
    Latitude_ave = Latitude_ave + abs(d)
Latitude_ave = float(Latitude_ave/len(Latitude_diff))

#Imput allowed deviation------------------------------------------------------
Latitude_deviation = .05

Latitude_check_index = [] 
for elem in df['Latitude']:
    if df['Type'][i] != df['Type'][i+1]:
        if abs(df['Latitude'][i+1] - df['Latitude'][i]) > Latitude_deviation:
            Latitude_check_index.append(i)
    i+=1
    if i+1 == len(df['Latitude']):
        break
    
#------------------------------------------------------------------------------
#Calculating Longitude Deviation
#------------------------------------------------------------------------------
i = 0
Longitude_diff = []
for elem in df['Longitude']:
    if df['Type'][i] != df['Type'][i+1]:
        Longitude_diff.append(df['Longitude'][i+1] - df['Longitude'][i])
        i+=1
        if i+1 == len(df['Longitude']):
            break
    i+=1
    if i+1 == len(df['Longitude']):
        break
i = 0
Longitude_ave = 0.0
for d in Longitude_diff:
    Longitude_ave = Longitude_ave + abs(d)
Longitude_ave = float(Longitude_ave/len(Longitude_diff))

#Imput allowed deviation------------------------------------------------------
Longitude_deviation = .1

Longitude_check_index = [] 
for elem in df['Longitude']:
    if df['Type'][i] != df['Type'][i+1]:
        if abs(df['Longitude'][i+1] - df['Longitude'][i]) > Longitude_deviation:
            Longitude_check_index.append(i)
    i+=1
    if i+1 == len(df['Longitude']):
        break

#------------------------------------------------------------------------------
#Date vs Latitude Graph 
#------------------------------------------------------------------------------
plt.rcParams.update({'font.size': 8})

fig, ax = plt.subplots()
color = [str(item) for item in df['Color']]
plt.scatter(df['Date_Time'],df['Latitude'], c=color, s=3)
plt.plot(df['Date_Time'],df['Latitude'], '-k', linewidth=.5)
plt.figure(figsize=(20,10))
duo_patch = mpatches.Patch(color='Blue', label='DUO')
pcg_patch = mpatches.Patch(color='orangered', label='PCG')
ax.legend(handles=[pcg_patch,duo_patch])
ax.xaxis.set_major_locator(MaxNLocator(21))
ax.yaxis.set_major_locator(MaxNLocator(22))
ax.set(xlabel='Date and Time', ylabel='Latatude')
fig.autofmt_xdate()
plt.show()
fig.savefig('Exports/Graph_Latitude.pdf')

#------------------------------------------------------------------------------
#Date vs Longitude Graph 
#------------------------------------------------------------------------------
fig, ax = plt.subplots()
color = [str(item) for item in df['Color']]
plt.scatter(df['Date_Time'],df['Longitude'], c=color, s=3)
plt.plot(df['Date_Time'],df['Longitude'], '-k', linewidth=.5)
plt.figure(figsize=(20,10))
duo_patch = mpatches.Patch(color='Blue', label='DUO')
pcg_patch = mpatches.Patch(color='orangered', label='PCG')
ax.legend(handles=[pcg_patch,duo_patch])
ax.xaxis.set_major_locator(MaxNLocator(21))
ax.yaxis.set_major_locator(MaxNLocator(22))
ax.set(xlabel='Date and Time', ylabel='Longitude')
fig.autofmt_xdate()
plt.show()
fig.savefig('Exports/Graph_Longitude.pdf')

#------------------------------------------------------------------------------
#Longitude vs Latitude Graph 
#------------------------------------------------------------------------------
fig, ax = plt.subplots()
color = [str(item) for item in df['Color']]
plt.scatter(df['Longitude'],df['Latitude'], c=color, s=3)
plt.plot(df['Longitude'],df['Latitude'], '-k', linewidth=.5)
plt.figure(figsize=(20,10))
duo_patch = mpatches.Patch(color='Blue', label='DUO')
pcg_patch = mpatches.Patch(color='orangered', label='PCG')
ax.legend(handles=[pcg_patch,duo_patch])
ax.xaxis.set_major_locator(MaxNLocator(21))
ax.yaxis.set_major_locator(MaxNLocator(22))
ax.set(xlabel='Latitude', ylabel='Longitude')
fig.autofmt_xdate()
plt.show()
fig.savefig('Exports/Graph_Longitude_Latitude.pdf')
df.to_csv('Exports/location_data_frame.txt', sep='\t', index=True)
location_check = open("Exports/location_check.txt", "w")

#------------------------------------------------------------------------------
#Writing Data to Files
#------------------------------------------------------------------------------
print("Latitude_Index" + str(Latitude_check_index) + "\n")
location_check.write("Latitude_Index" + str(Latitude_check_index) + "\n")
print("Average Delta: %.4f " % Latitude_ave)
location_check.write("Average Delta: %.4f " % Latitude_ave + "\n")
print("Outliers with a deviation constraint:", Latitude_deviation)
location_check.write("Outliers with a deviation constraint:" + str(Latitude_deviation) + "\n\n")
for t in Latitude_check_index:
    print(df['Type'][t] + "\t" + df['Date_Time'][t] + "\t" + str(df['Latitude'][t]))
    location_check.write(df['Type'][t] + "\t" + df['Date_Time'][t] + "\t" + str(df['Latitude'][t]) + "\n")
    print(df['Type'][t+1] + "\t" + df['Date_Time'][t+1] + "\t" + str(df['Latitude'][t+1]))
    location_check.write(df['Type'][t+1] + "\t" + df['Date_Time'][t+1] + "\t" + str(df['Latitude'][t+1]) + "\n\n")
    print()
print("Longitude_Index", Longitude_check_index)
location_check.write("Longitude_Index" + str(Longitude_check_index) + "\n")
print("Average Delta: %.4f " % Longitude_ave)
location_check.write("Average Delta: %.4f " % Longitude_ave + "\n")
print("Outliers with a deviation constraint:", Longitude_deviation)
location_check.write("Outliers with a deviation constraint:" + str(Longitude_deviation) + "\n\n")
for t in Longitude_check_index:
    print(df['Type'][t] + "\t" + df['Date_Time'][t] + "\t" + str(df['Longitude'][t]))
    location_check.write(df['Type'][t] + "\t" + df['Date_Time'][t] + "\t" + str(df['Longitude'][t]) + "\n")
    print(df['Type'][t+1] + "\t" + df['Date_Time'][t+1] + "\t" + str(df['Longitude'][t+1]))
    location_check.write(df['Type'][t+1] + "\t" + df['Date_Time'][t+1] + "\t" + str(df['Longitude'][t+1]) + "\n\n")
    print()
    
location_check.close()
#input()