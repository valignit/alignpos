##################################################
# Application:  ERPNext
# Installation: AFSM
# Server Script Doc Event: update_item_price
#               Doc Type:  Item Price
# Description:  Update the Standard Selling Rate in Item DocType whenever the price update take place
##################################################

doc_item = frappe.get_doc("Item", doc.item_code)
if (doc.price_list == "Standard Selling"):
    doc_item.standard_rate = doc.price_list_rate
doc_item.item_sync_date_time = frappe.utils.get_datetime()
doc_item.save()