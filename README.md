# Frappe Ecommerce Marketplace

An ecommerce marketplace system built using Frappe Framework with Golang wallet service integration and MinIO for file storage.

## 🏗️ System Architecture

- **Frontend & Backend**: Frappe Framework
- **Wallet Service**: Golang (Port 8080)
- **File Storage**: MinIO (Port 9001)
- **Database**: MariaDB/MySQL (via Frappe)

## 📋 Key Features

### 1. Item Management
- CRUD operations for marketplace items
- Image upload with MinIO storage
- Item categorization
- Pricing system

### 2. Balance & Wallet System
- Integration with Golang wallet service
- Multiple balance types (e.g., coin, point, cash)
- Automatic wallet creation for new users
- Transaction tracking

### 3. File Management
- MinIO integration for image storage
- Presigned URL generation
- Automatic file attachment to items

## 🛠️ Setup & Installation

### Prerequisites
- Frappe Framework
- MinIO Server
- Golang Wallet Service (running on port 8080)

### 1. MinIO Setup
```bash
# Start MinIO server
minio server /data --address ":9001" --console-address ":9002"

# Default credentials
# Access Key: minioadmin
# Secret Key: minioadmin
```

### 2. Frappe Installation
```bash
# Install app to your Frappe site
bench get-app [your-app-name]
bench --site [site-name] install-app [your-app-name]
```

### 3. Configuration
Ensure MinIO client is properly configured in `file_management.py`:
```python
client = Minio(
    endpoint="127.0.0.1:9001",
    access_key="minioadmin", 
    secret_key="minioadmin",
    secure=False
)
```

## 📚 API Documentation

### Balance Type Management

#### Create Balance Type
```http
POST /api/method/ecommerce_app.e_commerce_marketplace.api.balance_type_api.create_balance_type?type_name=Coins
```

#### Get Balance Type
```http
GET /api/method/ecommerce_app.e_commerce_marketplace.api.balance_type_api.get_balance_type?name=Coins
```

#### List All Balance Types
```http
GET /api/method/ecommerce_app.e_commerce_marketplace.api.balance_type_api.list_balance_types
```

#### Delete Balance Type
```http
DELETE /api/method/ecommerce_app.e_commerce_marketplace.api.balance_type_api.delete_balance_type?name=Coins
```

### Item Category Management

#### Create Item Category
```http
POST /api/method/ecommerce_app.e_commerce_marketplace.api.item_category_api.create_item_category?category_name=Electronics&description=Produk elektronik
```

#### Get Item Category
```http
GET /api/method/ecommerce_app.e_commerce_marketplace.api.item_category_api.get_item_category?name=Electronics
```

#### List All Item Categories
```http
GET /api/method/ecommerce_app.e_commerce_marketplace.api.item_category_api.list_item_categories
```

#### Delete Item Category
```http
DELETE /api/method/ecommerce_app.e_commerce_marketplace.api.item_category_api.delete_item_category?name=Electronics
```

### Item Management

#### Create Item
```http
POST /api/method/ecommerce_app.e_commerce_marketplace.api.item_api.create_item?item_name=HP&price=500.8&balance_type=Coins&category=Electronics&description=Samsung S24
```

#### Get Item by ID
```http
GET /api/method/ecommerce_app.e_commerce_marketplace.api.item_api.get_item?name=HP-38
```

#### Get Items by Name
```http
GET /api/method/ecommerce_app.e_commerce_marketplace.api.item_api.get_items_by_name?item_name=HP
```

#### Get All Items
```http
GET /api/method/ecommerce_app.e_commerce_marketplace.api.item_api.get_all_items?page=1&limit=2&category=Electronics
```

#### Delete Item
```http
DELETE /api/method/ecommerce_app.e_commerce_marketplace.api.item_api.delete_item?name=HP-38
```

### Marketplace Transaction

#### Buy Item
```http
POST /api/method/ecommerce_app.e_commerce_marketplace.api.buy_item.buy_item?balance_type=Coins&amount=500.5&item=HP-38
```

## 🗂️ DocTypes

### 1. Balance Type
- `type_name`: Name of balance type (e.g., Coin, Point, Cash)

### 2. Item Category  
- `category_name`: Category name
- `description`: Category description (optional)

### 3. Item
- `item_name`: Item name
- `description`: Item description
- `balance_type`: Link to Balance Type
- `category`: Link to Item Category
- `image`: Item image URL
- `price`: Item price

### 4. Player Wallet Mapping
- `user`: Link to User
- `wallet_user_id`: Wallet ID from Golang service

## 🔄 Integration Flow

### User Registration Flow
##### 1. New user registers in Frappe
##### 2. `create_wallet` hook is automatically triggered
##### 3. API call to Golang wallet service to create wallet
##### 4. wallet_user_id mapping is saved in `Player Wallet Mapping`
##### 5. User is assigned "Marketplace User" role

### Purchase Flow
##### 1. User calls `buy_item` API
##### 2. System checks user wallet mapping
##### 3. API call to Golang wallet service to deduct balance
##### 4. Transaction record is created with status based on response
##### 5. Response is returned to user

### File Upload Flow
##### 1. File is uploaded via Frappe
##### 2. File is saved to MinIO bucket "ecommerce-marketplace"
##### 3. Presigned URL is generated for file access
##### 4. File record is created in Frappe
##### 5. If attached to Item, image field is automatically updated
