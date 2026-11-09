
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/generated")

consumption = pd.read_csv(DATA_DIR / "material_consumption_rebuilt.csv")
orders = pd.read_csv(DATA_DIR / "production_orders.csv")
lots = pd.read_csv(DATA_DIR / "material_lots.csv")

# Check production order references
invalid_orders = consumption[
    ~consumption["order_id"].isin(orders["order_id"])
]

# Check material lot references
invalid_lots = consumption[
    ~consumption["lot_id"].isin(lots["lot_id"])
]

# Check product matches production order
merged = consumption.merge(
    orders[["order_id", "product_id"]],
    on="order_id",
    how="left",
    suffixes=("_consumption", "_order")
)

invalid_products = merged[
    merged["product_id_consumption"] != merged["product_id_order"]
]

# Check unique consumption IDs
duplicate_ids = consumption[
    consumption["consumption_id"].duplicated()
]

print("Total consumption records:", len(consumption))
print("Invalid order references:", len(invalid_orders))
print("Invalid lot references:", len(invalid_lots))
print("Product mismatches:", len(invalid_products))
print("Duplicate consumption IDs:", len(duplicate_ids))

if (
    invalid_orders.empty
    and invalid_lots.empty
    and invalid_products.empty
    and duplicate_ids.empty
):
    print("\nSUCCESS: All material consumption relationships are valid.")
else:
    print("\nWARNING: Please investigate the invalid records.")
