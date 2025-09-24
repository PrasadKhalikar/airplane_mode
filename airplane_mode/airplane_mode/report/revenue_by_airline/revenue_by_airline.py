# Copyright (c) 2025, prasad and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "airline", "label": "Airline", "fieldtype": "Link", "options": "Airline", "width": 300},
        {"fieldname": "revenue", "label": "Revenue", "fieldtype": "Currency", "width": 150}
    ]

    data = []

    # Get all airlines
    airlines = frappe.get_all("Airline", fields=["name"])
    total_revenue = 0.0

    for airline in airlines:
        # Get all airplanes of this airline
        airplanes = frappe.get_all("Airplane", filters={"airline": airline.name}, fields=["name"])
        airplane_names = [a.name for a in airplanes]

        # Get all flights for those airplanes
        flights = frappe.get_all("Airplane Flight", filters={"airplane": ["in", airplane_names]}, fields=["name"])
        flight_names = [f.name for f in flights]

        # Sum ticket prices for submitted tickets of these flights
        if flight_names:
            revenue = frappe.get_all(
                "Airplane Ticket",
                filters={
                    "flight": ["in", flight_names],
                    "docstatus": 1
                },
                fields=["sum(flight_price) as revenue"]
            )[0].get("revenue") or 0
        else:
            revenue = 0

        total_revenue += revenue

        data.append({
            "airline": airline.name,
            "revenue": revenue
        })
	data.append(["Total Revenue", total_revenue])
	labels = [row[0] for row in data]  # Airline names
	values = [row[1] for row in data]  # Revenue values

	chart = {
		"data": {
			"labels": labels,
			"datasets": [
				{
					"name": "Revenue",
					"values": values
				}
			]
		},
		"type": "donut"
	}
    summary = [
		{'label': 'Total Revenue', 'value': frappe.format_value(total_revenue, 'Currency')}
	]

    return columns, data, None, chart, summary

