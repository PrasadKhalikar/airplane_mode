# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ShopLeaseContract(Document):
    def on_update(self):
        if self.shop:
            if self.status == "Active":
                frappe.db.set_value("Airport Shop", self.shop, {
                    "status": "Occupied",
                    "current_contract": self.name
                })
            else:
                frappe.db.set_value("Airport Shop", self.shop, {
                    "status": "Vacant",
                    "current_contract": None
                })
