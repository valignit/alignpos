##################################################
# Application: ERPNext
# Installation: AFSM
# Server Script API: get_created_users 
# Description: Send the list of all Users with Alignpos User and Alignpos Manager roles
##################################################

# Receive branch from API request
ws_resp_json = json.loads(frappe.request.data)

# Fetch last date time of this API call
latest_user_sync_date_time = frappe.db.get_value('Branch', {'abbr': ws_resp_json['branch']}, ['user_sync_date_time'])

response_list = []

user_roles_list =    frappe.db.get_list('Has Role', 
                                filters=[
                                    ['role', 'like', 'Alignpos%'],
                                    ['creation', '>', latest_user_sync_date_time]
                                ],
                                fields=['name','parent']
                )
for row in user_roles_list:
    user_doc = frappe.get_doc('User', row['parent'])
    user_list = []
    user_list.append(user_doc.username)
    user_list.append(user_doc.full_name)
    user_list.append(user_doc.enabled)
    dictionary ={  
      "username": user_doc.username,  
      "full_name": user_doc.full_name,
      "role": 'Alignpos User',
      "enabled": user_doc.enabled,
      "creation": str(user_doc.creation)
    }
    response_list.append(dictionary)

user_roles_list =    frappe.db.get_list('Has Role', 
                                filters=[
                                    ['role', '=', 'Alignpos Manager'],
                                    ['creation', '>', latest_user_sync_date_time]
                                ],
                                fields=['name','parent']
                )
for row in user_roles_list:
    user_doc = frappe.get_doc('User', row['parent'])
    user_list = []
    user_list.append(user_doc.username)
    user_list.append(user_doc.full_name)
    dictionary ={  
      "username": user_doc.username,  
      "full_name": user_doc.full_name,
      "role": 'Alignpos Manager',
      "enabled": user_doc.enabled,
      "creation": str(user_doc.creation)
    }
    response_list.append(dictionary)  
       
# Serializing json   
json_object = json.dumps(response_list, indent = 4)

response_user_list = json.loads(json_object)

# Send list of Users as API response
frappe.response['users']= response_user_list
