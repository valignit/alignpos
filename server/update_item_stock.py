##################################################
# Application:  ERPNext
# Installation: AFSM
# Server Script Doc Event: update_item_stock
#               Doc Type:  Bin
# Description:  Update the Shop stock and Stores stock in Item DocType whenever the stock transactions take place
##################################################

doc_item = frappe.get_doc("Item", doc.item_code)
if (doc.warehouse == "Stores - AFSM"):
    doc_item.stores_stock = doc.actual_qty
elif (doc.warehouse == "Shop - AFSM"):
    doc_item.shop_stock = doc.actual_qty
doc_item.item_sync_date_time = frappe.utils.get_datetime()
doc_item.save()