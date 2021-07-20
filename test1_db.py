from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import os
import json

with open('./alignpos.json') as file_config:
  config = json.load(file_config)
  
db_pos_host = config["db_pos_host"]
db_pos_port = config["db_pos_port"]
db_pos_name = config["db_pos_name"]
db_pos_user = config["db_pos_user"]
db_pos_passwd = config["db_pos_passwd"]

conn_str = 'mariadb+mariadbconnector://{}:{}@{}:{}/{}'.format(db_pos_user, db_pos_passwd, db_pos_host, db_pos_port, db_pos_name)
engine = create_engine(conn_str)

Base = automap_base()
Base.prepare(engine, reflect=True)

session = Session(engine)

for table in Base.classes:
    table_name = str(table)[31:-2]
    if table_name == 'tabCustomer':
        Customer = table
    if table_name == 'tabItem':
        Item = table
    if table_name == 'tabEstimate':
        Estimate = table
    if table_name == 'tabEstimate Item':
        EstimateItem = table
    if table_name == 'tabInvoice':
        Invoice = table
    if table_name == 'tabInvoice Item':
        InvoiceItem = table
    if table_name == 'tabExchange Adjustment':
        ExchangeAdjustment = table
    if table_name == 'tabSequence':
        Sequence = table
        
        
cursor = session.query(InvoiceItem)

for invoice_item in cursor:
    print (invoice_item.name)
'''
for item_code in ('9991', '9992'):
    session.add(Item(name = item_code, item_code = item_code, item_name=item_code, barcode=item_code))
session.commit()
'''
