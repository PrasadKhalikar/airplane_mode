# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt


import frappe

def execute(filters=None):
    data = []
    columns = [
        {"label": "Airport", "fieldname": "airport", "fieldtype": "Data", "width": 200},
        {"label": "Total Shops", "fieldname": "total_shops", "fieldtype": "Int", "width": 120},
        {"label": "Occupied", "fieldname": "occupied", "fieldtype": "Int", "width": 120},
        {"label": "Vacant", "fieldname": "vacant", "fieldtype": "Int", "width": 120},
    ]

    # Get list of airports that have shops
    airports = frappe.get_all("Airport Shop", fields=["airport"], group_by="airport")

    for a in airports:
        airport_name = a.airport
        shops = frappe.get_all("Airport Shop", filters={"airport": airport_name}, fields=["status"])
        total = len(shops)
        occupied = len([s for s in shops if s.status == "Occupied"])
        vacant = len([s for s in shops if s.status == "Vacant"])

        data.append({
            "airport": airport_name,
            "total_shops": total,
            "occupied": occupied,
            "vacant": vacant
        })

    return columns, data

