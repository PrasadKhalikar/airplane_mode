# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt

# import frappe
# -*- coding: utf-8 -*-
from frappe.model.document import Document

class FlightPassenger(Document):
    def before_save(self):
        # Combine first name and last name into full_name
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        elif self.first_name:
            self.full_name = self.first_name
        elif self.last_name:
            self.full_name = self.last_name
        else:
            self.full_name = ""

