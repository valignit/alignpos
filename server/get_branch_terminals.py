##################################################
# Application: ERPNext
# Installation: AFSM
# Server Script API: get_branch_terminals
# Description: Get the list of terminals of a branch
##################################################

# Receive branch from API request
ws_resp_json = json.loads(frappe.request.data)

branch_name = frappe.db.get_value('Branch', {'abbr': ws_resp_json['branch']}, ['name'])

doc_branch = frappe.get_doc("Branch", branch_name)
branch_terminals = doc_branch.terminals

frappe.response['terminals'] = branch_terminals

