##################################################
# Application:  ERPNext
# Installation: AFSM
# Server Script Doc Event: Update Item Price
#               Doc Type:  Item Price
# Description:  Update the Standard Selling Rate in Item DocType whenever the 
#               price update take place
# Version:      1.0
# 1.0.0 - 25-04-2021: New program
##################################################

doc_item = frappe.get_doc("Item", doc.item_code)
if (doc.price_list == "Standard Selling"):
    doc_item.standard_rate = doc.price_list_rate
doc_item.item_sync_date_time = frappe.utils.get_datetime()
doc_item.save()