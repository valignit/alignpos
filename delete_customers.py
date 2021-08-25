##################################################
# Application: alignPOS
# Installation: AFSM 
# CLI Program: delete_customers
# Description: Delete all rows in the customer table in local db
# Version: 1.0
# 1.0.0 - 09-07-2021: New program
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


##############################
# Main
##############################
print_log('alignPOS - Delete Customers - Version 1.1')
print_log('-----------------------------------------')


######
# Connect to ERPNext web service
ws_erp_host = config["ws_host"]
ws_erp_sess = requests.Session()
ws_erp_user = config["ws_user"]
ws_erp_passwd = config["ws_passwd"]
ws_erp_payload = {"usr": ws_erp_user, "pwd": ws_erp_passwd }

ws_erp_method = '/api/method/login'

try:
    ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method, data=ws_erp_payload)
    ws_erp_resp.raise_for_status()   
    ws_erp_resp_text = ws_erp_resp.text
    ws_erp_resp_json = json.loads(ws_erp_resp_text)
    print_log(f"ERP web service logged in by {ws_erp_resp_json['full_name']}")
except requests.exceptions.HTTPError as ws_err:
    print_log(f"ERP web service error 201a: {ws_err}")
    sys.exit(1)
except requests.exceptions.ConnectionError as ws_err:
    print_log(f"ERP web service error 201b: {ws_err}")
    sys.exit(1)
except requests.exceptions.Timeout as ws_err:
    print_log(f"ERP web service error 201c: {ws_err}")
    sys.exit(1)
except requests.exceptions.RequestException as ws_err:
    print_log(f"ERP web service error 201d: {ws_err}")
    sys.exit(1)


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

######
# Delete old Customer records
db_pos_sql_stmt = (
    "DELETE FROM tabCustomer"
)

try:
    db_pos_cur.execute(db_pos_sql_stmt)
    db_pos_conn.commit()
    print_log("Old Customer records Deleted")
except mariadb.Error as db_err:
    print_log(f"POS database error 102: {db_err}")
    db_pos_conn.rollback()
    sys.exit(1)

last_sync_date_time = '2000-01-01 00:00:00'
ws_erp_payload = {"date": last_sync_date_time }

ws_erp_method = '/api/method/put_customer_sync_date_time'
try:
    ws_erp_resp = ws_erp_sess.put(ws_erp_host + ws_erp_method, json=ws_erp_payload)
    ws_erp_resp.raise_for_status()   
    ws_erp_resp_text = ws_erp_resp.text
    ws_erp_resp_json = json.loads(ws_erp_resp_text)
    #print_log(ws_erp_resp_json["data"])
except requests.exceptions.HTTPError as ws_err:
    print_log(f"ERP web service error 202a: {ws_err}")
    sys.exit(1)
except requests.exceptions.ConnectionError as ws_err:
    print_log(f"ERP web service error 202b: {ws_err}")
    sys.exit(1)
except requests.exceptions.Timeout as ws_err:
    print_log(f"ERP web service error 202c: {ws_err}")
    sys.exit(1)
except requests.exceptions.RequestException as ws_err:
    print_log(f"ERP web service error 202d: {ws_err}")
    sys.exit(1)

print_log(f"Time Stamp Updated: {last_sync_date_time}")

######    
# Closing DB connection
db_pos_conn.close()

######    
# Closing Log file 
print_log("Delete Customers process completed")
file_log.close()
