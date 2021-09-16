doc_invoice = frappe.get_doc({
    "doctype" : "Sales Invoice",
    "tax_invoice_number" : doc.name,
    "name" : doc.name,
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
doc_invoice.submit()

###
cash_amount = float(doc.cash_amount) - float(doc.cash_return)
if float(cash_amount) > 0:
    doc_payment_entry = frappe.get_doc({
        "doctype" : "Payment Entry",
        "company" : "Al Faridha Super Market",
        "payment_type" : "Receive",
        "posting_date" : frappe.utils.nowdate(),
        "party_type" : "Customer",
        "party" : doc.customer, 
        "mode_of_payment" : "Cash",
        "reference_no" : "1122",
        "reference_date" : frappe.utils.nowdate(),
        "paid_from" : "Debtors - AFSM",
        "paid_to" : "Cash - AFSM",
        "paid_to_account_currency" : "INR",
        "paid_amount" : cash_amount,
        "received_amount" : cash_amount
    })

    doc_payment_entry.append('references', {
        'reference_doctype': "Sales Invoice",
        'reference_name': doc.name,
        'allocated_amount': cash_amount
    })
    doc_payment_entry.insert()
    doc_payment_entry.submit()

###
if float(doc.card_amount) > 0:
    doc_payment_entry = frappe.get_doc({
        "doctype" : "Payment Entry",
        "company" : "Al Faridha Super Market",
        "payment_type" : "Receive",
        "posting_date" : frappe.utils.nowdate(),
        "party_type" : "Customer",
        "party" : doc.customer, 
        "mode_of_payment" : "Credit Card",
        "reference_no" : "1122",
        "reference_date" : frappe.utils.nowdate(),
        "paid_from" : "Debtors - AFSM",
        "paid_to" : "Bank - AFSM",
        "paid_to_account_currency" : "INR",
        "paid_amount" : doc.card_amount,
        "received_amount" : doc.card_amount
    })

    doc_payment_entry.append('references', {
        'reference_doctype': "Sales Invoice",
        'reference_name': doc.name,
        'allocated_amount': doc.card_amount
    })
    doc_payment_entry.insert()
    doc_payment_entry.submit()

###
if float(doc.exchange_amount) > 0:
    doc_payment_entry = frappe.get_doc({
        "doctype" : "Payment Entry",
        "company" : "Al Faridha Super Market",
        "payment_type" : "Receive",
        "posting_date" : frappe.utils.nowdate(),
        "party_type" : "Customer",
        "party" : doc.customer, 
        "mode_of_payment" : "Exchange Adjustment",
        "reference_no" : "1122",
        "reference_date" : frappe.utils.nowdate(),
        "paid_from" : "Debtors - AFSM",
        "paid_to" : "Exchange Adjustment - AFSM",
        "paid_to_account_currency" : "INR",
        "paid_amount" : doc.exchange_amount,
        "received_amount" : doc.exchange_amount
    })

    doc_payment_entry.append('references', {
        'reference_doctype': "Sales Invoice",
        'reference_name': doc.name,
        'allocated_amount': doc.exchange_amount
    })
    doc_payment_entry.insert()
    doc_payment_entry.submit()
    
#frappe.db.set_value('Alignpos Parameters', 'Alignpos Parameters', 'invoice_sync_date_time', doc.creation)
