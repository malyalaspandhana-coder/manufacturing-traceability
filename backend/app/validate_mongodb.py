
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

db = client["manufacturing_traceability"]

# Expected collection counts
expected_counts = {
    "products": 200,
    "suppliers": 50,
    "material_lots": 2000,
    "production_orders": 5000,
    "inspection_results": 20000,
    "machines": 25,
    "process_steps": 15000,
    "defect_records": 18011,
    "capa_records": 18011
}

print("\nMONGODB DATABASE VALIDATION")
print("-" * 40)

all_valid = True

for collection_name, expected in expected_counts.items():
    actual = db[collection_name].count_documents({})

    print(f"{collection_name}: {actual} documents")

    if actual != expected:
        print(f"  Expected: {expected} - COUNT MISMATCH")
        all_valid = False

print("-" * 40)

if all_valid:
    print("ALL COLLECTION COUNTS VALIDATED SUCCESSFULLY!")
else:
    print("VALIDATION FAILED: Please check the counts.")

client.close()
