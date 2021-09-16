import os
import json


class Config():

    def __init__(self):
        self.__application_path = os.environ['ALIGNPOS_PATH']
        with open(self.__application_path + '/app_config.json') as file_config:
          config = json.load(file_config)

        self.__config = config
        
        self.__language = config["language"]
        self.__terminal_id = config["terminal_id"]
        self.__branch_id = config["branch_id"]
        self.__ws_host = config["ws_host"]
        self.__ws_user = config["ws_user"]
        self.__ws_passwd = config["ws_passwd"]
        self.__db_host = config["db_host"]
        self.__db_port = config["db_port"]
        self.__db_database = config["db_database"]
        self.__db_user = config["db_user"]
        self.__db_passwd = config["db_passwd"]
        self.__kv_settings = config["kv_settings"]
        self.__kv_strings = config["kv_strings"]
        self.__log_folder_path = config["log_folder_path"]

    def get_application_path(self):
        return(self.__application_path)
    
    def get_terminal_id(self):
        return(self.__terminal_id)
    
    def get_branch_id(self):
        return(self.__branch_id)
    
    def get_language(self):
        return(self.__language)
    
    def get_ws_host(self):
        return(self.__ws_host)
       
    def get_ws_user(self):
        return(self.__ws_user)
       
    def get_ws_passwd(self):
        return(self.__ws_passwd)
       
    def get_db_host(self):
        return(self.__db_host)
       
    def get_db_port(self):
        return(self.__db_port)
       
    def get_db_database(self):
        return(self.__db_database)
       
    def get_db_user(self):
        return(self.__db_user)
       
    def get_db_passwd(self):
        return(self.__db_passwd)
       
    def get_kv_settings(self):
        return(self.__kv_settings)
       
    def get_kv_strings(self):
        return(self.__kv_strings)
       
    def get_log_folder_path(self):
        return(self.__log_folder_path)

    def get_value(self, key):
        return self.__config[key]
        
    application_path = property(get_application_path)         
    terminal_id = property(get_terminal_id)         
    branch_id = property(get_branch_id)         
    language = property(get_language)         
    ws_host = property(get_ws_host)         
    ws_user = property(get_ws_user)         
    ws_passwd = property(get_ws_passwd)         
    db_host = property(get_db_host)         
    db_port = property(get_db_port)         
    db_database = property(get_db_database)         
    db_user = property(get_db_user)         
    db_passwd = property(get_db_passwd)         
    kv_settings = property(get_kv_settings)         
    kv_strings = property(get_kv_strings)         
    log_folder_path = property(get_log_folder_path)
    