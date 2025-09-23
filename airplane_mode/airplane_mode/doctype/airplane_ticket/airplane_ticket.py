# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt
import frappe
import random
import string
from frappe.model.document import Document


class AirplaneTicket(Document):
    def before_insert(self):
        """Assign a random seat before inserting the ticket"""
        # Random seat number (1–99, adjust as you like)
        number = random.randint(1, 99)
        # Random letter A–E
        letter = random.choice(['A', 'B', 'C', 'D', 'E'])
        # Combine
        self.seat = f"{number}{letter}"
	def validate(self):
        
        seen = set()
        unique_addons = []
        for row in self.add_ons:
            if row.item not in seen:
                seen.add(row.item)
                unique_addons.append(row)
        self.add_ons = unique_addons
        addons_total = sum([row.amount for row in self.add_ons])
        self.total_amount = (self.flight_price or 0) + addons_total

    def before_submit(self):
            frappe.throw("You cannot submit this ticket unless the status is 'Boarded'")