// Dynamic UI Interaction
frappe.ui.form.on('Purchase Invoice', {
    refresh: function(frm) {
        set_status_color(frm);
    },
    status: function(frm) {
        set_status_color(frm);
    }
});

function set_status_color(frm) {
    if (frm.doc.status === 'Draft') {
        frm.page.wrapper.style.backgroundColor = '#FFF3CD';
    } else if (frm.doc.status === 'Submitted') {
        frm.page.wrapper.style.backgroundColor = '#D1ECF1';
    } else if (frm.doc.status === 'Paid') {
        frm.page.wrapper.style.backgroundColor = '#D4EDDA';
    }
}

//Conditional Field Visibility
frappe.ui.form.on('Purchase Invoice', {
    status: function(frm) {
        if (frm.doc.status === 'Draft') {
            frm.set_df_property('purchasing_agent', 'hidden', 1);
        } else {
            frm.set_df_property('purchasing_agent', 'hidden', 0);
        }
    }
});

//Real-time Total Calculation
frappe.ui.form.on('Purchase Invoice', {
    invoice_items_add: function(frm, cdt, cdn) {
        calculate_total_amount(frm);
    },
    invoice_items_remove: function(frm) {
        calculate_total_amount(frm);
    },
    invoice_items: function(frm) {
        calculate_total_amount(frm);
    }
});

function calculate_total_amount(frm) {
    var total = 0;
    frm.doc.invoice_items.forEach(function(row) {
        total += row.quantity * row.rate;
    });
    frm.set_value('total_amount', total);
}

// Interactive Invoice Status Change
frappe.ui.form.on('Purchase Invoice', {
    before_save: function(frm) {
        if (frm.doc.status_changed) {
            frappe.confirm('Are you sure you want to change the status?', function() {
                frm.doc.status_changed = false;
                frm.save();
            }, function() {
                frappe.msgprint('Status change canceled');
                frm.doc.status = frm.doc._original_status;
            });
            return false;
        }
        frm.doc._original_status = frm.doc.status;
    },
    status: function(frm) {
        frm.doc.status_changed = true;
    }
});

// Data Validation on Save
frappe.ui.form.on('Purchase Invoice', {
    before_save: function(frm) {
        if (frm.doc.invoice_date > frappe.datetime.nowdate()) {
            frappe.msgprint(__('Invoice date cannot be in the future'));
            frappe.validated = false;
        }
    }
});


