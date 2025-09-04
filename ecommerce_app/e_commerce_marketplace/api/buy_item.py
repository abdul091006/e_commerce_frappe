import frappe
import requests

@frappe.whitelist()
def buy_item(balance_type, amount, item):
    current_user = frappe.session.user

    if current_user == "Guest":
        frappe.throw("Must be logged in")

    # wallet_user_id
    mapping = frappe.get_value(
        "Player Wallet Mapping",
        {"user": current_user},
        "wallet_user_id"
    )

    if not mapping:
        frappe.throw(f"Wallet for user {current_user} is not found")

    wallet_user_id = mapping

    url = f"http://localhost:8080/api/v1/wallets/{wallet_user_id}/deduct"
    res = requests.post(url, json={
        "type": balance_type,
        "amount": amount
    })

    if res.status_code != 200:
        try:
            data = res.json()
        except Exception:
            data = {"success": False, "message": res.text}
    else:
        data = res.json()


    tx = frappe.get_doc({
        "doctype": "Marketplace Transaction",
        "user": current_user,
        "item": item,
        "amount": amount,
        "balance_type": balance_type,
        "status": "Success" if data.get("success") else "Failed",
    })
    tx.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "success": data.get("success", False),
        "message": data.get("message", "Terjadi kesalahan saat order"),
        "error": data.get("error", "Terjadi kesalahan saat order"),
        "item": item,
        "amount": amount,
        "balance_type": balance_type,
        "wallet_response": data
    }

