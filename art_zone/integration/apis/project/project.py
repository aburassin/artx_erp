import frappe

def create_new_project(**kwargs):
    """
    Create a new project with given data.
    """
    data = kwargs
    items = data.get("items", [])

    project = frappe.get_doc({
        "doctype": "Project",
        "project_name": data.get("project_name"),
        "project_uid": data.get("project_uid"),
        "project_owner_type": data.get("project_owner_type", "Customer"),
        "status": data.get("status", "Open"),
        # "is_active": data.get("is_active") or "Yes",
        "notes": data.get("notes", ""),
    })

    if data.get("project_owner_type") == "Customer":
        project.project_owner_c = data.get("project_owner_c")
    elif data.get("project_owner_type") == "Supplier":
        project.project_owner_s = data.get("project_owner_s")

    for item in items:
        project_item = project.append("items", {})
        project_item.item = item.get("item")
        project_item.qty = item.get("qty")
        project_item.price = item.get("price")

    project.estimated_costing = sum([item.qty * item.price for item in project.items])
    project.insert()
    return project

def update_old_project(**kwargs):
    """
    Update an existing project's status and other details.
    """
    data = kwargs
    project = frappe.get_doc("Project", data.get("name"))
    if "status" in data:
        project.status = data.get("status")
    if "notes" in data:
        project.notes = data.get("notes")
    project.save()
    return project

def update_old_project_items(project_name, items):
    """
    Update items in an existing project.
    """
    project = frappe.get_doc("Project", project_name)
    project.items = []

    for item in items:
        project_item = project.append("items", {})
        project_item.item = item.get("item")
        project_item.qty = item.get("qty")
        project_item.price = item.get("price")

    project.estimated_costing = sum([item.qty * item.price for item in project.items])
    project.save()
    return project

def toggle_old_project_status(project_name, is_active):
    """
    Toggle the active status of a project.
    """
    project = frappe.get_doc("Project", project_name)
    project.is_active = 1 if is_active else 0
    project.save()
    return project
