from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import frappe

def create_custom_fields_for_art_zone():
    custom_fields = {
        "Supplier": [
            {
                "fieldname": "supplier_uid",
                "fieldtype": "Data",
                "label": "Supplier UID",
                "insert_after": "supplier_name",
                "read_only": 1,
                "unique": 1
            }
        ],
        "Customer": [
            {
                "fieldname": "customer_uid",
                "fieldtype": "Data",
                "label": "Customer UID",
                "insert_after": "customer_name",
                "read_only": 1,
                "unique": 1
            }
        ],
        "Project": [
            {
                "fieldname": "project_uid",
                "fieldtype": "Data",
                "label": "Project UID",
                "insert_after": "project_name",
                "read_only": 0,
                "unique": 1
            },
            {
                "fieldname": "project_owner_type",
                "fieldtype": "Select",
                "label": "Project Owner Type",
                "insert_after": "project_uid",
                "options": "Supplier\nCustomer",
                "read_only": 0
            },
            {
                "fieldname": "completed_date",
                "fieldtype": "Date",
                "label": "Completed Date",
                "insert_after": "expected_end_date",
                "read_only": 0
            },
            {
                "fieldname": "project_owner_c",
                "fieldtype": "Link",
                "label": "Project Owner (Customer)",
                "insert_after": "project_owner_type",
                "options": "Customer",
                "depends_on": "eval:doc.project_owner_type == 'Customer'"
            },
            {
                "fieldname": "project_owner_s",
                "fieldtype": "Link",
                "label": "Project Owner (Supplier)",
                "insert_after": "project_owner_c",
                "options": "Supplier",
                "depends_on": "eval:doc.project_owner_type == 'Supplier'"
            },
            {
				"fieldname": "accepted_transaction",
				"fieldtype": "Link",
				"label": "Accepted Transaction",
				"insert_after": "department",
				"options": "Transaction",
				"read_only": 1
			},
            {
                "fieldname": "items_tab",
                "fieldtype": "Tab Break",
                "label": "Items",
                "insert_after": "message",
            },
            {
                "fieldname": "items",
                "fieldtype": "Table",
                "label": "Items",
                "options": "Project Item",
                "insert_after": "items_tab",
            }
        ]
    }

    create_custom_fields(custom_fields)

    frappe.db.commit()

    print("Custom Fields for Supplier and Project created successfully.")
