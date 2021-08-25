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


##############################
# Main
##############################
print_log('alignPOS - Upload Invoices - Version 1.1')
print_log('----------------------------------------')

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
# Fetch Invoices

db_pos_sql_stmt = (
    "SELECT * FROM `tabInvoice` WHERE invoice_number is not null and posting_date is null"
)
try:
    db_pos_cur.execute(db_pos_sql_stmt)
except mariadb.Error as db_err:
    print_log(f"POS database error 102: {db_err}")
    sys.exit(1)

db_invoice_rows = db_pos_cur.fetchall()

posting_date = None
  
for invoice_row in db_invoice_rows :
    invname = invoice_row[0]
    invoice_number = invoice_row[1]
    customer = invoice_row[3]
    cgst_tax_amount = invoice_row[4]
    sgst_tax_amount = invoice_row[5]
    total_amount = invoice_row[6]
    discount_amount = invoice_row[7]
    invoice_amount = invoice_row[8]
    exchange_amount = invoice_row[9]
    exchange_reference = ''
    redeemed_points = invoice_row[11]
    redeemed_amount = invoice_row[12]
    cash_amount = invoice_row[13]
    card_amount = invoice_row[14]
    card_reference = invoice_row[15]
    cash_return = invoice_row[16]
    paid_amount = invoice_row[17]
    home_delivery = invoice_row[18]
    terminal_id = invoice_row[19]
    approved_by = invoice_row[20]

    if not discount_amount:
        discount_amount = 0
    if not exchange_amount:
        exchange_amount = 0
    if not redeemed_amount:
        redeemed_amount = 0
    if not paid_amount:
        paid_amount = 0
        
    payload_invoice = '\
"doctype": "Alignpos Invoice",\
"docstatus": 0,\
"name": "{}",\
"invoice_number": "{}",\
"customer": "{}",\
"total_amount": "{}",\
"discount_amount": "{}",\
"cgst_tax_amount": "{}",\
"sgst_tax_amount": "{}",\
"invoice_amount": "{}",\
"exchange_amount": "{}",\
"exchange_reference": "{}",\
"redeemed_points": "{}",\
"redeemed_amount": "{}",\
"cash_amount": "{}",\
"card_amount": "{}",\
"card_reference": "{}",\
"cash_return": "{}",\
"paid_amount": "{}",\
"home_delivery": "No",\
"terminal_id": "{}",'.format(
invname,
invoice_number,
customer,
"{:.2f}".format(total_amount),
"{:.2f}".format(discount_amount),
"{:.2f}".format(cgst_tax_amount),
"{:.2f}".format(sgst_tax_amount),
"{:.2f}".format(invoice_amount),
"{:.2f}".format(exchange_amount),
exchange_reference,
redeemed_points,
"{:.2f}".format(redeemed_amount),
"{:.2f}".format(cash_amount),
"{:.2f}".format(card_amount),
card_reference,
"{:.2f}".format(cash_return),
"{:.2f}".format(paid_amount),
home_delivery,
terminal_id
)
    payload_invoice = '{ ' + payload_invoice + '"items": ['
    db_pos_sql_stmt = (
        "SELECT * FROM `tabInvoice_item` WHERE parent = '" + invname + "'" 
    )
    try:
        db_pos_cur.execute(db_pos_sql_stmt)
    except mariadb.Error as db_err:
        print_log(f"POS database error 102: {db_err}")
        sys.exit(1)

    db_invoice_item_rows = db_pos_cur.fetchall()
   
    for invoice_item_row in db_invoice_item_rows :
        itemname = invoice_item_row[0]
        item = invoice_item_row[2]
        qty = invoice_item_row[3]
        standard_selling_price = invoice_item_row[4]
        applied_selling_price = invoice_item_row[5]
        cgst_tax_rate = invoice_item_row[7]
        sgst_tax_rate = invoice_item_row[8]
        approved_by = invoice_item_row[9]

        if not standard_selling_price:
            standard_selling_price = 0
        if not applied_selling_price:
            applied_selling_price = 0

        payload_item = '\
"name": "{}",\
"parent": "{}",\
"parentfield": "Items",\
"parenttype": "Alignpos Invoice",\
"item": "{}",\
"qty": "{}",\
"standard_selling_price": "{}",\
"applied_selling_price": "{}",\
"cgst_tax_rate": "{}",\
"sgst_tax_rate": "{}",\
"approved_by": "{}"'.format(
itemname,
invname,
item,
qty,
"{:.2f}".format(standard_selling_price),
"{:.2f}".format(applied_selling_price),
cgst_tax_rate,
sgst_tax_rate,
approved_by
)
        payload_item = '{' + payload_item + '},'
        payload_invoice = payload_invoice + payload_item
    payload_invoice = payload_invoice[:-1] + ']}'
    print(payload_invoice)

    ws_erp_method = 'api/resource/Alignpos Invoice'
    try:
        ws_erp_resp = ws_erp_sess.post(ws_erp_host + ws_erp_method, data=payload_invoice)
        ws_erp_resp.raise_for_status()   
        ws_erp_resp_text = ws_erp_resp.text
        ws_erp_resp_json = json.loads(ws_erp_resp_text)
        #print(ws_erp_resp_text)
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

    print(ws_erp_resp_json["data"]["creation"])
    
    posting_date = str(ws_erp_resp_json["data"]["creation"])

if posting_date:
    sql_update_query = 'Update tabInvoice set posting_date = "{}"'.format(posting_date)

    try:
        db_pos_cur.execute(sql_update_query, input)
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
