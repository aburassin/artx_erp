import frappe
from frappe.model.document import Document
from frappe.utils import now

class Transaction(Document):

    def on_submit(self):
        self.set_transaction_complete_date()
        if self.status == "Accept":
            self.process_acceptance()

    def on_cancel(self):
        if self.status == "Accept":
            self.reverse_acceptance()

    def set_transaction_complete_date(self):
        self.transaction_complete_date = now()

    def process_acceptance(self):
        self.update_project_status()
        self.create_purchase_invoice()
        self.create_sales_invoice()

    def reverse_acceptance(self):
        self.reverse_project_status()
        self.delete_purchase_invoice()
        self.delete_sales_invoice()

    def update_project_status(self):
        project = self.get_ref_project()
        if not project:
            frappe.throw("Referenced project not found.")
        project.estimated_costing = self.cost + self.company_fees
        project.status = "Completed"
        project.accepted_transaction = self.name
        self.add_transaction_row_in_project(project)
        project.save()

    def reverse_project_status(self):
        project = self.get_ref_project()
        if not project:
            frappe.throw("Referenced project not found.")
        project.estimated_costing = 0.0
        project.status = "Open"
        self.remove_transaction_row_from_project(project)
        project.save()

    def add_transaction_row_in_project(self, project):
        project.append("accepted_transaction_table", {
            "transaction": self.name,
            "cost": self.cost,
            "transaction_owner": self.transaction_owner
        })

    def remove_transaction_row_from_project(self, project):
        for row in project.accepted_transaction_table:
            if row.transaction == self.name:
                project.remove(row)
                break

    def create_purchase_invoice(self):
        ref_project = self.get_ref_project()
        if not ref_project or ref_project.project_owner_type != "Customer":
            frappe.throw("Invalid project or owner type is not Customer.")

        pi = frappe.new_doc("Purchase Invoice")
        pi.supplier = self.transaction_owner
        pi.project = self.project
        pi.posting_date = now()

        for project_item in ref_project.items:
            pi_item = pi.append("items", {})
            pi_item.item_code = project_item.item
            pi_item.qty =  1
            pi_item.rate = self.cost
            pi_item.amount = self.cost
            pi_item.description = project_item.get("description", f"Transaction: {self.name}")

        pi.save()
        frappe.db.commit()

        self.purchase_invoice = pi.name
        return pi

    def delete_purchase_invoice(self):
        if self.purchase_invoice:
            pi = frappe.get_doc("Purchase Invoice", self.purchase_invoice)
            if pi:
                pi.cancel()
                pi.delete()
                frappe.db.commit()

    def create_sales_invoice(self):
        ref_project = self.get_ref_project()
        if not ref_project or ref_project.project_owner_type != "Customer":
            frappe.throw("Invalid project or owner type is not Customer.")

        si = frappe.new_doc("Sales Invoice")
        si.customer = ref_project.project_owner_c
        si.project = self.project
        si.posting_date = now()

        for project_item in ref_project.items:
            si_item = si.append("items", {})
            si_item.item_code = project_item.item
            si_item.qty = 1
            si_item.rate = self.cost + self.company_fees
            si_item.amount = si_item.rate
            si_item.description = project_item.get("description", " ")

        default_tax_template = frappe.get_value("Sales Taxes and Charges Template", {"is_default": 1}, "name")
        if default_tax_template:
            si.taxes_and_charges = default_tax_template

            tax_template = frappe.get_doc("Sales Taxes and Charges Template", default_tax_template)
            for tax in tax_template.taxes:
                si_tax = si.append("taxes", {})
                si_tax.charge_type = tax.charge_type
                si_tax.account_head = tax.account_head
                si_tax.description = tax.description
                si_tax.rate = tax.rate
                si_tax.tax_amount = tax.tax_amount
                si_tax.base_tax_amount = tax.base_tax_amount

        si.save()
        frappe.db.commit()

        self.sales_invoice = si.name
        return si


    def delete_sales_invoice(self):
        if self.sales_invoice:
            si = frappe.get_doc("Sales Invoice", self.sales_invoice)
            if si:
                si.cancel()
                si.delete()
                frappe.db.commit()

    def get_ref_project(self):
        project = frappe.get_doc("Project", self.project)
        if not project:
            frappe.throw("Referenced project not found.")
        return project