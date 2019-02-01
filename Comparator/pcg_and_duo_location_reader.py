# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:15:39 2019

@author: jknox
"""
def find_and_store(element_to_find, entry_list):
    i = 0
    for element in entry_list:
        if element == element_to_find:
            return entry_list[i+1]
        i +=1
        
def find_and_store_time(element_to_find, entry_list):
    i = 0
    for element in entry_list:
        if element == element_to_find:
            return entry_list[i+2]
        i +=1
            
#------------------------------------------------------------------------------
#PCG Location Reader
#------------------------------------------------------------------------------
#splits the log into entries 
log_file = "Logs/pcg_location.log"
log = open(log_file, "r")
data_read = log.read()
log.close()

#splits the log into entries 
data_split = data_read.split("\n")

export_file = "Exports/pcg_location_export.txt"

log_data = open(export_file, "w")
log_data.write("Log_Type" + "\t" + "Date_Time" + "\t" + "Latitude" + "\t" + "Longitude" + "\n")

for entry in data_split:
    
    if entry.find("notice") > 0:
        entry_split = entry.split();
        for element in entry_split:
            date_time_info = entry[0:19]
            Date_Time = date_time_info.replace("T", "_")
            Latitude = find_and_store("lat", entry_split)
            Longitude = find_and_store("lon", entry_split)
        print("PCG" + "\t" + Date_Time + "\t" + Latitude + "\t" + Longitude + "\n")
        log_data.write("PCG" + "\t" + Date_Time + "\t" + Latitude + "\t" + Longitude + "\n")
log_data.close()

#------------------------------------------------------------------------------
#DUO Location Reader
#------------------------------------------------------------------------------         
log_file = "Logs/duo_location.log"
log = open(log_file, "r")
data_read = log.read()
log.close()

#splits the log into entries 
data_split = data_read.split("\n")

export_file = "Exports/duo_location_export.txt"

log_data = open(export_file, "w")
log_data.write("Log_Type" + "\t" + "Date_Time" + "\t" + "Latitude" + "\t" + "Longitude" + "\n")

for entry in data_split:
        
    if entry.find("notice") > 0:
        entry_split = entry.split();
        for element in entry_split:
            date_time_info = entry[0:19]
            Date_Time = date_time_info.replace("T", "_")
            Latitude = find_and_store("lat", entry_split)
            Longitude = find_and_store("lon", entry_split)
        print("DUO" + "\t" + Date_Time + "\t" + Latitude + "\t" + Longitude + "\n")
        log_data.write("DUO" + "\t" +Date_Time + "\t" + Latitude + "\t" + Longitude + "\n")
log_data.close()
