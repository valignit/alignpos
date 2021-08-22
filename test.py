##################################################
# Application: alignPOS
# Installation: AFSM
# CLI Program: upload_invoices
# Description: Upload all paid invoices to ERPNext
# Version: 1.0
# 1.0.0 - 25-04-2021: New program
##################################################

import json
import requests
import mariadb
import sys
import datetime

now = datetime.datetime.now()

with open('./app_config.json') as file_config:
  config = json.load(file_config)
  
file_name = config["log_folder_path"] + str(__file__)[:-3] + "-" + now.strftime("%Y%m%d%H%M") + ".log"
file_log = open(file_name, "w")

##############################
# Print and Log
##############################
def print_log(msg):
    print(msg)
    msg = str(now) + ': ' + msg + '\n'
    file_log.write(msg)



######
# Connect to POS database
db_pos_host = config["db_host"]
db_pos_port = config["db_port"]
db_pos_database = config["db_database"]
db_pos_user = config["db_user"]
db_pos_passwd = config["db_passwd"]

try:
    db_pos_conn = mariadb.connect(
        user = db_pos_user,
        password = db_pos_passwd,
        host = db_pos_host,
        port = db_pos_port,
        database = db_pos_database
    )
    print_log("POS database connected")

except mariadb.Error as db_err:
    print_log(f"POS database error 101: {db_err}")
    sys.exit(1)
    
db_pos_cur = db_pos_conn.cursor()

datestr = '2010-12-11 01:01:01'
sql_update_query = 'Update tabInvoice set posting_date = "{}"'.format(datestr)

try:
    db_pos_cur.execute(sql_update_query)
    db_pos_conn.commit()
except mariadb.Error as db_err:
    print_log(f"POS database error 102: {db_err}")
    db_pos_conn.rollback()
    sys.exit(1)
        
######    
# Closing DB connection
db_pos_conn.close()

######    
# Closing Log file 
print_log("Upload Invoices process completed")
file_log.close()
