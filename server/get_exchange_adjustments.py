##################################################
# Application: ERPNext
# Installation: AFSM
# Server Script API: get_exchange_adjustments
# Description: Send the list of Exchange Adjustments made after the last API call
##################################################

# Receive branch from API request
ws_resp_json = json.loads(frappe.request.data)

# Fetch last date time of this API call
latest_exchange_sync_date_time = frappe.db.get_value('Branch', {'abbr': ws_resp_json['branch']}, ['exchange_sync_date_time'])


# Fetch all Exchange Adjustments created after the last date time
exchange_adjustments_list =    frappe.db.get_list('Payment Entry', 
                                filters=[
                                    ['creation', '>', latest_exchange_sync_date_time],
                                    ['mode_of_payment', '=', 'Exchange Adjustment'],
                                    ['payment_type', '=', 'Pay']
                                ],
                                fields=['name'],
                                order_by='creation'
                )

response_list = []
for row in exchange_adjustments_list:
    payment_entry_doc = frappe.get_doc('Payment Entry', row['name'])
    response_list.append(payment_entry_doc)

# Send list of Items as API response
frappe.response['exchange_adjustments_list'] = response_list

