#!/bin/sh

echo "🚀 Starting MinIO bucket initialization..."

for i in $(seq 1 30); do
  echo "🔁 Attempt $i: Connecting to MinIO..."
  mc alias set local http://minio:9001 minioadmin minioadmin && break
  sleep 2
done

if mc ls local/ecommerce-marketplace >/dev/null 2>&1; then
  echo "✅ Bucket 'ecommerce-marketplace' already exists."
else
  echo "📦 Creating bucket 'ecommerce-marketplace'..."
  mc mb local/ecommerce-marketplace
  echo "✅ Bucket created!"
fi

echo "🎉 MinIO init done!"
