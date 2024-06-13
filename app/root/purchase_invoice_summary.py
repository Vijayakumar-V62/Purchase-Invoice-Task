import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Invoice No"), "fieldname": "name", "fieldtype": "Link", "options": "Purchase Invoice", "width": 150},
        {"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": _("Supplier"), "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 150},
        {"label": _("Total Amount"), "fieldname": "total_amount", "fieldtype": "Currency", "width": 100}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND posting_date <= %(to_date)s"

    data = frappe.db.sql(f"""
        SELECT
            name, posting_date, supplier, total_amount
        FROM
            `tabPurchase Invoice`
        WHERE
            docstatus = 1 {conditions}
        ORDER BY
            posting_date desc
    """, filters, as_dict=1)

    return data


