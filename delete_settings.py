##################################################
# Application: alignPOS
# Installation: AFSM
# CLI Program: delete_settings
# Description: Initialize the parameter settings 
# Version: 1.0
# 1.0.0 - 09-07-2021: New program
##################################################

import json
import requests
import pickledb
import sys
from datetime import datetime, timedelta


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

with open('./app_config.json') as file_config:
  config = json.load(file_config)

branch_id = config["branch_id"]

file_name = config["log_folder_path"] + str(__file__)[:-3] + "-" + now.strftime("%Y%m%d%H%M") + ".log"
file_log = open(file_name, "w")

print_log('Download Settings - Version 1.1')

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
# Connect to Key Value database
#kv = pickledb.load('data/alignpos_settings', False)
kv = pickledb.load(config["kv_settings"], False)

kv.deldb()

######
# Fetch module parameters from ERP
ws_erp_method = 'api/resource/Alignpos Parameters/Alignpos Parameters'
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
ws_erp_method = 'api/method/get_branch'
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
#current_date = ws_settings_row["current_date"]
#current_status = ws_settings_row["current_status"]
favorite_items = ws_settings_row["favorites"]
fast_moving_items = ws_settings_row["fast_moving"]
terminals = ws_settings_row["terminals"]

#kv.set('current_date', current_date)
#kv.set('current_status', current_status)

if favorite_items:
    ct = 0
    for item in favorite_items:
        ct += 1
        key = 'favorite_item_' + str(ct)
        kv.set(key, item["name"])
        
if fast_moving_items:
    ct = 0
    for item in fast_moving_items:
        ct += 1
        key = 'fast_moving_item_' + str(ct)
        kv.set(key, item["name"])

if terminals:
    ct = 0
    for terminal in terminals:
        ct += 1
        key = 'terminal_' + str(ct) + '_id'
        kv.set(key, terminal["terminal_id"])
        key = 'terminal_' + str(ct) + '_enabled'
        kv.set(key, terminal["enabled"])

######    
# Closing DB connection
for key in kv.getall():
    if not key == 'welcome_text':
        print_log('Loaded ' + key + ': ' + str(kv.get(key)))

kv.dump()

######    
# Closing Log file 
print_log("Process completed")
