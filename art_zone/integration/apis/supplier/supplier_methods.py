import frappe
from frappe import _

def create_supplier(**kwargs):
    supplier_name = kwargs.get("supplier_name")
    supplier_uid = kwargs.get("supplier_uid")
    supplier_type = kwargs.get("supplier_type") or "Individual"

    if not supplier_name or not supplier_uid:
        frappe.throw(_("Supplier name and supplier UID are required."))

    existing_supplier = frappe.db.exists("Supplier", {"supplier_uid": supplier_uid})

    try:
        if existing_supplier:
            supplier = frappe.get_doc("Supplier", existing_supplier)
            supplier.supplier_name = supplier_name
            supplier.supplier_type = supplier_type
            supplier.save()
        else:
            supplier = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": supplier_name,
                "supplier_uid": supplier_uid,
                "supplier_type": supplier_type
            })
            supplier.insert() 

        frappe.db.commit() 
        return supplier

    except Exception as e:
        frappe.throw(_("An error occurred while processing the supplier: {0}").format(str(e)))


def toggle_supplier_status(**kwargs):
    supplier_name = kwargs.get("supplier_name")
    supplier_uid = kwargs.get("supplier_uid")

    try:
        supplier = frappe.get_doc("Supplier", supplier_name)
    except frappe.DoesNotExistError:
        frappe.throw(_("Supplier with Name '{0}' not found").format(supplier_name))

    # Toggle the "disabled" state
    try:
        # If the supplier is currently disabled (1), enable it (set disabled to 0), else disable it (set disabled to 1)
        supplier.disabled = 0 if supplier.disabled == 1 else 1
        supplier.save() 

        return {
            "supplier_name": supplier_name,
            "supplier_uid": supplier_uid,
            "disabled": supplier.disabled
        }
    except Exception as e:
        frappe.throw(_("An error occurred while updating the supplier status: {0}").format(str(e)))
