import frappe

# CREATE
@frappe.whitelist()
def create_item_category(category_name, description=None):
    try:
        doc = frappe.get_doc({
            "doctype": "Item Category",
            "category_name": category_name,
            "description": description
        })
        doc.insert()
        frappe.db.commit()
        return {
            "status": "success",
            "message": "Item Category created successfully",
            "data": doc.as_dict()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# GET BY ID
@frappe.whitelist()
def get_item_category(name):
    try:
        doc = frappe.get_doc("Item Category", name)
        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# GET ALL
@frappe.whitelist()
def list_item_categories():
    try:
        docs = frappe.get_all("Item Category", fields=["name", "category_name", "description"])
        return {"status": "success", "data": docs}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# # UPDATE
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
#             "data": doc.as_dict()
#         }
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# DELETE
@frappe.whitelist()
def delete_item_category(name):
    try:
        frappe.delete_doc("Item Category", name, )
        frappe.db.commit()
        return {
            "status": "success",
            "message": f"Item Category '{name}' deleted successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
