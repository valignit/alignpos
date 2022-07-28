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
        self.__ws_protocol = config["ws_protocol"]
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
    
    def get_ws_protocol(self):
        return(self.__ws_protocol)
       
    def get_ws_host(self):
        return(self.__ws_host)
       
    def get_ws_user(self):
        return(self.decrypt(self.__ws_user))
       
    def get_ws_passwd(self):
        return(self.decrypt(self.__ws_passwd))
       
    def get_db_host(self):
        return(self.__db_host)
       
    def get_db_port(self):
        return(self.__db_port)
       
    def get_db_database(self):
        return(self.__db_database)
       
    def get_db_user(self):
        return(self.decrypt(self.__db_user))
       
    def get_db_passwd(self):
        return(self.decrypt(self.__db_passwd))
       
    def get_kv_settings(self):
        return(self.__kv_settings)
       
    def get_kv_strings(self):
        return(self.__kv_strings)
       
    def get_log_folder_path(self):
        return(self.__log_folder_path)

    def get_value(self, key):
        return self.__config[key]

    def encrypt(self, decrypt_text):
        enclist=[48,99,55,54,91,79,122,109,78,68,44,77,120,34,70,53,73,40,72,41,123,61,51,64,87,81,126,117,96,80,39,66,60,76,88,98,52,86,124,42,105,65,121,58,38,95,69,63,59,92,119,43,125,89,67,50,46,83,113,45,107,85,104,74,114,62,84,118,100,97,112,93,35,71,103,36,106,57,115,90,110,108,75,47,49,82,116,37,94,111,101,33,102,56]
        encstr=""
        for i in decrypt_text:
            encstr=encstr+chr(enclist[ord(i)-33])
        return encstr


    def decrypt(self, encrypt_text):
        declist=[124,46,105,108,120,77,63,50,52,72,84,43,92,89,116,33,117,88,55,69,48,36,35,126,110,76,81,65,54,98,80,56,74,64,87,42,79,47,106,51,49,96,115,66,44,41,38,62,58,118,90,99,94,70,57,67,86,112,37,82,104,121,78,61,102,68,34,101,123,125,107,95,73,109,93,114,40,113,122,103,91,97,111,119,60,100,83,45,75,39,53,71,85,59]
        decstr=""
        for i in encrypt_text:
            decstr=decstr+chr(declist[ord(i)-33])
        return decstr
        
    application_path = property(get_application_path)         
    terminal_id = property(get_terminal_id)         
    branch_id = property(get_branch_id)         
    language = property(get_language)         
    ws_protocol = property(get_ws_protocol)         
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



    