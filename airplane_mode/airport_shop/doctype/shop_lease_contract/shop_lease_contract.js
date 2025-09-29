// Copyright (c) 2025, prasad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Lease Contract", {
    refresh(frm) {
        if (frm.is_new() && !frm.doc.rent_amount) {
            frappe.db.get_single_value("Airport Shop Settings", "default_rent_amount")
                .then(rent => {
                    if (rent) {
                        frm.set_value("rent_amount", rent);
                    }
                });
        }
    }
});
