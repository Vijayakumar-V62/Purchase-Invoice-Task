import frappe

def setup_workflow():
    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": "Purchase Invoice Workflow",
        "document_type": "Purchase Invoice",
        "is_active": 1,
        "states": [
            {"state": "Draft", "doc_status": 0, "allow_edit": "Procurement Manager"},
            {"state": "Pending Approval", "doc_status": 0, "allow_edit": "Procurement Manager"},
            {"state": "Approved", "doc_status": 1, "allow_edit": "Procurement Manager"},
            {"state": "Paid", "doc_status": 1, "allow_edit": "Procurement Manager"},
        ],
        "transitions": [
            {"state": "Draft", "action": "Submit", "next_state": "Pending Approval", "allow": "Procurement Manager"},
            {"state": "Pending Approval", "action": "Approve", "next_state": "Approved", "allow": "Procurement Manager"},
            {"state": "Approved", "action": "Pay", "next_state": "Paid", "allow": "Procurement Manager"},
        ],
        "permissions": [
            {"role": "Procurement Manager", "state": "Pending Approval"},
            {"role": "Procurement Manager", "state": "Approved"},
        ],
    })
    workflow.insert(ignore_permissions=True)

setup_workflow()


