
import pandas as pd
from pathlib import Path
import shutil

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "generated"

BOM_FILE = DATA_DIR / "bom.csv"
LOTS_FILE = DATA_DIR / "material_lots.csv"
ORDERS_FILE = DATA_DIR / "production_orders.csv"

OUTPUT_FILE = DATA_DIR / "material_consumption_rebuilt.csv"
BACKUP_FILE = DATA_DIR / "material_consumption_before_rebuild.csv"

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

bom = pd.read_csv(BOM_FILE)
lots = pd.read_csv(LOTS_FILE)
orders = pd.read_csv(ORDERS_FILE)

required_columns = {
    "bom": {"product_id", "lot_id", "material_name", "quantity_required"},
    "lots": {"lot_id", "material_name", "quantity_received"},
    "orders": {"order_id", "product_id", "quantity_ordered"}
}

for name, required in required_columns.items():
    frame = {"bom": bom, "lots": lots, "orders": orders}[name]
    missing = required - set(frame.columns)

    if missing:
        raise ValueError(
            f"{name}.csv is missing columns: {sorted(missing)}"
        )

# --------------------------------------------------
# 3. NORMALIZE DATA
# --------------------------------------------------

for frame, columns in [
    (bom, ["product_id", "lot_id", "material_name"]),
    (lots, ["lot_id", "material_name"]),
    (orders, ["order_id", "product_id"])
]:
    for column in columns:
        frame[column] = frame[column].astype(str).str.strip()

bom["material_key"] = bom["material_name"].str.lower()
lots["material_key"] = lots["material_name"].str.lower()

bom["quantity_required"] = pd.to_numeric(
    bom["quantity_required"], errors="coerce"
)

lots["quantity_received"] = pd.to_numeric(
    lots["quantity_received"], errors="coerce"
)

orders["quantity_ordered"] = pd.to_numeric(
    orders["quantity_ordered"], errors="coerce"
)

if bom[["quantity_required"]].isna().any().any():
    raise ValueError("BOM contains invalid required quantities.")

if lots[["quantity_received"]].isna().any().any():
    raise ValueError("Material lots contain invalid received quantities.")

if orders[["quantity_ordered"]].isna().any().any():
    raise ValueError("Production orders contain invalid quantities.")

if lots["lot_id"].duplicated().any():
    raise ValueError("Duplicate material lot IDs found.")

# --------------------------------------------------
# 4. EXCLUDE UNAVAILABLE LOTS
# --------------------------------------------------

blocked_statuses = {
    "blocked", "quarantine", "inactive", "rejected"
}

if "status" in lots.columns:
    lots = lots[
        ~lots["status"].astype(str).str.strip().str.lower().isin(
            blocked_statuses
        )
    ].copy()

# --------------------------------------------------
# 5. PREPARE STOCK
# --------------------------------------------------

stock = dict(
    zip(lots["lot_id"], lots["quantity_received"].astype(float))
)

lots_by_material = {}

for material, group in lots.groupby("material_key"):
    lots_by_material[material] = group.to_dict("records")

# --------------------------------------------------
# 6. ALLOCATE MATERIAL TO PRODUCTION ORDERS
# --------------------------------------------------

records = []
counter = 1
completed_orders = 0
skipped_orders = 0

for _, order in orders.iterrows():

    order_id = order["order_id"]
    product_id = order["product_id"]
    order_quantity = float(order["quantity_ordered"])

    requirements = bom[bom["product_id"] == product_id]

    if requirements.empty or order_quantity <= 0:
        skipped_orders += 1
        continue

    # Temporary stock prevents partial or duplicate allocation.
    working_stock = stock.copy()
    staged = []
    possible = True

    for _, requirement in requirements.iterrows():

        material_key = requirement["material_key"]
        required_quantity = (
            float(requirement["quantity_required"]) * order_quantity
        )

        if required_quantity <= 0:
            possible = False
            break

        remaining = required_quantity

        candidates = lots_by_material.get(material_key, [])

        # Prefer the BOM lot first, then other lots of the same material.
        preferred_lot = str(requirement["lot_id"]).strip()

        candidates = sorted(
            candidates,
            key=lambda lot: (
                lot["lot_id"] != preferred_lot,
                lot["lot_id"]
            )
        )

        for lot in candidates:

            lot_id = lot["lot_id"]
            available = working_stock.get(lot_id, 0)

            if available <= 0:
                continue

            used = min(available, remaining)

            staged.append({
                "order_id": order_id,
                "lot_id": lot_id,
                "product_id": product_id,
                "quantity_consumed": used
            })

            # Reserve stock immediately.
            working_stock[lot_id] -= used
            remaining -= used

            if remaining <= 0:
                break

        if remaining > 0:
            possible = False
            break

    # Commit only if every BOM requirement is satisfied.
    if possible:

        stock = working_stock

        for item in staged:
            item["consumption_id"] = f"CON-{counter:07d}"
            counter += 1
            records.append(item)

        completed_orders += 1

    else:
        skipped_orders += 1

# --------------------------------------------------
# 7. CREATE OUTPUT
# --------------------------------------------------

result = pd.DataFrame(
    records,
    columns=[
        "consumption_id",
        "order_id",
        "lot_id",
        "product_id",
        "quantity_consumed"
    ]
)

# --------------------------------------------------
# 8. VALIDATE BEFORE SAVING
# --------------------------------------------------

if result["consumption_id"].duplicated().any():
    raise ValueError("Duplicate consumption IDs generated.")

if result["order_id"].isin(orders["order_id"]).all() is False:
    raise ValueError("Invalid production order reference.")

if result["lot_id"].isin(lots["lot_id"]).all() is False:
    raise ValueError("Invalid material lot reference.")

if result["quantity_consumed"].isna().any():
    raise ValueError("Missing consumption quantity.")

if (result["quantity_consumed"] <= 0).any():
    raise ValueError("Non-positive consumption quantity found.")

consumed_by_lot = (
    result.groupby("lot_id")["quantity_consumed"].sum()
)

received_by_lot = lots.set_index("lot_id")["quantity_received"]

comparison = pd.DataFrame({
    "consumed": consumed_by_lot,
    "received": received_by_lot
}).fillna(0)

overused = comparison[
    comparison["consumed"] > comparison["received"]
]

if not overused.empty:
    raise ValueError(
        f"Stock validation failed for {len(overused)} lots."
    )

# --------------------------------------------------
# 9. PRESERVE PREVIOUS FILE AND SAVE PREVIEW
# --------------------------------------------------

old_file = DATA_DIR / "material_consumption.csv"

if old_file.exists() and not BACKUP_FILE.exists():
    shutil.copy2(old_file, BACKUP_FILE)

result.to_csv(OUTPUT_FILE, index=False)

# --------------------------------------------------
# 10. FINAL REPORT
# --------------------------------------------------

print("\nMATERIAL CONSUMPTION GENERATION SUCCESSFUL")
print("------------------------------------------")
print("Consumption records:", len(result))
print("Fully allocated orders:", completed_orders)
print("Skipped orders:", skipped_orders)
print("Duplicate consumption IDs:", result["consumption_id"].duplicated().sum())
print("Over-consumed lots:", len(overused))
print("Output:", OUTPUT_FILE)
print("\nExisting active CSV and MongoDB were not replaced.")
