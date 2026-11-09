
import pandas as pd
import random
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "generated"
DATA_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

# Load existing datasets
orders = pd.read_csv(DATA_DIR / "production_orders.csv")
inspections = pd.read_csv(DATA_DIR / "inspection_results.csv")

print("Existing datasets loaded successfully!")

# Step 1: Generate Defect Records
defects = []

failed_inspections = inspections[
    inspections["result"] == "Fail"
]

for i, row in enumerate(
    failed_inspections.itertuples(index=False), start=1
):
    defects.append({
        "defect_id": f"DEF-{i:06d}",
        "inspection_id": row.inspection_id,
        "order_id": row.order_id,
        "defect_type": random.choice([
            "Surface Defect",
            "Dimensional Error",
            "Material Defect",
            "Assembly Defect",
            "Functional Failure"
        ]),
        "severity": random.choice([
            "Low", "Medium", "High", "Critical"
        ]),
        "defect_quantity": row.defect_quantity,
        "status": random.choice([
            "Open", "Under Investigation", "Resolved"
        ])
    })

defects_df = pd.DataFrame(defects)

defects_df.to_csv(
    DATA_DIR / "defect_records.csv",
    index=False
)

print("Defect records generated:", len(defects_df))


# Step 2: Generate CAPA Records
capa_records = []

for i, row in enumerate(defects, start=1):
    capa_records.append({
        "capa_id": f"CAPA-{i:06d}",
        "defect_id": row["defect_id"],
        "order_id": row["order_id"],
        "root_cause": random.choice([
            "Machine malfunction",
            "Human error",
            "Poor raw material quality",
            "Incorrect machine settings",
            "Improper assembly"
        ]),
        "corrective_action": random.choice([
            "Repair machine",
            "Replace defective material",
            "Rework affected product",
            "Adjust machine settings",
            "Retrain operator"
        ]),
        "preventive_action": random.choice([
            "Schedule regular maintenance",
            "Improve quality inspection",
            "Introduce operator training",
            "Monitor production parameters",
            "Improve supplier quality checks"
        ]),
        "status": "Closed" if i % 3 == 0 else "In Progress" if i % 3 == 1 else "Open",
"verified": i % 3 == 0
    })

capa_df = pd.DataFrame(capa_records)

capa_df.to_csv(
    DATA_DIR / "capa_records.csv",
    index=False
)

print("CAPA records generated:", len(capa_df))

print("\nDataset Summary")
print("Defect Records:", len(defects_df))
print("CAPA Records:", len(capa_df))
print("\nBoth datasets generated successfully!")
