import json
import sys
from sqlalchemy.orm import sessionmaker, mapper, registry
from sqlalchemy import create_engine, MetaData, Table, exc, text, func
import warnings

with open('./alignpos.json') as file_config:
  config = json.load(file_config)


###
# Table Layouts
class Customer(object):
    pass

class Item(object):
    pass    

class Invoice(object):
    pass    

class InvoiceItem(object):
    pass    

class Estimate(object):
    pass    

class EstimateItem(object):
    pass    

class ExchangeAdjustment(object):
    pass    


###
# Database Connection object for alignpos
class ConnAlignPos():

    def __init__(self):

        self.__engine = None
        self.__session = None
        self.__text = None
             
        db_pos_host = config["db_pos_host"]
        db_pos_port = config["db_pos_port"]
        db_pos_name = config["db_pos_name"]
        db_pos_user = config["db_pos_user"]
        db_pos_passwd = config["db_pos_passwd"]
        
        conn_str = 'mariadb+mariadbconnector://{}:{}@{}:{}/{}'.format(db_pos_user, db_pos_passwd, db_pos_host, db_pos_port, db_pos_name)

        self.__engine = create_engine(conn_str)
        
        db_table_meta = MetaData(self.__engine)
        db_err = ''

        try:
            db_table_meta.reflect()
        except exc.SQLAlchemyError as db_err:
            print(f"Database error 101 while connecting {db_pos_name}\nProcess Terminated\n{db_err}")
            sys.exit(1)    

        # Table mappers - add additional tables as required
        mapper(Customer, Table('tabCustomer', db_table_meta, autoload=True))
        mapper(Item, Table('tabItem', db_table_meta, autoload=True))
        mapper(Invoice, Table('tabInvoice', db_table_meta, autoload=True))
        mapper(InvoiceItem, Table('tabInvoice Item', db_table_meta, autoload=True))
        mapper(Estimate, Table('tabEstimate', db_table_meta, autoload=True))
        mapper(EstimateItem, Table('tabEstimate Item', db_table_meta, autoload=True))
        mapper(ExchangeAdjustment, Table('tabExchange Adjustment', db_table_meta, autoload=True))
        
        db_session = sessionmaker(bind=self.__engine)
        self.__session = db_session()
        
    def get_session(self):
        return self.__session
        
    def get_engine(self):
        return self.__engine
      
    def get_text(self):
        self.__text = text
        return self.__text
          
    def close(self):
        self.__session.close()    
        self.__engine.dispose()    

    session = property(get_session) 
    engine = property(get_engine) 
    text = property(get_text) 
  

###
# Generic Database Table interface
class DbTable():

    def __init__(self, conn, table):
        self.__conn = conn
        self.__table = table        
        self.__list = None        
        self.__row = None
        self.__count = 0
                
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
                print("Database error 201 while get_row() in {self.__table.name}\nProcess Terminated\n{db_err}")
                sys.exit(1)
                   
    def create_row(self, row):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__conn.session.add(row)
                self.__conn.session.flush()               
            except exc.SQLAlchemyError as db_err:
                print("Database error 202 while create_row() in {self.__table.name}\nProcess Terminated\n{db_err}")
                sys.exit(1)
                
    def update_row(self, row):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__conn.session.add(row)
                self.__conn.session.flush()                               
            except exc.SQLAlchemyError as db_err:
                print("Database error 203 while update_row() in {self.__table.name}\nProcess Terminated\n{db_err}")
                sys.exit(1)

    def delete_row(self, row):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__conn.session.delete(row)
                self.__conn.session.flush()                               
            except exc.SQLAlchemyError as db_err:
                print("Database error 204 while delete_row() in {self.__table.name}\nProcess Terminated\n{db_err}")
                sys.exit(1)

    def count(self, filter):
        self.__list = self.list(filter)
        self.__count = len(self.__list)                
        return(self.__count)
   
    def list(self, filter):
        print(filter)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__list = self.__conn.session.query(self.__table).filter(text(filter)).all()       
            except exc.SQLAlchemyError as db_err:
                print(f"Database error 205 while list() in {self.__table.name}\nProcess Terminated\n{db_err}")
                sys.exit(1)    
            return self.__list
   
    def first(self, filter):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__row = self.__conn.session.query(self.__table).filter(text(filter)).first()        
            except exc.SQLAlchemyError as db_err:
                print(f"Database error 206 while first() in {self.__table.name}\nProcess Terminated\n{db_err}")
                sys.exit(1)
            return self.__row

    def last(self, filter):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=exc.SAWarning)
            try:
                self.__row = self.__conn.session.query(self.__table).filter(text(filter)).order_by(self.__table.name.desc()).first()       
            except exc.SQLAlchemyError as db_err:
                print(f"Database error 207 while last() in {self.__table.name}\nProcess Terminated\n{db_err}")
                sys.exit(1)    
            return self.__row


###
# Generic Database Query interface
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
