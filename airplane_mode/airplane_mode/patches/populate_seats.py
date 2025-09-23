# airplane_mode/patches/populate_seats.py
import frappe
import random

def execute():
    """Populate seats for existing Airplane Ticket records"""
    tickets = frappe.get_all("Airplane Ticket", filters={"seat": ["is", "not set"]}, pluck="name")
    
    for name in tickets:
        number = random.randint(1, 99)
        letter = random.choice(['A', 'B', 'C', 'D', 'E'])
        seat = f"{number}{letter}"
        
        frappe.db.set_value("Airplane Ticket", name, "seat", seat)
    
    frappe.db.commit()
