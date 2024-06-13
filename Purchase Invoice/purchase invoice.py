from frappe import _

def before_insert(doc, method):
    if not doc.invoice_items:
        frappe.throw(_("Please add items to the invoice."))

def validate(doc, method):
    for item in doc.invoice_items:
        item.total_amount = item.quantity * item.rate
    doc.total_amount = sum([item.total_amount for item in doc.invoice_items])

doctype_js = """
frappe.ui.form.on('Purchase Invoice', {
    onload: function(frm) {
        frm.set_query('supplier', function() {
            return {
                filters: {
                    'is_supplier': 1
                }
            };
        });
        frm.set_query('item_code', 'invoice_items', function() {
            return {
                filters: {
                    'is_sales_item': 1
                }
            };
        });
        frm.set_query('purchasing_agent', function() {
            return {
                filters: {
                    'designation': 'Purchasing Agent'
                }
            };
        });
    },
    status: function(frm) {
        if (frm.doc.status === 'Draft') {
            frm.set_df_property('purchasing_agent', 'hidden', 1);
        } else {
            frm.set_df_property('purchasing_agent', 'hidden', 0);
        }
    },
    invoice_items_add: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, 'total_amount', row.quantity * row.rate);
    },
    invoice_items_remove: function(frm) {
        update_total_amount(frm);
    },
    refresh: function(frm) {
        update_total_amount(frm);
        set_status_color(frm);
    }
});

function update_total_amount(frm) {
    var total = 0;
    frm.doc.invoice_items.forEach(function(row) {
        total += row.total_amount;
    });
    frm.set_value('total_amount', total);
}

function set_status_color(frm) {
    if (frm.doc.status === 'Draft') {
        frm.page.wrapper.style.backgroundColor = '#FFF3CD';
    } else if (frm.doc.status === 'Submitted') {
        frm.page.wrapper.style.backgroundColor = '#D1ECF1';
    } else if (frm.doc.status === 'Paid') {
        frm.page.wrapper.style.backgroundColor = '#D4EDDA';
    }
}
"""


