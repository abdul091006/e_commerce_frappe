import frappe

def sanitize_doc(doc_dict):
    exclude_fields = ["owner", "creation", "modified", "modified_by", "docstatus", "idx", "doctype"]
    return {k: v for k, v in doc_dict.items() if k not in exclude_fields}

# CREATE
@frappe.whitelist()
def create_item_category(category_name):
    try:
        doc = frappe.get_doc({
            "doctype": "Item Category",
            "category_name": category_name
        })
        doc.insert()
        frappe.db.commit()
        return {
            "status": "success",
            "message": "Item Category created successfully",
            "data": sanitize_doc(doc.as_dict())
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# GET BY ID
@frappe.whitelist()
def get_item_category(name):
    try:
        doc = frappe.get_doc("Item Category", name)
        return {
            "status": "success",
            "data": sanitize_doc(doc.as_dict())
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# GET ALL
@frappe.whitelist()
def list_item_categories():
    try:
        docs = frappe.get_all("Item Category", fields=["name", "category_name"])
        return {"status": "success", "data": docs}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# UPDATE (optional kalau mau dipakai)
# @frappe.whitelist()
# def update_item_category(name, category_name=None, description=None):
#     try:
#         doc = frappe.get_doc("Item Category", name)
#         if category_name:
#             doc.category_name = category_name
#         if description is not None:
#             doc.description = description
#         doc.save()
#         frappe.db.commit()
#         return {
#             "status": "success",
#             "message": "Item Category updated successfully",
#             "data": sanitize_doc(doc.as_dict())
#         }
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# DELETE
@frappe.whitelist()
def delete_item_category(name):
    try:
        frappe.delete_doc("Item Category", name)
        frappe.db.commit()
        return {
            "status": "success",
            "message": f"Item Category '{name}' deleted successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
