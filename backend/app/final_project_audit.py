
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["manufacturing_traceability"]

collections = [
    "products",
    "bom",
    "suppliers",
    "material_lots",
    "production_orders",
    "machines",
    "process_steps",
    "inspection_plans",
    "inspection_results",
    "defect_records",
    "capa_records",
    "material_consumption"
]

print("\n========== YOTTAFLEX PROJECT AUDIT ==========\n")

# 1. Collection counts
print("1. DATABASE COLLECTIONS")
for name in collections:
    print(f"{name}: {db[name].count_documents({})}")

# 2. Relationship checks
checks = []

def check(label, collection, field, reference_collection, reference_field):
    valid_ids = set(
        db[reference_collection].distinct(reference_field)
    )
    invalid = db[collection].count_documents({
        field: {"$nin": list(valid_ids)}
    })
    checks.append((label, invalid))

check("BOM -> Product", "bom", "product_id", "products", "product_id")
check("BOM -> Material Lot", "bom", "lot_id", "material_lots", "lot_id")
check("Material Lot -> Supplier", "material_lots", "supplier_id", "suppliers", "supplier_id")
check("Production Order -> Product", "production_orders", "product_id", "products", "product_id")
check("Process Step -> Production Order", "process_steps", "order_id", "production_orders", "order_id")
check("Process Step -> Machine", "process_steps", "machine_id", "machines", "machine_id")
check("Inspection Result -> Production Order", "inspection_results", "order_id", "production_orders", "order_id")
check("Defect -> Production Order", "defect_records", "order_id", "production_orders", "order_id")
check("Defect -> Inspection", "defect_records", "inspection_id", "inspection_results", "inspection_id")
check("CAPA -> Defect", "capa_records", "defect_id", "defect_records", "defect_id")
check("CAPA -> Production Order", "capa_records", "order_id", "production_orders", "order_id")
check("Consumption -> Production Order", "material_consumption", "order_id", "production_orders", "order_id")
check("Consumption -> Material Lot", "material_consumption", "lot_id", "material_lots", "lot_id")

print("\n2. RELATIONSHIP VALIDATION")
for label, invalid in checks:
    print(f"{label}: {'PASS' if invalid == 0 else 'FAIL'} ({invalid} invalid)")

# 3. Consumption quantity versus received stock
print("\n3. MATERIAL STOCK VALIDATION")

pipeline = [
    {
        "$group": {
            "_id": "$lot_id",
            "consumed": {"$sum": "$quantity_consumed"}
        }
    },
    {
        "$lookup": {
            "from": "material_lots",
            "localField": "_id",
            "foreignField": "lot_id",
            "as": "lot"
        }
    },
    {"$unwind": "$lot"},
    {
        "$match": {
            "$expr": {
                "$gt": ["$consumed", "$lot.quantity_received"]
            }
        }
    }
]

overused = list(db.material_consumption.aggregate(pipeline))
print("Over-consumed lots:", len(overused))


# 4. DEFECT QUANTITY VALIDATION
print("\n4. DEFECT QUANTITY VALIDATION")

pipeline = [
    {
        "$lookup": {
            "from": "inspection_results",
            "localField": "inspection_id",
            "foreignField": "inspection_id",
            "as": "inspection"
        }
    },
    {"$unwind": "$inspection"},
    {
        "$addFields": {
            "defect_qty": {
                "$convert": {
                    "input": "$defect_quantity",
                    "to": "double",
                    "onError": 0,
                    "onNull": 0
                }
            },
            "inspected_qty": {
                "$convert": {
                    "input": "$inspection.inspected_quantity",
                    "to": "double",
                    "onError": 0,
                    "onNull": 0
                }
            }
        }
    },
    {
        "$match": {
            "$expr": {
                "$gt": ["$defect_qty", "$inspected_qty"]
            }
        }
    },
    {"$count": "invalid_count"}
]

result = list(db.defect_records.aggregate(pipeline))
invalid_defects = result[0]["invalid_count"] if result else 0

print("Defects exceeding inspected quantity:", invalid_defects)


# 5. CAPA verification
print("\n5. CAPA VERIFICATION")

closed_unverified = db.capa_records.count_documents({
    "status": "Closed",
    "verified": {"$ne": True}
})
missing_verification = db.capa_records.count_documents({
    "verified": {"$exists": False}
})

print("Closed but unverified CAPAs:", closed_unverified)
print("CAPAs missing verification field:", missing_verification)

# 6. Material consumption product matching
print("\n6. PRODUCT MATCH VALIDATION")

mismatches = 0
for item in db.material_consumption.find():
    order = db.production_orders.find_one(
        {"order_id": item.get("order_id")}
    )
    if order and order.get("product_id") != item.get("product_id"):
        mismatches += 1

print("Consumption product mismatches:", mismatches)

print("\n========== AUDIT COMPLETED ==========")
print("This audit did not modify your database.")
