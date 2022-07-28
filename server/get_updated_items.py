##################################################
# Application: ERPNext
# Installation: AFSM
# Server Script API: get_updated_items
# Description: Send the list of Items updated after the last API call
##################################################

# Receive branch from API request
ws_resp_json = json.loads(frappe.request.data)

# Fetch last date time of this API call
latest_item_sync_date_time = frappe.db.get_value('Branch', {'abbr': ws_resp_json['branch']}, ['item_sync_date_time'])
w_price_list = frappe.db.get_value('Branch', {'abbr': ws_resp_json['branch']}, ['price_list'])

# Fetch all Items updated after the last date time
items_list =    frappe.db.get_list('Item', 
                                filters=[
                                    ['modified', '>', latest_item_sync_date_time]
                                ],
                                fields=['item_code'],
                                order_by='modified'
                )

response_list = []
for row in items_list:
    w_standard_rate = frappe.db.get_value('Item Price', {'item_code': row['item_code'], 'price_list': w_price_list}, ['price_list_rate'])
    item_doc = frappe.get_doc('Item', row['item_code'])
    if w_standard_rate:
        item_doc.standard_rate = w_standard_rate
    response_list.append(item_doc)

# Send list of Items as API response
frappe.response['items'] = response_list

