# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 13:31:18 2019

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
#DUO Radio Reader
#------------------------------------------------------------------------------
#opens and reads log data with name "duo_log.txt"
log_file = "Logs\duo_radio.log"
log_data = open(log_file, "r")
data_read = log_data.read()
log_data.close

#splits log data and sorts into radio data and location data
data_split = data_read.split("\n")

#creates export file
export_file = "Exports\duo_radio_export.txt"
radio_log = open(export_file, "w")
radio_log.write("Log_Type" + "\t" +"date_time\trsrp\trsrq\n")

rsrp = rsrq = date = time = ""
for entry in data_split:
    entry_split = entry.split()
    if entry.find("utc") > 0 and entry.find("rsrp") > 0:
        date = find_and_store("utc", entry_split)
        time = find_and_store_time("utc", entry_split)
        time = time.replace(",", "")
        rsrp = find_and_store('rsrp', entry_split)
        rsrp = rsrp.replace(",", "")
        rsrq = find_and_store('rsrq', entry_split)
        rsrq = rsrq.replace(",", "")
        if rsrq == '-' or rsrq == 'null':
            rsrq = 0
        if rsrp == '-' or rsrp == 'null':
            rsrp = 0
#writes information to export file
        radio_log.write("duo" + "\t" +date + "_" + time + "\t" + str(rsrp) + "\t" + str(rsrq) + "\n")
        print("date:" + date + "\n" + "time:" + time + "\n" + "rsrp:" + str(rsrp) + "\n" + "rsrq:" + str(rsrq) + "\n")

radio_log.close()   