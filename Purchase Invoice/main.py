# Data Retrieval
import frappe

def get_purchase_invoices():
    invoices = frappe.get_all('Purchase Invoice', fields=['name', 'posting_date', 'total_amount'])
    for invoice in invoices:
        print(f"Invoice: {invoice.name}, Date: {invoice.posting_date}, Total: {invoice.total_amount}")

get_purchase_invoices()

# Filtering and Sorting
def get_filtered_sorted_invoices(supplier):
    invoices = frappe.get_all('Purchase Invoice', filters={'supplier': supplier}, fields=['name', 'posting_date', 'total_amount'], order_by='posting_date asc')
    for invoice in invoices:
        print(f"Invoice: {invoice.name}, Date: {invoice.posting_date}, Total: {invoice.total_amount}")

get_filtered_sorted_invoices('Supplier Name')

# Data Aggregation
def calculate_total_expenditure():
    invoices = frappe.get_all('Purchase Invoice', fields=['total_amount'])
    total_expenditure = sum([invoice.total_amount for invoice in invoices])
    print(f"Total Expenditure: {total_expenditure}")

calculate_total_expenditure()

# Dynamic Query with Parameters
def get_invoices_within_date_range(start_date, end_date):
    invoices = frappe.get_all('Purchase Invoice', filters={'posting_date': ['between', [start_date, end_date]]}, fields=['name', 'posting_date', 'total_amount'])
    for invoice in invoices:
        print(f"Invoice: {invoice.name}, Date: {invoice.posting_date}, Total: {invoice.total_amount}")

get_invoices_within_date_range('2023-01-01', '2023-12-31')

# Complex Data Processing
def get_top_purchasing_agent():
    invoices = frappe.get_all('Purchase Invoice', fields=['purchasing_agent', 'total_amount'])
    agent_totals = {}
    for invoice in invoices:
        agent_totals[invoice.purchasing_agent] = agent_totals.get(invoice.purchasing_agent, 0) + invoice.total_amount
    top_agent = max(agent_totals, key=agent_totals.get)
    print(f"Top Purchasing Agent: {top_agent}, Total Purchases: {agent_totals[top_agent]}")

get_top_purchasing_agent()


