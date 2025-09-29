# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt


# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils.background_jobs import enqueue

class AirplaneFlight(WebsiteGenerator):
    def on_submit(self):
        """Mark flight as Completed once submitted"""
        self.status = "Completed"
    
    def before_insert(self):
        if not self.route:
            pass
    
    def after_insert(self):
        if not self.route:
            self.db_set("route", f"airplane-flight/{self.name}")
    
    def before_save(self):
        """Generate route if missing and trigger ticket updates if gate changes"""
        # --- Keep existing route logic ---
        if not self.route and self.name and not self.name.startswith("new-"):
            self.route = f"airplane-flight/{self.name}"

        # --- New: detect gate change ---
        old_doc = self.get_doc_before_save()
        if old_doc and old_doc.gate != self.gate:
            # Enqueue background job to update all tickets linked to this flight
            enqueue(
                "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_ticket_gates",
                flight_name=self.name,
                new_gate=self.gate
            )
    
    def get_context(self, context):
        """Add additional context for web view"""
        context.no_cache = 1
        
        # Get airplane details to fetch airline
        if self.airplane:
            airplane_doc = frappe.get_doc("Airplane", self.airplane)
            context.airline = airplane_doc.airline if hasattr(airplane_doc, 'airline') else ""
        
        # Format duration and date for better display
        if self.duration:
            context.formatted_duration = frappe.utils.format_duration(self.duration)
        
        if self.date_of_departure:
            context.formatted_date = frappe.utils.format_date(self.date_of_departure, "d MMMM, YYYY")
        
        return context


# ----------------------------
# Background job function
# ----------------------------
def update_ticket_gates(flight_name, new_gate):
    """
    Background job to update all tickets linked to a flight
    when the flight's gate changes.
    """
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"flight": flight_name},
        fields=["name"]
    )
    
    for ticket in tickets:
        frappe.db.set_value("Airplane Ticket", ticket.name, "gate", new_gate)
    
    frappe.db.commit()
