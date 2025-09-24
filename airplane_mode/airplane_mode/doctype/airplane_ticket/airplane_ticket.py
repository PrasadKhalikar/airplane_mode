# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt
# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt
import frappe
import random
from frappe.model.document import Document


class AirplaneTicket(Document):
    def before_insert(self):
        """Assign a random seat before inserting the ticket"""
        number = random.randint(1, 99)
        letter = random.choice(["A", "B", "C", "D", "E"])
        self.seat = f"{number}{letter}"

        # --- Capacity Check ---
        if self.flight:
            flight = frappe.get_doc("Airplane Flight", self.flight)
            airplane = frappe.get_doc("Airplane", flight.airplane)

            # Count tickets already booked for this flight
            booked_count = frappe.db.count(
                "Airplane Ticket",
                filters={"flight": self.flight}
            )

            if booked_count >= (airplane.capacity or 0):
                frappe.throw(
                    f"Cannot book ticket: Flight {flight.name} is already full "
                    f"(Capacity: {airplane.capacity})"
                )

    def validate(self):
        """Ensure add-ons are unique and calculate total amount"""
        seen = set()
        unique_addons = []
        for row in self.add_ons:
            if row.item not in seen:
                seen.add(row.item)
                unique_addons.append(row)
        self.add_ons = unique_addons

        addons_total = sum([row.price for row in self.add_ons])
        self.total_amount = (self.flight_price or 0) + addons_total

    def before_submit(self):
        """Prevent submission unless status is Boarded"""
        if self.status != "Boarded":
            frappe.throw("You cannot submit this ticket unless the status is 'Boarded'")
