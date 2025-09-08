import frappe

# CREATE
@frappe.whitelist()
def create_balance_type(type_name):
    try:
        doc = frappe.get_doc({
            "doctype": "Balance Type",
            "type_name": type_name
        })
        doc.insert()
        frappe.db.commit()
        return {
            "status": "success",
            "message": "Balance Type created successfully",
            "data": doc.as_dict()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# GET BY ID
@frappe.whitelist()
def get_balance_type(name):
    try:
        doc = frappe.get_doc("Balance Type", name)
        return {
            "status": "success",
            "data": doc.as_dict()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# GET ALL
@frappe.whitelist()
def list_balance_types():
    try:
        docs = frappe.get_all("Balance Type", fields=["name", "type_name"])
        return {"status": "success", "data": docs}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# # UPDATE
# @frappe.whitelist()
# def update_balance_type(name, type_name):
#     try:
#         doc = frappe.get_doc("Balance Type", name)
#         if type_name:
#             doc.type_name = type_name
#         doc.save()
#         frappe.db.commit()
#         return {
#             "status": "success",
#             "message": "Balance Type updated successfully",
#             "data": doc.as_dict()
#         }
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# DELETE
@frappe.whitelist()
def delete_balance_type(name):
    try:
        frappe.delete_doc("Balance Type", name, )
        frappe.db.commit()
        return {
            "status": "success",
            "message": f"Balance Type '{name}' deleted successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
