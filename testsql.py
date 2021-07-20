import os
import json
from testsql_db import DbConn, DbTable, DbQuery

with open('./alignpos.json') as file_config:
  config = json.load(file_config)
  
def main():
    db_pos_host = config["db_pos_host"]
    db_pos_port = config["db_pos_port"]
    db_pos_database = config["db_pos_database"]
    db_pos_user = config["db_pos_user"]
    db_pos_passwd = config["db_pos_passwd"] 
    
    db_conn = DbConn(db_pos_host, db_pos_port, db_pos_database, db_pos_user, db_pos_passwd)
    db_session = db_conn.session

    db_customer_table = DbTable(db_conn, 'tabCustomer')
    db_item_table = DbTable(db_conn, 'tabItem')
    print(db_item_table)   
    customer_cursor = db_customer_table.list('')

    for customer_row in customer_cursor:
        print (customer_row.name)

    db_query = DbQuery(db_conn, 'SELECT nextval("ESTIMATE_NUMBER")')
    for db_row in db_query.result:
        print(db_row[0])
    db_query = DbQuery(db_conn, 'SELECT nextval("ESTIMATE_NUMBER")')
    for db_row in db_query.result:
        print('nextval:', db_row[0])
    
    item_count = db_item_table.count('')
    print(item_count)
    
    db_item_row = db_item_table.new_row()
    db_item_row.name = '9995'
    db_item_row.item_code = '9995'
    db_item_row.item_name = '9995'
    db_item_row.barcode = '9995'
    db_item_table.create_row(db_item_row)
    db_session.commit()
    
    
    
main()