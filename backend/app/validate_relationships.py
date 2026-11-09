import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/generated")

# Load CSV files
products = pd.read_csv(DATA_DIR / "products.csv")
suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
material_lots = pd.read_csv(DATA_DIR / "material_lots.csv")
production_orders = pd.read_csv(DATA_DIR / "production_orders.csv")
inspection_results = pd.read_csv(DATA_DIR / "inspection_results.csv")

print("Starting Relationship Validation...\n")

# 1. Check Product IDs in Production Orders
invalid_products = production_orders[
    ~production_orders["product_id"].isin(products["product_id"])
]

print("Invalid Product References:", len(invalid_products))

# 2. Check Supplier IDs in Material Lots
invalid_suppliers = material_lots[
    ~material_lots["supplier_id"].isin(suppliers["supplier_id"])
]

print("Invalid Supplier References:", len(invalid_suppliers))

# 3. Check Order IDs in Inspection Results
invalid_orders = inspection_results[
    ~inspection_results["order_id"].isin(production_orders["order_id"])
]

print("Invalid Order References:", len(invalid_orders))

print("\nRelationship Validation Completed!")