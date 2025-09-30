# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt

# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirportShop(WebsiteGenerator):
    # WebsiteGenerator already gives you route/title handling

    def autoname(self):
        # keep doc.name = shop_name (or you can use shop_number instead)
        self.name = self.shop_name

    def before_insert(self):
        # set route automatically if not set
        if not self.route:
            # frappe.scrub makes "Coffee Corner" -> "coffee-corner"
            self.route = f"shops/{frappe.scrub(self.shop_name)}"

    def get_context(self, context):
        # extra data for rendering in shop.html
        context.title = self.shop_name
        return context
