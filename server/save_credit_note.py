##################################################
# Application:  ERPNext
# Installation: AFSM
# Server Script Doc Event: save_credit_note
#               Doc Type:  Sales Invoice
# Description:  
##################################################

if doc.is_return == 1:
    doc.tax_invoice_number = doc.tax_invoice_number + '-CN'
  