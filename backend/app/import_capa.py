
import pandas as pd
from pathlib import Path
from pymongo import ReplaceOne
from mongodb_connection import capa_records

# Locate the generated CAPA CSV
BASE_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BASE_DIR / "data" / "generated" / "capa_records.csv"

# Read CAPA records
df = pd.read_csv(CSV_PATH)
records = df.to_dict(orient="records")

# Update existing records or insert new ones
operations = [
    ReplaceOne(
        {"capa_id": record["capa_id"]},
        record,
        upsert=True
    )
    for record in records
]

if operations:
    result = capa_records.bulk_write(operations)

    print("CAPA MongoDB update successful!")
    print("CSV records:", len(records))
    print("Updated:", result.modified_count)
    print("Inserted:", result.upserted_count)
    print("Total CAPA records:", capa_records.count_documents({}))
else:
    print("No CAPA records found.")
