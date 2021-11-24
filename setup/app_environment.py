import sys
import pickledb
import json
from datetime import date, datetime

sys_path = 'c:\\alignpos\\'
sys.path.append(sys_path)

with open(sys_path + 'app_config.json') as file_config:
  config = json.load(file_config)

today = date.today()
  
######
# Connect to Key Value database
#kv = pickledb.load('data/alignpos_settings.db', False)
kv = pickledb.load(config["kv_settings"], False)

kv.set('tax_included', '')
kv.set('walk_in_customer', '')
kv.set('welcome_text', '')
kv.set('current_date', str(today))

for key in kv.getall():
    print('Loaded', key, ':', kv.get(key))
        
kv.dump()
