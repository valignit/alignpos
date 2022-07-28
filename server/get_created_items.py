##################################################
# Application: ERPNext
# Installation: AFSM
# Server Script API: get_created_items
# Description: Send the list of Items created after the last API call
##################################################

# Receive branch from API request
ws_resp_json = json.loads(frappe.request.data)

# Fetch last date time of this API call
latest_item_sync_date_time = frappe.db.get_value('Branch', {'abbr': ws_resp_json['branch']}, ['item_sync_date_time'])

# Fetch all Items created after the last date time
items_list =    frappe.db.get_list('Item', 
                                filters=[
                                    ['creation', '>', latest_item_sync_date_time]
                                ],
                                fields=['item_code'],
                                order_by='creation'
                )

response_list = []
for row in items_list:
    item_doc = frappe.get_doc('Item', row['item_code'])
    response_list.append(item_doc)

# Send list of Items as API response
frappe.response['items'] = response_list

