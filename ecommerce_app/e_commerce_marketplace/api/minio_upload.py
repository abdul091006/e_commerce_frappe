import frappe
from minio import Minio
from minio.error import S3Error
from io import BytesIO
from datetime import timedelta

# Setup MinIO client
client = Minio(
    endpoint="127.0.0.1:9001",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

def generate_presigned_url(path, expires=3600):
    """Generate presigned URL for accessing file in MinIO"""
    try:
        bucket, object_name = path.split("/", 1)
        return client.presigned_get_object(
            bucket_name=bucket,
            object_name=object_name,
            expires=timedelta(seconds=expires)
        )
    except S3Error as e:
        frappe.throw(_("Failed to generate presigned URL: {0}").format(e))

@frappe.whitelist()
def upload_file():
    """Override Frappe's upload_file to store files in MinIO"""
    uploaded = frappe.request.files.get('file')
    if not uploaded:
        frappe.throw(_("No file provided"))

    filename = frappe.form_dict.get('filename') or uploaded.filename
    bucket = "ecommerce-marketplace"

    # Ensure bucket exists
    if not client.bucket_exists(bucket):
        try:
            client.make_bucket(bucket)
        except S3Error as e:
            frappe.throw(_("Failed to create bucket: {0}").format(e))

    # Upload file to MinIO
    file_bytes = uploaded.read()
    try:
        client.put_object(
            bucket_name=bucket,
            object_name=filename,
            data=BytesIO(file_bytes),
            length=len(file_bytes),
            content_type=uploaded.content_type or "application/octet-stream"
        )
    except S3Error as e:
        frappe.throw(_("Failed to upload to MinIO: {0}").format(e))

    # Generate presigned URL
    file_url = generate_presigned_url(f"{bucket}/{filename}")

    # Create File record
    attached_to_doctype = frappe.form_dict.get("doctype")
    attached_to_name = frappe.form_dict.get("docname")

    # Create File record
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": filename,
        "file_url": file_url,
        "is_private": 0,
        "attached_to_doctype": attached_to_doctype if attached_to_name and "new-" not in attached_to_name else None,
        "attached_to_name": attached_to_name if attached_to_name and "new-" not in attached_to_name else None
    })
    file_doc.insert(ignore_permissions=True)

    # if Item exist, update image field
    if attached_to_doctype == "Item" and attached_to_name and "new-" not in attached_to_name:
        item = frappe.get_doc("Item", attached_to_name)
        item.image = file_url
        item.save(ignore_permissions=True)

    return {
        "name": file_doc.name,
        "file_name": file_doc.file_name,
        "file_url": file_doc.file_url,
        "is_private": file_doc.is_private,
        "attached_to_doctype": frappe.form_dict.get("doctype"),
        "attached_to_name": frappe.form_dict.get("docname")
    }

def save_item_image(doc, method):
    """Update Item image field when a File is attached"""
    if doc.image and hasattr(doc, "_image_file"):
        file = doc._image_file
        filename = file.filename
        file_bytes = file.read()
        bucket = "ecommerce-marketplace"

        # Ensure bucket exists
        if not client.bucket_exists(bucket):
            try:
                client.make_bucket(bucket)
            except S3Error as e:
                frappe.throw(_("Failed to create bucket: {0}").format(e))

        # Upload to MinIO
        try:
            client.put_object(
                bucket_name=bucket,
                object_name=filename,
                data=BytesIO(file_bytes),
                length=len(file_bytes),
                content_type=file.content_type or "application/octet-stream"
            )
        except S3Error as e:
            frappe.throw(_("Failed to upload to MinIO: {0}").format(e))

        # Generate presigned URL
        file_url = generate_presigned_url(f"{bucket}/{filename}")

        # Create File record
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": filename,
            "file_url": file_url,
            "is_private": 0,
            "attached_to_doctype": "Item",
            "attached_to_name": doc.name
        })
        file_doc.insert(ignore_permissions=True)

        # Update Item image field
        doc.image = file_url