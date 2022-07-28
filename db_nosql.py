import pickledb
import os
import sys
import json
import warnings

from config import Config

###
# alignpos Database Connection
class KvDatabase():

    def __init__(self, context):
        self.__kv = None
        config = Config()

        kv_database = config.get_value(context)
        self.__kv = pickledb.load(kv_database, False)

    def set(self, key, value):
        self.__kv.set(key, value)
        self.__kv.dump()        
        
    def get(self, key):
        return self.__kv.get(key)
 
    def getall(self):
        return self.__kv.getall()

    def truncate(self):
        self.__kv.deldb()


######
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')

        