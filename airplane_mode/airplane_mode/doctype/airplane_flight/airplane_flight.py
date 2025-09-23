# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt


# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

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
        if not self.route and self.name and not self.name.startswith("new-"):
            self.route = f"airplane-flight/{self.name}"
    
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