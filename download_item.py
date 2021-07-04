##################################################
# Application: alignPOS
# Installation: AFSM
# CLI Program: download-item
# Description: Send the list of all Items along with details including Stock and Price
# Version: 1.0
# 1.0.0 - 25-04-2021: New program
##################################################

import json
import requests
import mariadb
import sys
import datetime


now = datetime.datetime.now()

with open('./alignpos.json') as file_config:
  config = json.load(file_config)
  
file_name = str(__file__)[:-3] + "-" + now.strftime("%Y%m%d%H%M") + ".log"
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
print_log('alignPOS - Download Item - Version 1.1')
print_log('--------------------------------------')

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
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.ConnectionError as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.Timeout as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.RequestException as ws_err:
    print_log(f"ERP web service error: {ws_err}")
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
    print_log(f"POS database error: {db_err}")
    sys.exit(1)
    
db_pos_cur = db_pos_conn.cursor()


######
# Delete old Item records
db_pos_sql_stmt = (
    "DELETE FROM tabItem"
)

try:
    db_pos_cur.execute(db_pos_sql_stmt)
    db_pos_conn.commit()
    print_log("Old Item records Deleted")
except mariadb.Error as db_err:
    print_log(f"POS database error: {db_err}")
    db_pos_conn.rollback()
    sys.exit(1)


######
# Fetch List of Items from ERP
ws_erp_method = '/api/resource/Item?limit_page_length=None'
try:
    ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method)
    ws_erp_resp.raise_for_status()   
    ws_erp_resp_text = ws_erp_resp.text
    ws_erp_resp_json = json.loads(ws_erp_resp_text)
    #print_log(ws_erp_resp_text)
except requests.exceptions.HTTPError as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.ConnectionError as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.Timeout as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.RequestException as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)

######
# Fetch each Item from Item List from ERP   
item_count = 0
for ws_erp_row_item in ws_erp_resp_json["data"]:
    #print_log(str(ws_erp_row_item))
    item_count+=1
    ws_erp_method = '/api/resource/Item/' + str(ws_erp_row_item["name"])
    try:
        ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method)
        ws_erp_resp.raise_for_status()   
        ws_erp_resp_text = ws_erp_resp.text
        ws_erp_resp_json = json.loads(ws_erp_resp_text)
        #print_log(ws_erp_resp_text)
    except requests.exceptions.HTTPError as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.Timeout as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.RequestException as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)

    item_name = ws_erp_resp_json["data"]["name"]
    item_code = ws_erp_resp_json["data"]["item_code"]
    item_item_name = ws_erp_resp_json["data"]["item_name"]
    item_group = ws_erp_resp_json["data"]["item_group"]
    item_stock = ws_erp_resp_json["data"]["shop_stock"]
    item_selling_price = ws_erp_resp_json["data"]["standard_rate"]
    item_maximum_retail_price = ws_erp_resp_json["data"]["maximum_retail_price"]
    #print(str(item_selling_price),',',str(item_maximum_retail_price))
    
    # Pick first uom of the Item
    item_uom = 'Nos'
    for uom in ws_erp_resp_json["data"]["uoms"]:
        item_uom = uom["uom"]
        #print_log(item_uom)
        break

    # Pick first barcode of the Item
    item_barcode = item_code
    for barcode in ws_erp_resp_json["data"]["barcodes"]:
        item_barcode = barcode["name"]
        #print_log(item_barcode)
        break
        
    # Pick first Tax template of the Item
    for tax in ws_erp_resp_json["data"]["taxes"]:
        item_tax_template = tax["item_tax_template"]
        #print_log(item_tax_template)        
        break

    # Fetch Item Tax Template details 
    ws_erp_method = '/api/resource/Item Tax Template/' 
    try:
        ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method + item_tax_template)
        ws_erp_resp.raise_for_status()   
        ws_erp_resp_text = ws_erp_resp.text
        ws_erp_resp_json = json.loads(ws_erp_resp_text)
        #print_log(ws_erp_resp_text)
    except requests.exceptions.HTTPError as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.Timeout as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.RequestException as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)

    # Pick Tax rates from Tax Template
    for tax in ws_erp_resp_json["data"]["taxes"]:
        if tax["tax_type"] == 'CGST - AFSM':
            cgst_tax_rate = tax["tax_rate"]
        if tax["tax_type"] == 'SGST - AFSM':
            sgst_tax_rate = tax["tax_rate"]
             
        #print_log(cgst_tax_rate)        
    
    db_pos_sql_stmt = (
       "INSERT INTO tabItem (name, item_code, item_name, item_group, barcode, uom, stock, selling_price, maximum_retail_price, cgst_tax_rate, sgst_tax_rate, creation, owner)"
       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s)"
    )
    db_pos_sql_data = (item_name, item_code, item_item_name, item_group, item_barcode, item_uom, item_stock, item_selling_price, item_maximum_retail_price, cgst_tax_rate, sgst_tax_rate, ws_erp_user)

    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        db_pos_conn.commit()
        #print_log(f"Inserted Item: {item_name}")
    except mariadb.Error as db_err:
        print_log(f"POS database error: {db_err}")
        db_pos_conn.rollback()
        sys.exit(1)
    

print_log(f"Total Items Inserted: {item_count}")

######    
# Closing DB connection
db_pos_conn.close()

######    
# Closing Log file 
print_log("Item Upload process completed")
file_log.close()
