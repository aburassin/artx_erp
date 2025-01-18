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
        purchase_invoice = self.create_purchase_invoice()
        sales_invoice = self.create_sales_invoice()
        
        # Create Payment Entries
        self.create_payment_entry_for_purchase_invoice(purchase_invoice)
        self.create_payment_entry_for_sales_invoice(sales_invoice)

    def reverse_acceptance(self):
        self.reverse_project_status()
        self.reverse_payment_entries()
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
        pi.submit()
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
        si.submit()
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

    def create_payment_entry_for_purchase_invoice(self, purchase_invoice):
        payment_entry = frappe.new_doc("Payment Entry")
        payment_entry.payment_type = "Pay"
        payment_entry.party_type = "Supplier"
        payment_entry.party = purchase_invoice.supplier
        
        payment_entry.paid_from = self.get_company_default_account("default_bank_account")
        payment_entry.paid_to = self.get_company_default_account("default_payable_account")
        
        payment_entry.paid_amount = purchase_invoice.grand_total
        payment_entry.received_amount = purchase_invoice.grand_total
        payment_entry.reference_no = purchase_invoice.name
        payment_entry.reference_date = now()
        
        payment_entry.append("references", {
            "reference_doctype": "Purchase Invoice",
            "reference_name": purchase_invoice.name,
            "total_amount": purchase_invoice.grand_total,
            "outstanding_amount": purchase_invoice.grand_total,
            "allocated_amount": purchase_invoice.grand_total
        })
        
        payment_entry.save()
        frappe.db.commit()
        payment_entry.submit()
        self.purchase_payment_entry = payment_entry.name
        return payment_entry
    def create_payment_entry_for_sales_invoice(self, sales_invoice):
        payment_entry = frappe.new_doc("Payment Entry")
        payment_entry.payment_type = "Receive"
        payment_entry.party_type = "Customer"
        payment_entry.party = sales_invoice.customer
        payment_entry.paid_from = self.get_company_default_account("default_receivable_account")
        payment_entry.paid_to = self.get_company_default_account("default_bank_account")
        payment_entry.paid_amount = sales_invoice.grand_total
        payment_entry.received_amount = sales_invoice.grand_total
        payment_entry.reference_no = sales_invoice.name
        payment_entry.reference_date = now()
        payment_entry.append("references", {
            "reference_doctype": "Sales Invoice",
            "reference_name": sales_invoice.name,
            "total_amount": sales_invoice.grand_total,
            "outstanding_amount": sales_invoice.grand_total,
            "allocated_amount": sales_invoice.grand_total
        })
        payment_entry.save()
        frappe.db.commit()
        payment_entry.submit()
        self.sales_payment_entry = payment_entry.name
        return payment_entry

    def get_company_default_account(self, account_type):
        project = self.get_ref_project()
        if not project:
            frappe.throw("Referenced project not found.")
        
        company = project.company
        if not company:
            frappe.throw(f"Company not set for project {project.name}.")

        account = frappe.get_value("Company", company, account_type)
        if not account:
            frappe.throw(f"Default {account_type} account not set for company {company}.")
        return account
    
    def reverse_payment_entries(self):
        if self.purchase_payment_entry:
            purchase_payment_entry = frappe.get_doc("Payment Entry", self.purchase_payment_entry)
            if purchase_payment_entry.docstatus == 1:
                purchase_payment_entry.cancel()
            purchase_payment_entry.delete()
            frappe.db.commit()
            self.purchase_payment_entry = None 

        if self.sales_payment_entry:
            sales_payment_entry = frappe.get_doc("Payment Entry", self.sales_payment_entry)
            if sales_payment_entry.docstatus == 1:
                sales_payment_entry.cancel()
            sales_payment_entry.delete()
            frappe.db.commit()
            self.sales_payment_entry = None 
