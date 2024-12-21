# Copyright (c) 2024, abdelwahab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now

class Transaction(Document):

	def before_save(self):
		if self.status == "Accept":
			self.update_project_status()
			self.create_purchase_order()

	def update_project_status(self):
		project = self.get_ref_project()
		project.status = "Completed"
		project.save()
	
	def create_purchase_order(self):
		ref_project = self.get_ref_project()
		if not ref_project or ref_project.project_owner_type != "Supplier":
			frappe.throw("Invalid project or owner type is not Supplier.")

		po = frappe.new_doc("Purchase Order")
		po.supplier = self.transaction_owner
		po.project = self.project
		po.schedule_date = now()
		for project_item in ref_project.items:
			po_item = po.append("items", {})
			po_item.item_code = project_item.item
			po_item.qty = project_item.quantity
			po_item.rate = project_item.price
			po_item.amount = project_item.quantity * project_item.price
			po_item.description = project_item.get("description", "No description provided")

		po.save()
		frappe.db.commit()
		
		return po

	def get_ref_project(self):
		return frappe.get_doc("Project", self.project)