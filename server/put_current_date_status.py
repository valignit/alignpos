##################################################
# Application: ERPNext
# Installation: AFSM
# Server Script API: put_current_date_status
# Description: Update the last API call
##################################################

# Receive date from API request
ws_resp_json = json.loads(frappe.request.data)

# Get Branch name using Abbr
branch_name = frappe.db.get_value('Branch', {'abbr': ws_resp_json["branch"]}, ['name'])

# Update last date time of this API call
frappe.db.set_value('Branch', branch_name, 'current_date', ws_resp_json["current_date"])
frappe.db.set_value('Branch', branch_name, 'current_status', ws_resp_json["current_status"])
