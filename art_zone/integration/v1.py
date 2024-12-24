
import frappe
from frappe import _
from .apis.items.create_item_group import create_item_group
from .apis.auth.get_token import get_user_token
from .apis.items.create_item import (
    create_item,
    update_item,
    toggle_item_status
)
from .apis.supplier.supplier_methods import (create_supplier, toggle_supplier_status)
from .apis.customer.customer_methods import (create_customer , toggle_customer_status)
from .apis.project.project import (
    create_new_project,update_old_project,update_old_project_items,toggle_old_project_status)
from .apis.project.transaction import (
    tr_create_transaction,
    tr_update_transaction,
    tr_update_transaction_owner,
    tr_update_cost_and_fees,
    tr_update_transaction_status,
    tr_submit_transaction,
    tr_cancel_transaction,
    tr_update_project)

@frappe.whitelist(allow_guest=True , methods=["POST"])
def login(user , password):
    get_user_token (user , password)

@frappe.whitelist(methods=["POST"])
def create_category(item_group):
    if not item_group:
        return frappe.throw(_("Item Group is required"))
    
    return create_item_group(item_group)


@frappe.whitelist(methods=["POST"])
def create_service(**kwargs):
    return create_item(**kwargs)

@frappe.whitelist(methods=["PUT"])
def update_service(**kwargs):
    return update_item(**kwargs)

@frappe.whitelist(methods=["PUT"])
def toggle_service_status(**kwargs):
    return toggle_item_status(**kwargs)

@frappe.whitelist(methods=["POST"])
def create_service_provider(**kwargs):
    return create_supplier(**kwargs)

@frappe.whitelist(methods=["PUT"])
def toggle_service_provider_status(**kwargs):
    return toggle_supplier_status(**kwargs)

@frappe.whitelist(methods=["POST"])
def create_client(**kwargs):
    return create_customer(**kwargs)

@frappe.whitelist(methods=["PUT"])
def toggle_client_status(**kwargs):
    return toggle_customer_status(**kwargs)

@frappe.whitelist(methods=["POST"])
def create_project(**kwargs):
    return create_new_project(**kwargs)

@frappe.whitelist(methods=["PUT"])
def update_project(**kwargs):
    return update_old_project(**kwargs)

@frappe.whitelist(methods=["PUT"]) 
def update_project_items(**kwargs):
    project_uid = kwargs.get("project_uid")
    items = kwargs.get("items")
    return update_old_project_items(project_uid, items)

@frappe.whitelist(methods=["PUT"])
def toggle_project_status(**kwargs):
    project_name = kwargs.get("project_uid")
    is_active = kwargs.get("is_active")
    return toggle_old_project_status(project_name, is_active)

@frappe.whitelist(methods=["POST"])
def create_transaction(**kwargs):
    return tr_create_transaction(**kwargs)

@frappe.whitelist(methods=["PUT"])
def update_transaction(**kwargs):
    return tr_update_transaction(**kwargs)

@frappe.whitelist(methods=["PUT"])
def update_transaction_owner(**kwargs):
    return tr_update_transaction_owner(**kwargs)

@frappe.whitelist(methods=["PUT"])  
def update_cost_and_fees(**kwargs):
    return tr_update_cost_and_fees(**kwargs)

@frappe.whitelist(methods=["PUT"])  
def update_transaction_status(**kwargs):
    return tr_update_transaction_status(**kwargs)

@frappe.whitelist(methods=["PUT"])
def submit_transaction(**kwargs):
    return tr_submit_transaction(**kwargs)

@frappe.whitelist(methods=["PUT"])
def cancel_transaction(**kwargs):
    return tr_cancel_transaction(**kwargs)

@frappe.whitelist(methods=["PUT"])
def update_project(**kwargs):
    return tr_update_project(**kwargs)

