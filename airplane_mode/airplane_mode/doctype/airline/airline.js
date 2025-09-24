// Copyright (c) 2025, prasad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
    refresh(frm) {
        // remove old link if any
        frm.sidebar.clear_user_actions();

        if (frm.doc.website) {
            frm.sidebar.add_user_action("See on Website", () => {
                window.open(frm.doc.website, "_blank");
            });
        }
    }
});
