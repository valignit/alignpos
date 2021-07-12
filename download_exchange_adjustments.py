##################################################
# Application: alignPOS
# Installation: AFSM
# CLI Program: download_exchange adjustments
# Description: Get the Exchange Adjustments created and updated after the last download.
#              Insert or Update the Exchange Adjustments table in local db
# Version: 1.0
# 1.0.0 - 09-07-2021: New program
##################################################

import json
import requests
import mariadb
import sys
from datetime import datetime, timedelta


last_sync = '2000-01-01 00:01:01.000001'
exchange_adjustment_count = 0

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
now = datetime.now()

with open('./alignpos.json') as file_config:
  config = json.load(file_config)
  
file_name = config["log_folder_path"] + str(__file__)[:-3] + "-" + now.strftime("%Y%m%d%H%M") + ".log"
file_log = open(file_name, "w")

print_log('alignPOS - Download Exchange Adjustments - Version 1.1')
print_log('------------------------------------------------------')

######
# Connect to ERPNext web service
ws_erp_host = config["ws_erp_host"]
ws_erp_sess = requests.Session()
ws_erp_user = config["ws_erp_user"]
ws_erp_passwd = config["ws_erp_passwd"]
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
db_pos_host = config["db_pos_host"]
db_pos_port = config["db_pos_port"]
db_pos_name = config["db_pos_name"]
db_pos_user = config["db_pos_user"]
db_pos_passwd = config["db_pos_passwd"]

try:
    db_pos_conn = mariadb.connect(
        user = db_pos_user,
        password = db_pos_passwd,
        host = db_pos_host,
        port = db_pos_port,
        database = db_pos_name
    )
    print_log("POS database connected")

except mariadb.Error as db_err:
    print_log(f"POS database error 101: {db_err}")
    sys.exit(1)
    
db_pos_cur = db_pos_conn.cursor()


######
# Fetch Created list of Exchange Adjustments from ERP
ws_erp_method = 'api/method/get_exchange_adjustments?limit_page_length=None'
try:
    ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method)
    ws_erp_resp.raise_for_status()   
    ws_erp_resp_text = ws_erp_resp.text
    ws_erp_resp_json = json.loads(ws_erp_resp_text)
    #print_log(ws_erp_resp_text)
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

######
# Fetch each Item from Exchange Adjustment List from ERP

exchange_adjustment_create_count = 0
for ws_exchange_adjustment_row in ws_erp_resp_json["exchange_adjustments_list"]:
    print_log("Transferring Exchange Adjustment: " + ws_exchange_adjustment_row["name"])
    exchange_adjustment_count+=1
    exchange_adjustment_create_count+=1
    exchange_adjustment_name = ws_exchange_adjustment_row["name"]
    exchange_adjustment_customer = ws_exchange_adjustment_row["party"]
    exchange_adjustment_amount = ws_exchange_adjustment_row["paid_amount"]
    exchange_adjustment_modified = ws_exchange_adjustment_row["creation"]
 
    exchange_adjustment_modified_datetime = datetime.strptime(ws_exchange_adjustment_row["creation"], '%Y-%m-%d %H:%M:%S.%f')
    last_sync_datetime = datetime.strptime(last_sync, '%Y-%m-%d %H:%M:%S.%f') 

    if exchange_adjustment_modified_datetime > last_sync_datetime:
        last_sync = exchange_adjustment_modified
    
    db_pos_sql_stmt = (
       "INSERT INTO `tabExchange Adjustment` (name, customer, exchange_amount, creation, owner)"
       "VALUES (%s, %s, %s, now(), %s)"
    )
    db_pos_sql_data = (exchange_adjustment_name, exchange_adjustment_customer, exchange_adjustment_amount, ws_erp_user)

    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        db_pos_conn.commit()
    except mariadb.Error as db_err:
        print_log(f"POS database error 102: {db_err}")
        db_pos_conn.rollback()
        sys.exit(1)

print_log(f"Total Exchange Adjustments Transferred: {exchange_adjustment_create_count}")


######
# Update Last sync date time
if (exchange_adjustment_count > 0):
    ws_erp_payload = {"date": last_sync}
    
    #print('payload:', ws_erp_payload)

    ws_erp_method = '/api/method/put_exchange_adjustment_sync_date_time'
    try:
        ws_erp_resp = ws_erp_sess.put(ws_erp_host + ws_erp_method, json=ws_erp_payload)
        ws_erp_resp.raise_for_status()   
        ws_erp_resp_text = ws_erp_resp.text
        ws_erp_resp_json = json.loads(ws_erp_resp_text)
        #print_log(ws_erp_resp_json["data"])
    except requests.exceptions.HTTPError as ws_err:
        print_log(f"ERP web service error 206a: {ws_err}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as ws_err:
        print_log(f"ERP web service error 206b: {ws_err}")
        sys.exit(1)
    except requests.exceptions.Timeout as ws_err:
        print_log(f"ERP web service error 206c: {ws_err}")
        sys.exit(1)
    except requests.exceptions.RequestException as ws_err:
        print_log(f"ERP web service error 206d: {ws_err}")
        sys.exit(1)

    print_log(f"Time Stamp Updated: {str(last_sync_datetime)}")


######    
# Closing DB connection
db_pos_conn.close()

######    
# Closing Log file 
print_log("Download Exchange Adjustments process completed")
file_log.close()
