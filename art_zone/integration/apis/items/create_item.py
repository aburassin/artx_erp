import frappe
from frappe import _

def create_item(**kwargs):
    item_name = kwargs.get("item_name")
    item_code = kwargs.get("item_code")
    item_group = kwargs.get("item_group")

    # Check if the item already exists
    existing_item = frappe.db.exists("Item", {"item_code": item_code})
    if existing_item:
        frappe.throw(_("Item with this code already exists"))

    try:
        # Create a new item
        item = frappe.get_doc({
            "doctype": "Item",
            "item_name": item_name,
            "item_code": item_code,
            "item_group": item_group
        })
        item.insert() 
        return item
    except Exception as e:
        frappe.throw(str(e))


def update_item(**kwargs):
    item_code = kwargs.get("item_code")
    item_name = kwargs.get("item_name")
    item_group = kwargs.get("item_group")

    # Fetch the existing item based on item_code
    item = frappe.get_doc("Item", item_code)
    if not item:
        frappe.throw(_("Item not found"))

    try:
        # Update the item fields
        if item_name:
            item.item_name = item_name
        if item_group:
            item.item_group = item_group

        item.save()  # Save the updated item
        return item
    except Exception as e:
        frappe.throw(str(e))


import frappe
from frappe import _

def toggle_item_status(**kwargs):
    item_code = kwargs.get("item_code")

    try:
        item = frappe.get_doc("Item", item_code)
    except frappe.DoesNotExistError:
        frappe.throw(_("Item not found"))

    try:
        # If the item is currently disabled (1), enable it (set disabled to 0), else disable it (set disabled to 1)
        item.disabled = 0 if item.disabled == 1 else 1
        item.save()

        return {
            "item_code": item_code,
            "disabled": item.disabled
        }
    except Exception as e:
        frappe.throw(str(e))
