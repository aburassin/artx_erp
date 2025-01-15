import frappe
from frappe import _

def create_customer(**kwargs):
    customer_name = kwargs.get("customer_name")
    customer_uid = kwargs.get("customer_uid")
    customer_type = kwargs.get("customer_type") or "Individual"

    if not customer_name or not customer_uid:
        frappe.throw(_("Customer name and customer UID are required."))

    existing_customer = frappe.db.exists("Customer", {"customer_uid": customer_uid})

    try:
        if existing_customer:
            customer = frappe.get_doc("Customer", existing_customer)
            customer.customer_name = customer_name
            customer.customer_type = customer_type
            customer.save()  
        else:
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": customer_name,
                "customer_uid": customer_uid,
                "customer_type": customer_type
            })
            customer.insert() 

        frappe.db.commit() 
        return customer

    except Exception as e:
        frappe.throw(_("An error occurred while processing the customer: {0}").format(str(e)))

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
