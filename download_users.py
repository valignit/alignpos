##################################################
# Application: alignPOS
# Installation: AFSM
# CLI Program: download_users
# Description: Get the Users created and updated after the last download.
#              Insert or Update the Users table in local db
# Version: 1.0
# 1.0.0 - 09-07-2021: New program
##################################################

import json
import requests
import mariadb
import sys
from datetime import datetime, timedelta


last_sync = '2000-01-01 00:01:01.000001'
user_count = 0

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

with open('./app_config.json') as file_config:
  config = json.load(file_config)
  
file_name = config["log_folder_path"] + str(__file__)[:-3] + "-" + now.strftime("%Y%m%d%H%M") + ".log"
file_log = open(file_name, "w")

branch_id = config["branch_id"]

print_log('alignPOS - Download Users - Version 1.1')
print_log('-------------------------------------------')

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
# Fetch Created list of Users from ERP
ws_erp_method = 'api/method/get_created_users'
ws_erp_payload = {"branch": branch_id}
try:
    ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method, json=ws_erp_payload)
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
# Fetch each Item from Item List from ERP

user_create_count = 0
for ws_user_row in ws_erp_resp_json["users"]:
    print_log("Creating Item: " + ws_user_row["username"])
    user_count+=1
    user_create_count+=1
    user_name = ws_user_row["username"]
    user_full_name = ws_user_row["full_name"]
    user_role = ws_user_row["role"]
    user_enabled = ws_user_row["enabled"]
    user_created = ws_user_row["creation"]
 
    user_created_datetime = datetime.strptime(ws_user_row["creation"], '%Y-%m-%d %H:%M:%S.%f')
    last_sync_datetime = datetime.strptime(last_sync, '%Y-%m-%d %H:%M:%S.%f') 

    if user_created_datetime > last_sync_datetime:
        last_sync = user_created
    
    db_pos_sql_stmt = (
       "INSERT INTO tabUser (user_name, full_name, passwd, role, enabled, creation, owner)"
       "VALUES (%s, %s, ENCODE('welcome', 'secret'), %s, %d, now(), %s)"
    )
    db_pos_sql_data = (user_name, user_full_name, user_role, user_enabled, ws_erp_user)

    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        db_pos_conn.commit()
    except mariadb.Error as db_err:
        print_log(f"POS database error 102: {db_err}")
        db_pos_conn.rollback()
        sys.exit(1)

print_log(f"Total Users Created: {user_create_count}")


######
# Fetch Updated list of Users from ERP
ws_erp_method = 'api/method/get_updated_users'
ws_erp_payload = {"branch": branch_id}

try:
    ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method, json=ws_erp_payload)
    ws_erp_resp.raise_for_status()   
    ws_erp_resp_text = ws_erp_resp.text
    ws_erp_resp_json = json.loads(ws_erp_resp_text)
    #print_log(ws_erp_resp_text)
except requests.exceptions.HTTPError as ws_err:
    print_log(f"ERP web service error 204a: {ws_err}")
    sys.exit(1)
except requests.exceptions.ConnectionError as ws_err:
    print_log(f"ERP web service error 204b: {ws_err}")
    sys.exit(1)
except requests.exceptions.Timeout as ws_err:
    print_log(f"ERP web service error 204c: {ws_err}")
    sys.exit(1)
except requests.exceptions.RequestException as ws_err:
    print_log(f"ERP web service error 204d: {ws_err}")
    sys.exit(1)

######
# Fetch each Item from Item List from ERP

user_update_count = 0
for ws_user_row in ws_erp_resp_json["users"]:
    print_log("Updating Item: " + ws_user_row["username"])
    user_count+=1
    user_update_count+=1
    user_full_name = ws_user_row["full_name"]
    user_role = ws_user_row["role"]
    user_enabled = ws_user_row["enabled"]
    user_modified = ws_user_row["modified"]
  
    user_modified_datetime = datetime.strptime(ws_user_row["modified"], '%Y-%m-%d %H:%M:%S.%f')
    last_sync_datetime = datetime.strptime(last_sync, '%Y-%m-%d %H:%M:%S.%f') 

    if user_modified_datetime > last_sync_datetime:
        last_sync = user_modified
    
    db_pos_sql_stmt = (
       "UPDATE tabUser  SET full_name = %s, \
                            role = %s, \
                            enabled = %d, \
                            modified = now(), \
                            modified_by = %s \
                        WHERE name = %s" \
    )
    db_pos_sql_data = ( user_full_name, user_role, user_enabled, \
                        ws_erp_user, user_name \
    )

    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        db_pos_conn.commit()
    except mariadb.Error as db_err:
        print_log(f"POS database error 103: {db_err}")
        db_pos_conn.rollback()
        sys.exit(1)

print_log(f"Total Users Updated: {user_update_count}")


######
# Update Last sync date time
if (user_count > 0):
    
    #print('payload:', ws_erp_payload)

    ws_erp_method = '/api/method/put_user_sync_date_time'
    ws_erp_payload = {"date": last_sync, "branch": branch_id}
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
print_log("Download Users process completed")
file_log.close()
