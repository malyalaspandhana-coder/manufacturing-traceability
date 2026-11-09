
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "generated"

defects = pd.read_csv(DATA_DIR / "defect_records.csv")
capa = pd.read_csv(DATA_DIR / "capa_records.csv")
inspections = pd.read_csv(DATA_DIR / "inspection_results.csv")
orders = pd.read_csv(DATA_DIR / "production_orders.csv")

print("DEFECT AND CAPA VALIDATION")

# Check missing values
print("\nMissing Values:")
print("Defects:", defects.isnull().sum().sum())
print("CAPA:", capa.isnull().sum().sum())

# Check duplicate IDs
print("\nDuplicate IDs:")
print("Defect IDs:", defects["defect_id"].duplicated().sum())
print("CAPA IDs:", capa["capa_id"].duplicated().sum())

# Validate inspection references
invalid_inspections = ~defects["inspection_id"].isin(
    inspections["inspection_id"]
)

# Validate order references
invalid_defect_orders = ~defects["order_id"].isin(
    orders["order_id"]
)

invalid_capa_defects = ~capa["defect_id"].isin(
    defects["defect_id"]
)

invalid_capa_orders = ~capa["order_id"].isin(
    orders["order_id"]
)
# Validate defect quantity against inspected quantity
inspection_limits = inspections.set_index("inspection_id")["inspected_quantity"]

defect_totals = defects.groupby("inspection_id")["defect_quantity"].sum()

invalid_defect_quantities = (
    defect_totals >
    inspection_limits.reindex(defect_totals.index)
).fillna(True)

print("\nRelationship Validation:")
print("Invalid Defect Quantities:", invalid_defect_quantities.sum())
print("Invalid Inspection IDs:", invalid_inspections.sum())
print("Invalid Defect Order IDs:", invalid_defect_orders.sum())
print("Invalid CAPA Defect IDs:", invalid_capa_defects.sum())
print("Invalid CAPA Order IDs:", invalid_capa_orders.sum())

if (
    defects.isnull().sum().sum() == 0
    and capa.isnull().sum().sum() == 0
    and defects["defect_id"].duplicated().sum() == 0
    and capa["capa_id"].duplicated().sum() == 0
    and invalid_inspections.sum() == 0
    and invalid_defect_orders.sum() == 0
    and invalid_capa_defects.sum() == 0
    and invalid_capa_orders.sum() == 0
):
    print("\nVALIDATION SUCCESSFUL!")
else:
    print("\nVALIDATION FAILED!")
