// Copyright (c) 2025, prasad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button("Assign Seat", () => {
                let d = new frappe.ui.Dialog({
                    title: "Assign Seat",
                    fields: [
                        {
                            label: "Seat Number",
                            fieldname: "seat_number",
                            fieldtype: "Data",
                            reqd: 1
                        }
                    ],
                    primary_action_label: "Assign",
                    primary_action(values) {
                        frm.set_value("seat", values.seat_number);
                        frm.save();
                        d.hide();
                    }
                });
                d.show();
            }, "Actions"); 
        }
    }
});
