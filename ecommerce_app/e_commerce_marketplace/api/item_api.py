import frappe
from frappe import _

# CREATE ITEM
@frappe.whitelist()
def create_item(item_name, balance_type, category, price, description=None, image=None):
    try:
        if not frappe.db.exists("Balance Type", balance_type):
            return {"status": "error", "message": f"Balance Type '{balance_type}' not found"}
        if not frappe.db.exists("Item Category", category):
            return {"status": "error", "message": f"Item Category '{category}' not found"}

        doc = frappe.get_doc({
            "doctype": "Item",
            "item_name": item_name,
            "description": description,
            "balance_type": balance_type,
            "category": category,
            "image": image,
            "price": price
        })
        doc.insert()
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Item created successfully",
            "data": doc.as_dict()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# GET ITEM BY ID
@frappe.whitelist()
def get_item(name):
    try:
        if not frappe.db.exists("Item", name):
            return {"status": "error", "message": f"Item with id '{name}' not found"}

        doc = frappe.get_doc("Item", name)

        return {
            "status": "success",
            "data": doc.as_dict()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# GET ITEMS BY ITEM NAME
@frappe.whitelist()
def get_items_by_name(item_name):
    try:
        items = frappe.get_all(
            "Item",
            filters={"item_name": item_name},
            fields=["name", "item_name", "description", "balance_type", "category", "image", "price"]
        )

        if not items:
            return {"status": "error", "message": f"No items found with name '{item_name}'"}

        return {
            "status": "success",
            "data": items
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# GET ALL ITEMS
@frappe.whitelist()
def get_all_items(category=None, page=1, limit=10):
    try:
        filters = {}
        if category:
            filters["category"] = category

        offset = (int(page) - 1) * int(limit)

        total_items = frappe.db.count("Item", filters=filters)

        items = frappe.get_all(
            "Item",
            filters=filters,
            fields=["name", "item_name", "description", "balance_type", "category", "image", "price"],
            limit_start=offset,
            limit_page_length=limit,
        )

        return {
            "status": "success",
            "page": int(page),
            "limit": int(limit),
            "total_items": total_items,
            "total_pages": (total_items + int(limit) - 1) // int(limit),
            "data": items,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# UPDATE ITEM
@frappe.whitelist()
def update_item(name, item_name=None, balance_type=None, category_name=None, image=None, price=None):
    try:
        if not frappe.db.exists("Item", name):
            return {"status": "error", "message": f"Item '{name}' not found"}

        doc = frappe.get_doc("Item", name)

        if item_name:
            doc.item_name = item_name

        if balance_type:
            if not frappe.db.exists("Balance Type", balance_type):
                return {"status": "error", "message": f"Balance Type '{balance_type}' not found"}
            doc.balance_type = balance_type

        if category_name:
            if not frappe.db.exists("Item Category", category_name):
                return {"status": "error", "message": f"Item Category '{category_name}' not found"}
            doc.category_name = category_name

        if image:
            doc.image = image

        if price is not None: 
            doc.price = price

        doc.save()
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Item updated successfully",
            "data": doc.as_dict()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# DELETE ITEM
@frappe.whitelist()
def delete_item(name):
    try:
        if not frappe.db.exists("Item", name):
            return {"status": "error", "message": f"Item '{name}' not found"}

        frappe.delete_doc("Item", name, )
        frappe.db.commit()

        return {
            "status": "success",
            "message": f"Item '{name}' deleted successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
