import pickledb
import os
import sys
import json
import warnings


###
# alignpos Database Connection
class KvConn():

    def __init__(self):
        self.__kv = None
        
        with open('./alignpos.json') as file_config:
          config = json.load(file_config)

        kv_pos_database = config["kv_pos_database"]
        self.__kv = pickledb.load(kv_pos_database, False)

    def set(self, key, value):
        self.__kv.set(key, value)
        self.__kv.dump()        
        
    def get(self, key):
        print(self.__kv.get(key))
        return self.__kv.get(key)
   

######
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')

        