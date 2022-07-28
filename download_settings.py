##################################################
# Application: alignPOS
# Installation: AFSM
# CLI Program: download_settings
# Description: Get the Alignpos Settings from ERPNext
# Version: 1.0
# 1.0.0 - 09-07-2021: New program
##################################################

import json
import requests
import pickledb
import sys
from datetime import datetime, timedelta
import mariadb

from config import Config

last_sync = '2000-01-01 00:01:01.000001'
customer_count = 0

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

config = Config()

branch_id = config.branch_id

file_name = config.log_folder_path + str(__file__)[:-3] + "-" + now.strftime("%Y%m%d%H%M") + ".log"
file_log = open(file_name, "w")

print_log('Download Settings - Version 1.1')

######
# Connect to ERPNext web service
ws_erp_host = config.ws_protocol + '://' + config.ws_host
ws_erp_sess = requests.Session()
ws_erp_user = config.ws_user
ws_erp_passwd = config.ws_passwd
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
db_pos_host = config.db_host
db_pos_port = config.db_port
db_pos_database = config.db_database
db_pos_user = config.db_user
db_pos_passwd = config.db_passwd

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
# Connect to Key Value database
#kv = pickledb.load('data/alignpos_settings', False)
kv = pickledb.load(config.kv_settings, False)

kv.deldb()

######
# Fetch module parameters from ERP
ws_erp_method = '/api/resource/Alignpos Parameters/Alignpos Parameters'
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
# Fetch Alignpos Settings from ERP
ws_settings_row = ws_erp_resp_json["data"]

tax_included = ws_settings_row["tax_included"]
welcome_text = ws_settings_row["welcome_text"]
walk_in_customer = ws_settings_row["walk_in_customer"]

kv.set('tax_included', tax_included)
kv.set('walk_in_customer', walk_in_customer)
kv.set('welcome_text', welcome_text)

######
# Fetch branch parameters from ERP
ws_erp_method = '/api/method/get_branch'
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
# Fetch Alignpos Settings from ERP
ws_settings_row = ws_erp_resp_json["branch"]
favorite_items = ws_settings_row["favorites"]
fast_moving_items = ws_settings_row["fast_moving"]
terminals = ws_settings_row["terminals"]

if favorite_items:
    ct = 0
    for item in favorite_items:
        ct += 1
        key = 'favorite_item_' + str(ct)
        kv.set(key, item["favorite_item"])
        
if fast_moving_items:
    ct = 0
    for item in fast_moving_items:
        ct += 1
        key = 'fast_moving_item_' + str(ct)
        kv.set(key, item["fast_moving_item"])

if terminals:
    ct = 0
    for terminal in terminals:
        terminal_id = terminal["terminal_id"]
        terminal_enabled = terminal["enabled"]
        terminal_cash_allowed = terminal["cash_allowed"]
        terminal_sales_allowed = terminal["sales_allowed"]
        
        db_pos_sql_stmt = (
           "UPDATE tabTerminal  SET enabled = %d, \
                                cash_allowed = %d, \
                                sales_allowed = %d, \
                                modified = now() \
                            WHERE name = %s" \
        )
        db_pos_sql_data = ( terminal_enabled, terminal_cash_allowed, terminal_sales_allowed, terminal_id \
        )

        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
            db_pos_conn.commit()
        except mariadb.Error as db_err:
            print_log(f"POS database error 103: {db_err}")
            db_pos_conn.rollback()
            sys.exit(1)


######    
# Closing DB connection
db_pos_conn.close()


for key in kv.getall():
    if not key == 'welcome_text':
        print_log('Loaded ' + key + ': ' + str(kv.get(key)))

kv.dump()

######    
# Closing Log file 
print_log("Process completed")
