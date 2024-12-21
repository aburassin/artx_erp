

import frappe 

def create_new_project(**kwargs):
    data = kwargs
    project = frappe.get_doc({
        "doctype": "Project",
        "project_name": data.get("project_name"),
        "project_uid": data.get("project_uid"),
        "project_owner_type": data.get("project_owner_type"),
        "status": data.get("status"),
        "is_active": data.get("is_active"),
        "expected_start_date": data.get("expected_start_date"),
        "expected_end_date": data.get("expected_end_date"),
        "notes": data.get("notes"),
    })
    if data.get("project_owner_type") == "Customer":
        project.project_owner_c = data.get("project_owner_c")
    elif data.get("project_owner_type") == "Supplier":
        project.project_owner_s = data.get("project_owner_s")
    
    project.insert()
    return project