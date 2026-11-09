from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["manufacturing_traceability"]

# Create unique indexes
db.products.create_index(
    "product_id",
    unique=True
)

db.suppliers.create_index(
    "supplier_id",
    unique=True
)

print("MongoDB indexes created successfully!")

print("Product indexes:", db.products.index_information())
print("Supplier indexes:", db.suppliers.index_information())

client.close()