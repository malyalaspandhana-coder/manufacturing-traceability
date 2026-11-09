
from pymongo import MongoClient
from collections import defaultdict

client = MongoClient("mongodb://localhost:27017/")
db = client["manufacturing_traceability"]

order_id = "WO-000220"

order = db.production_orders.find_one({"order_id": order_id})

if not order:
    print("Production order not found")
else:
    product_id = order["product_id"]
    quantity = float(order["quantity_ordered"])

    bom_rows = list(db.bom.find({"product_id": product_id}))
    consumption_rows = list(
        db.material_consumption.find({"order_id": order_id})
    )

    lots = {
        lot["lot_id"]: lot
        for lot in db.material_lots.find()
    }

    required = defaultdict(float)
    consumed = defaultdict(float)

    for item in bom_rows:
        material = item["material_name"].strip().lower()
        required[material] += (
            float(item["quantity_required"]) * quantity
        )

    for item in consumption_rows:
        lot = lots.get(item["lot_id"])
        if lot:
            material = lot["material_name"].strip().lower()
            consumed[material] += float(item["quantity_consumed"])

    print("\nBOM vs ACTUAL MATERIAL CONSUMPTION")
    print("Production Order:", order_id)
    print("Product:", product_id)
    print("Order Quantity:", quantity)

    all_materials = sorted(set(required) | set(consumed))

    for material in all_materials:
        expected = required.get(material, 0)
        actual = consumed.get(material, 0)

        status = "PASS" if abs(expected - actual) < 0.001 else "CHECK"

        print(f"\nMaterial: {material}")
        print("Required:", expected)
        print("Actually consumed:", actual)
        print("Status:", status)

    client.close()
