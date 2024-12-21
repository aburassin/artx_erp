import frappe
from frappe import _

def create_customer(**kwargs):
    customer_name = kwargs.get("customer_name")
    customer_uid = kwargs.get("customer_uid")
    customer_type = kwargs.get("customer_type") or "Individual"

    # Validate that the required fields are provided
    if not customer_name or not customer_uid:
        frappe.throw(_("customer name and customer code are required"))

    # Check if the customer already exists based on customer_code
    existing_customer = frappe.db.exists("Customer", {"customer_name": customer_name})
    if existing_customer:
        frappe.throw(_("customer with Name '{0}' already exists").format(customer_name))

    try:
        # Create a new customer
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": customer_name,
            "customer_uid": customer_uid,
            "customer_type": customer_type
        })
        customer.insert()  
        return customer
    except Exception as e:
        frappe.throw(_("An error occurred while creating the customer: {0}").format(str(e)))


def toggle_customer_status(**kwargs):
    customer_name = kwargs.get("customer_name")
    customer_uid = kwargs.get("customer_uid")

    # Fetch the existing customer based on customer_uid
    try:
        customer = frappe.get_doc("Customer", customer_name)
    except frappe.DoesNotExistError:
        frappe.throw(_("customer with Name '{0}' not found").format(customer_name))

    # Toggle the "disabled" state
    try:
        # If the customer is currently disabled (1), enable it (set disabled to 0), else disable it (set disabled to 1)
        customer.disabled = 0 if customer.disabled == 1 else 1
        customer.save() 

        return {
            "customer_name": customer_name,
            "customer_uid": customer_uid,
            "disabled": customer.disabled
        }
    except Exception as e:
        frappe.throw(_("An error occurred while updating the customer status: {0}").format(str(e)))
