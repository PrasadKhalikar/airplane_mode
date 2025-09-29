import frappe

def send_rent_reminders():
    settings = frappe.get_single("Airport Shop Settings")
    
    if not settings.enable_rent_reminders:
        print("Rent reminders are disabled in settings.")
        return

    contracts = frappe.get_all(
        "Shop Lease Contract",
        filters={"status": "Active"},
        fields=["name", "tenant", "shop", "rent_amount"]
    )

    for contract in contracts:
        tenant_email = frappe.get_value("Shop Tenant", contract["tenant"], "email")
        if tenant_email:
            # Use default rent if rent_amount is empty
            rent_amount = contract['rent_amount'] or settings.default_rent_amount

            message = f"""
            Dear {contract['tenant']},

            This is a friendly reminder that your rent of ₹{rent_amount} 
            for shop {contract['shop']} is due this month.

            Please make the payment on time.

            Regards,
            Airport Management
            """
            frappe.sendmail(
                recipients=tenant_email,
                subject="Monthly Rent Reminder",
                message=message
            )

    frappe.db.commit()
