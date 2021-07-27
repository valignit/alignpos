from sqlalchemy import create_engine, exc, text, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import os
import sys
import json
import warnings


###
# alignpos Database Connection
class DbConn():

    def __init__(self):
        self.__engine = None
        self.__session = None
        self.__table = None
        self.__table_name = ''
        self.__customer_table = None 
        
        with open('./alignpos.json') as file_config:
          config = json.load(file_config)

        db_pos_host = config["db_pos_host"]
        db_pos_port = config["db_pos_port"]
        db_pos_database = config["db_pos_database"]
        db_pos_user = config["db_pos_user"]
        db_pos_passwd = config["db_pos_passwd"]         
       
        conn_str = 'mariadb+mariadbconnector://{}:{}@{}:{}/{}'.format(db_pos_user, db_pos_passwd, db_pos_host, db_pos_port, db_pos_database)
        self.__engine = create_engine(conn_str)
        self.__session = Session(self.__engine)
        metadata = MetaData()
        metadata.reflect(self.__engine)
        self.__base = automap_base(metadata=metadata)        
        self.__base.prepare(self.__engine, reflect=True)
        
              
    def get_session(self):
        return self.__session
        
    def get_engine(self):
        return self.__engine
        
    def get_base(self):
        return self.__base

    def close(self):
        self.__session.close()    
        self.__engine.dispose()    

    session = property(get_session) 
    engine = property(get_engine) 
    base = property(get_base) 


###
# alignpos Database Table interface
class DbTable():

    def __init__(self, conn, table_name):
        self.__conn = conn
        self.__table_name = table_name
        self.__list = None        
        self.__row = None
        self.__count = 0

        switcher = {
            'tabCustomer': conn.base.classes.tabCustomer,
            'tabItem': conn.base.classes.tabItem,
            'tabEstimate': conn.base.classes.tabEstimate,
            'tabEstimate_Item': conn.base.classes.tabEstimate_Item,
            'tabInvoice': conn.base.classes.tabInvoice,
            'tabInvoice_Item': conn.base.classes.tabInvoice_Item,
            'tabExchange': conn.base.classes.tabExchange,
            'tabSequence': conn.base.classes.tabSequence,
            'tabUser': conn.base.classes.tabUser,
        }
        self.__table = switcher.get(table_name)
        
    def new_row(self):
        self.__row = self.__table()
        return self.__row
               
    def get_row(self, name):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__row = self.__conn.session.query(self.__table).get(name)
                return self.__row
            except exc.SQLAlchemyError as db_err:
                print("Database error 201 while get_row() in {}\nProcess Terminated\n{}".format(self.__table_name, db_err))
                sys.exit(1)
                   
    def create_row(self, row):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__conn.session.add(row)
                self.__conn.session.flush()               
            except exc.SQLAlchemyError as db_err:
                print("Database error 202 while create_row() in {}\nProcess Terminated\n{}".format(self.__table_name, db_err))
                sys.exit(1)
                
    def update_row(self, row):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__conn.session.add(row)
                self.__conn.session.flush()                               
            except exc.SQLAlchemyError as db_err:
                print("Database error 203 while update_row() in {}\nProcess Terminated\n{}".format(self.__table_name, db_err))
                sys.exit(1)

    def delete_row(self, row):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__conn.session.delete(row)
                self.__conn.session.flush()                               
            except exc.SQLAlchemyError as db_err:
                print("Database error 204 while delete_row() in {}\nProcess Terminated\n{}".format(self.__table_name, db_err))
                sys.exit(1)

    def count(self, filter):
        self.__list = self.list(filter)
        self.__count = len(self.__list)                
        return(self.__count)
   
    def list(self, filter):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__list = self.__conn.session.query(self.__table).filter(text(filter)).all()       
            except exc.SQLAlchemyError as db_err:
                print("Database error 205 while list() in {}\nProcess Terminated\n{}".format(self.__table_name, db_err))
                sys.exit(1)    
            return self.__list
   
    def first(self, filter):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__row = self.__conn.session.query(self.__table).filter(text(filter)).first()        
            except exc.SQLAlchemyError as db_err:
                print("Database error 206 while first() in {}\nProcess Terminated\n{}".format(self.__table_name, db_err))
                sys.exit(1)
            return self.__row

    def last(self, filter):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__row = self.__conn.session.query(self.__table).filter(text(filter)).order_by(self.__table.name.desc()).first()       
            except exc.SQLAlchemyError as db_err:
                print("Database error 207 while last() in {}\nProcess Terminated\n{}".format(self.__table_name, db_err))
                sys.exit(1)    
            return self.__row


###
# alignpos Database Query interface
class DbQuery():

    def __init__(self, conn, query):
        self.__conn = conn
        self.__query = query        
        self.__result = None        
        with self.__conn.engine.connect().execution_options(autocommit=True) as connection:
            self.__result = connection.execute(self.__query)
    
    def get_result(self):
        return self.__result

    result = property(get_result)
    
######
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')

        