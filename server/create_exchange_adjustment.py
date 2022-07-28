##################################################
# Application:  ERPNext
# Installation: AFSM
# Server Script Doc Event:  create_exchange_adjustment
#               Doc Type:   Sales Invoice
#               Event:      After Submit
# Description:  Automatically create Exchange Adjustment Payment Entry when the Sales Invoice Return is submitted
##################################################
doc_sales_invoice = doc
payment_amount = doc_sales_invoice.rounded_total * -1 
allocated_amount = doc_sales_invoice.rounded_total 
msgstr = 'Server Script:' + str(payment_amount) + str(allocated_amount)
frappe.msgprint(msgstr)

if doc_sales_invoice.is_return == 1:
    frappe.msgprint('here1')
    doc_payment_entry = frappe.get_doc({
        'doctype' : "Payment Entry",
        'company' : doc_sales_invoice.company,
        'payment_type' : "Pay",
        'posting_date' : frappe.utils.nowdate(),
        'party_type' : "Customer",
        'party' : doc_sales_invoice.customer,
        'mode_of_payment' : "Exchange Adjustment",
        'paid_from' : "Exchange Adjustment - AFSM",
        'paid_to' : "Debtors - AFSM",
        'paid_amount' : payment_amount,
        'received_amount' : payment_amount
    })
    doc_payment_entry.append("references", {
        'reference_doctype': "Sales Invoice",
        'reference_name': doc_sales_invoice.return_against,
        'allocated_amount': allocated_amount
    })
    doc_payment_entry.insert()
    doc_payment_entry.submit()
