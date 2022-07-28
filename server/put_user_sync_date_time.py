##################################################
# Application: ERPNext
# Installation: AFSM
# Server Script API: put_user_sync_date_time
# Description: Update the last API call
##################################################

# Receive date from API request
ws_resp_json = json.loads(frappe.request.data)

# Get Branch name using Abbr
branch_name = frappe.db.get_value('Branch', {'abbr': ws_resp_json["branch"]}, ['name'])

# Update last date time of this API call
frappe.db.set_value('Branch', branch_name, 'user_sync_date_time', ws_resp_json["date"])
