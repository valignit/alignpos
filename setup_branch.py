##################################################
# Application: alignPOS
# Installation: AFSM 
# CLI Program: setup_branch
# Description: Delete all rows in the item table in local db
# Version: 1.0
# 1.0.0 - 09-07-2021: New program
##################################################

import os
import sys
import subprocess
import pickledb
import json
from datetime import date, datetime, timedelta


##############################
# Print and Log
##############################
def print_log(msg):
    file_log = open(file_name, "a")
    msg = str(now) + ': ' + msg + '\n'
    file_log.write(msg)
    file_log.close()
    
    
##############################
# Main
##############################
now = datetime.now()


sys_path = 'c:\\alignpos\\'
sys.path.append(sys_path)

with open(sys_path + 'app_config.json') as file_config:
  config = json.load(file_config)

file_name = config["log_folder_path"] + str(__file__)[:-3] + "-" + now.strftime("%Y%m%d%H%M") + ".log"
file_log = open(file_name, "w")

today = date.today()

print_log('Setup Branch - Version 1.1')

pid = subprocess.Popen(["python", "download_settings.py"])
print_log('download_settings completed')
pid = subprocess.Popen(["python", "download_customers.py"])
print_log('download_customers completed')

print_log('Process completed')
file_log.close()
