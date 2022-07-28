##################################################
# Application: ERPNext
# Installation: AFSM
# Server Script API: get_updated_customers
# Description: Send the list of Customers updated after the last API call
##################################################

# Receive branch from API request
ws_resp_json = json.loads(frappe.request.data)

# Fetch last date time of this API call
latest_customer_sync_date_time = frappe.db.get_value('Branch', {'abbr': ws_resp_json['branch']}, ['customer_sync_date_time'])

# Fetch all Customers updated after the last date time
customers_list =    frappe.db.get_list('Customer', 
                                filters=[
                                    ['modified', '>', latest_customer_sync_date_time]
                                ],
                                fields=['name'],
                                order_by='modified'
                )

response_list = []
for row in customers_list:
    customer_doc = frappe.get_doc('Customer', row['name'])
    response_list.append(customer_doc)

# Send list of Items as API response
frappe.response['customers'] = response_list
