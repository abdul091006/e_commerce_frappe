import frappe
import requests

def create_wallet(doc, method):
    user_id = doc.name

    try:
        response = requests.post("http://localhost:8080/api/v1/wallets")
        response.raise_for_status()

        wallet_data = response.json()
        wallet_user_id = wallet_data.get("data", {}).get("wallet_user_id")

        if not wallet_user_id:
            frappe.throw("Wallet service tidak mengembalikan wallet_user_id")

        wallet_doc = frappe.get_doc({
            "doctype": "Player Wallet Mapping",
            "user": user_id,
            "wallet_user_id": wallet_user_id,
        })
        wallet_doc.insert(ignore_permissions=True)

        user = frappe.get_doc("User", user_id)
        user.add_roles("Marketplace User")

    except Exception as e:
        frappe.log_error(f"Create wallet failed for {user_id}: {str(e)}")
