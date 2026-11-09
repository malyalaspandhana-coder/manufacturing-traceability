
# Manufacturing Traceability Data Generator
# YottaFlex AI - Round 3 Code Challenge

import pandas as pd
import random
from pathlib import Path

# Import project configuration
from config import (
    RANDOM_SEED,
    NUM_PRODUCTS,
    NUM_SUPPLIERS,
    NUM_MATERIAL_LOTS,
    NUM_PRODUCTION_ORDERS,
    NUM_INSPECTIONS
)

# Set fixed random seed for reproducibility
random.seed(RANDOM_SEED)

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Output directory
OUTPUT_DIR = BASE_DIR / "data" / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_data():
    """Generate manufacturing traceability data."""

    print("Starting manufacturing data generation...")

    print(f"Products: {NUM_PRODUCTS}")
    print(f"Suppliers: {NUM_SUPPLIERS}")
    print(f"Material Lots: {NUM_MATERIAL_LOTS}")
    print(f"Production Orders: {NUM_PRODUCTION_ORDERS}")
    print(f"Inspections: {NUM_INSPECTIONS}")

    # Step 1: Generate Products

    products = []

    categories = [
        "Electronics",
        "Automotive",
        "Machinery",
        "Components"
    ]

    for i in range(NUM_PRODUCTS):
        products.append({
            "product_id": f"SKU-{i+1:06d}",
            "product_name": f"Product {i+1}",
            "category": random.choice(categories),
            "status": "Active"
        })

    products_df = pd.DataFrame(products)

    products_df.to_csv(
        OUTPUT_DIR / "products.csv",
        index=False
    )

    print("200 Products generated successfully!")
    
    # Step 2: Generate Suppliers

    suppliers = []

    for i in range(NUM_SUPPLIERS):
        suppliers.append({
            "supplier_id": f"SUP-{i+1:06d}",
            "supplier_name": f"Supplier {i+1}",
            "location": random.choice([
                "Hyderabad",
                "Mumbai",
                "Delhi",
                "Chennai",
                "Bangalore"
            ]),
            "status": "Active"
        })

    suppliers_df = pd.DataFrame(suppliers)

    suppliers_df.to_csv(
        OUTPUT_DIR / "suppliers.csv",
        index=False
    )

    print("50 Suppliers generated successfully!")
    
    # Step 3: Generate Material Lots

    material_lots = []

    for i in range(NUM_MATERIAL_LOTS):
        material_lots.append({
            "lot_id": f"LOT-{i+1:06d}",
            "supplier_id": random.choice(suppliers)["supplier_id"],
            "material_name": random.choice([
                "Steel",
                "Aluminium",
                "Copper",
                "Plastic",
                "Rubber"
            ]),
            "quantity_received": random.randint(100, 1000),
            "status": "Available"
        })

    material_lots_df = pd.DataFrame(material_lots)

    material_lots_df.to_csv(
        OUTPUT_DIR / "material_lots.csv",
        index=False
    )

    print("2000 Material Lots generated successfully!")

# Step 4: Generate Production Orders
# Load generated products
products = pd.read_csv(
    OUTPUT_DIR / "products.csv"
).to_dict(orient="records")

production_orders = []

for i in range(NUM_PRODUCTION_ORDERS):
    production_orders.append({
        "order_id": f"WO-{i+1:06d}",
        "product_id": random.choice(products)["product_id"],
        "quantity_ordered": random.randint(50, 500),
        "status": random.choice([
            "Pending",
            "In Progress",
            "Completed"
        ])
    })

production_orders_df = pd.DataFrame(production_orders)

production_orders_df.to_csv(
    OUTPUT_DIR / "production_orders.csv",
    index=False
)
    
print("5000 Production Orders generated successfully!")


    # Step 5: Generate Inspection Results

inspection_results = []

for i in range(NUM_INSPECTIONS):

        order = random.choice(production_orders)

        inspected = random.randint(
            1, order["quantity_ordered"]
        )

        defective = random.randint(
            0, min(10, inspected)
        )

        result = "Pass" if defective == 0 else "Fail"

        inspection_results.append({
            "inspection_id": f"INS-{i+1:06d}",
            "order_id": order["order_id"],
            "inspected_quantity": inspected,
            "defect_quantity": defective,
            "result": result
        })

inspection_df = pd.DataFrame(inspection_results)
print(inspection_df["result"].value_counts())

inspection_df.to_csv(
        OUTPUT_DIR / "inspection_results.csv",
        index=False
    )

print("20000 Inspection Results generated successfully!")




if __name__ == "__main__":
    generate_data()
