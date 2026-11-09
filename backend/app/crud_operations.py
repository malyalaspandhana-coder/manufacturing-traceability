from mongodb_connection import products

# CREATE - Insert a product
new_product = {
    "product_id": "SKU-TEST001",
    "product_name": "Test Product",
    "category": "Electronics",
    "status": "Active"
}

products.insert_one(new_product)

print("Product inserted successfully!")

# READ - Retrieve product
product = products.find_one(
    {"product_id": "SKU-TEST001"}
)

print("Product Details:", product)
# UPDATE - Update product status

products.update_one(
    {"product_id": "SKU-TEST001"},
    {"$set": {"status": "Under Maintenance"}}
)

print("Product updated successfully!")

# Verify updated product
updated_product = products.find_one(
    {"product_id": "SKU-TEST001"}
)

print("Updated Product:", updated_product)
# DELETE - Delete test product

delete_result = products.delete_one(
    {"product_id": "SKU-TEST001"}
)

if delete_result.deleted_count == 1:
    print("Test product deleted successfully!")
else:
    print("Product not found!")