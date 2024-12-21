import frappe

def create_item_group(item_group_name):
    existing_item_group = frappe.db.exists("Item Group", {"item_group_name": item_group_name})
    if existing_item_group:
        frappe.throw(f"Item Group with the name '{item_group_name}' already exists.")

    try:
        item_group = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": item_group_name
        })
        item_group.insert() 
        return item_group
    except Exception as e:
        frappe.throw(str(e))



def bulk_create_item_groups(item_group_names):
    created_groups = []
    errors = []
    
    for item_group_name in item_group_names:
        # Check if the item group already exists
        existing_item_group = frappe.db.exists("Item Group", {"item_group_name": item_group_name})
        if existing_item_group:
            errors.append(f"Item Group '{item_group_name}' already exists.")
            continue 
        
        try:
            # Create a new Item Group
            item_group = frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": item_group_name
            })
            item_group.insert()  
            created_groups.append(item_group)
        except Exception as e:
            errors.append(f"Failed to create Item Group '{item_group_name}': {str(e)}")
    
    return {
        "created_groups": created_groups,
        "errors": errors
    }
