import frappe
from frappe import _

def tr_create_transaction(**kwargs):
    transaction_uid = kwargs.get("transaction_uid")
    transaction_owner = kwargs.get("transaction_owner")
    status = kwargs.get("status")
    project_uid = kwargs.get("project_uid")
    cost = kwargs.get("cost")
    company_fees = kwargs.get("company_fees")

    existing_transaction = frappe.db.exists("Transaction", {"transaction_uid": transaction_uid})
    if existing_transaction:
        frappe.throw(_("Transaction with this code already exists"))

    project = frappe.get_doc("Project", {"project_uid": project_uid})

    try:
        transaction = frappe.get_doc({
            "doctype": "Transaction",
            "transaction_uid": transaction_uid,
            "transaction_owner": transaction_owner,
            "status": status,
            "project": project.name,
            "cost": cost,
            "company_fees": company_fees
        })
        transaction.insert() 
        return transaction
    except Exception as e:
        frappe.throw(str(e))

def tr_update_transaction(transaction_uid, **kwargs):
    transaction = frappe.get_doc("Transaction", {"transaction_uid": transaction_uid})
    if not transaction:
        frappe.throw(_("Transaction not found"))

    for key, value in kwargs.items():
        setattr(transaction, key, value)
    
    transaction.save()
    return transaction

def tr_update_transaction_status(transaction_uid, status):
    transaction = frappe.get_doc("Transaction", {"transaction_uid": transaction_uid})
    if not transaction:
        frappe.throw(_("Transaction not found"))

    if not status in ["Accept", "Reject", "Pending"]:
        frappe.throw(_("Invalid status. Status must be one of 'Accept', 'Reject', 'Pending'"))

    transaction.status = status
    transaction.save()
    return transaction

def tr_update_cost_and_fees(transaction_uid, cost, company_fees):
    transaction = frappe.get_doc("Transaction", {"transaction_uid": transaction_uid})
    if not transaction:
        frappe.throw(_("Transaction not found"))
    
    transaction.cost = cost
    transaction.company_fees = company_fees
    transaction.save()
    return transaction

def tr_update_project(transaction_uid, project_uid):
    transaction = frappe.get_doc("Transaction", {"transaction_uid": transaction_uid})
    if not transaction:
        frappe.throw(_("Transaction not found"))
    
    project = frappe.get_doc("Project", {"project_uid": project_uid})
    if not project:
        frappe.throw(_("Project not found"))

    transaction.project = project.name
    transaction.save()
    return transaction

def tr_update_transaction_owner(transaction_uid, transaction_owner):
    transaction = frappe.get_doc("Transaction", {"transaction_uid": transaction_uid})
    if not transaction:
        frappe.throw(_("Transaction not found"))
    
    transaction.transaction_owner = transaction_owner
    transaction.save()
    return transaction

def tr_submit_transaction(transaction_uid):
    transaction = frappe.get_doc("Transaction", {"transaction_uid": transaction_uid})
    if not transaction:
        frappe.throw(_("Transaction not found"))

    if transaction.status != "Accept":
        frappe.throw(_("Only transactions with status 'Accept' can be submitted"))

    transaction.submit()
    return transaction

def tr_cancel_transaction(transaction_uid):
    transaction = frappe.get_doc("Transaction", {"transaction_uid": transaction_uid})
    if not transaction:
        frappe.throw(_("Transaction not found"))

    if not transaction.docstatus == 1:
        frappe.throw(_("Only submitted transactions can be cancelled"))

    transaction.cancel()
    return transaction