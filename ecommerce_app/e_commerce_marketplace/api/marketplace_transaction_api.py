import frappe

# GET ALL PURCHASED ITEMS WITH PAGINATION
@frappe.whitelist()
def get_purchased_items(page=1, limit=10):
    try:
        current_user = frappe.session.user
        if current_user == "Guest":
            frappe.throw("Must be logged in")

        page = max(int(page), 1)
        limit = max(int(limit), 1)
        offset = (page - 1) * limit

        filters = {
            "user": current_user,
            "status": "Success"
        }

        # total semua transaksi sukses user
        total_purchases = frappe.db.count("Marketplace Transaction", filters=filters)

        transactions = frappe.get_all(
            "Marketplace Transaction",
            filters=filters,
            fields=["name", "item", "amount", "balance_type", "status", "creation"],
            order_by="creation desc",
            limit_start=offset,
            limit_page_length=limit,
        )

        for tx in transactions:
            if "creation" in tx:
                tx["creation"] = str(tx["creation"])

        total_pages = (total_purchases + limit - 1) // limit

        return {
            "status": "success",
            "page": page,
            "limit": limit,
            "total_purchases": total_purchases,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "data": transactions
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# GET DETAIL OF PURCHASED ITEM 
@frappe.whitelist()
def get_purchased_item_detail(transaction_id):
    try:
        current_user = frappe.session.user
        if current_user == "Guest":
            frappe.throw("Must be logged in")

        # ambil transaksi
        if not frappe.db.exists("Marketplace Transaction", transaction_id):
            return {"status": "error", "message": f"Transaction '{transaction_id}' not found"}

        tx = frappe.get_doc("Marketplace Transaction", transaction_id)

        # pastikan transaksi milik user ini & status sukses
        if tx.user != current_user:
            return {"status": "error", "message": "This transaction does not belong to you"}
        if tx.status != "Success":
            return {"status": "error", "message": "This transaction is not successful"}

        # ambil detail item
        if not frappe.db.exists("Item", tx.item):
            return {"status": "error", "message": f"Item '{tx.item}' not found"}

        item_doc = frappe.get_doc("Item", tx.item)

        return {
            "status": "success",
            "data": {
                "name": tx.name,
                "item": tx.item,
                "amount": tx.amount,
                "balance_type": tx.balance_type,
                "status": tx.status,
                "creation": tx.creation,
                "item_detail": {
                    "name": item_doc.name,
                    "item_name": item_doc.item_name,
                    "description": item_doc.description,
                    "balance_type": item_doc.balance_type,
                    "category": item_doc.category,
                    "image": item_doc.image,
                    "price": item_doc.price
                }
            }
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
