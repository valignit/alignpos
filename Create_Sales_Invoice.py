doc_invoice = frappe.get_doc({
    "doctype" : "Sales Invoice",
    "company" : "Al Faridha Super Market",
    "customer" : doc.customer,
    "posting_date" : frappe.utils.nowdate(),
    "due_date" : frappe.utils.nowdate(),
    "currency" : "INR",
    "conversion_rate" : "1.0",
    "selling_price_list" : "Standard Selling",
    "price_list_currency" : "INR",
    "plc_conversion_rate" : "1.0",
    "debit_to" : "Debtors - AFSM"
})

doc_invoice.append('taxes', {
    'charge_type': 'On Net Total',
    'account_head': 'CGST - AFSM',
    'description': 'CGST',
    'included_in_print_rate': 0,
    'tax_amount': doc.cgst_tax_amount
})
 
doc_invoice.append('taxes', {
    'charge_type': 'On Net Total',
    'account_head': 'SGST - AFSM',
    'description': 'SGST',
    'included_in_print_rate': 0,
    'tax_amount': doc.sgst_tax_amount
})

for invoice_item in doc.items:
    amount = float(invoice_item.qty) * float(invoice_item.applied_selling_price)
    doc_invoice.append('items', {
        'item_code': invoice_item.item,
        'description': "POS",
        "uom" : invoice_item.uom,
        "qty" : invoice_item.qty,
        "conversion_factor" : "1.000",
        "rate" : invoice_item.applied_selling_price,
        "amount" : amount
    })
    
doc_invoice.insert()
#doc_invoice.submit()

#frappe.db.set_value('Alignpos Parameters', 'Alignpos Parameters', 'invoice_sync_date_time', doc.creation)
