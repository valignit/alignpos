doc_invoice = frappe.get_doc({
    "doctype" : "Sales Invoice",
    "name" : doc_invoice.name,
    "company" : "Al Faridha Super Market",
    "posting_date" : frappe.utils.nowdate(),
    "due_date" : frappe.utils.nowdate(),
    "customer" : doc_invoice.customer,
    "currency" : "INR",
    "conversion_rate" : "1.0",
    "selling_price_list" : "Standard Selling",
    "price_list_currency" : "INR",
    "plc_conversion_rate" : "1.0",
    "net_total" : "900.00",
    "base_net_total" : "900.00",
    "grand_total" : "900.00",
    "base_grand_total" : "900.00",
    "update_stock": 1,
    "debit_to" : "Debtors - AFSM"
})

doc_invoice.append('taxes', {
    'charge_type': 'On Net Total',
    'account_head': 'CGST-AFSM',
    'description': 'CGST',
    'included_in_print_rate': 1,
    'tax_amount': doc_invoice.cgst_tax_amount
})
 
doc_invoice.append('taxes', {
    'charge_type': 'On Net Total',
    'account_head': 'SGST-AFSM',
    'description': 'SGST',
    'included_in_print_rate': 1,
    'tax_amount': doc_invoice.sgst_tax_amount
})

for item in doc.items:
    amount = float(item.qty) * float(item.applied_selling_price)
    doc_invoice.append('items', {
        'item_code': item.item,
        'item_name': "xxxxxx",
        'description': "POS",
        "uom" : "Unit",
        "qty" : item.qty,
        "conversion_factor" : "1.000",
        "rate" : item.applied_selling_price,
        "amount" : amount,
        "base_rate" : item.applied_selling_price,
        "base_amount" : amount
    })
    
doc_invoice.insert()
doc_invoice.submit()

frappe.db.set_value('Alignpos Parameters', 'Alignpos Parameters', 'invoice_sync_date_time', doc.creation)
