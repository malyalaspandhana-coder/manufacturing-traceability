
import pandas as pd
from pathlib import Path
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_FILE = BASE_DIR / "data" / "generated" / "material_consumption_rebuilt.csv"

client = MongoClient("mongodb://localhost:27017/")
db = client["manufacturing_traceability"]
collection = db["material_consumption"]

# Load validated CSV
df = pd.read_csv(CSV_FILE)
records = df.to_dict(orient="records")

# Stop if the CSV is empty or contains duplicate IDs.
if not records:
    raise ValueError("No material consumption records found.")

ids = [r["consumption_id"] for r in records]
if len(ids) != len(set(ids)):
    raise ValueError("Duplicate consumption IDs found.")

# Confirm backup exists before replacing active data.
backup = db["material_consumption_backup_20261109"]
if backup.count_documents({}) != 410:
    raise RuntimeError("Backup verification failed. Import cancelled.")

# Replace only the material consumption collection.
collection.delete_many({})

try:
    collection.insert_many(records, ordered=True)
except Exception:
    collection.delete_many({})
    collection.insert_many(list(backup.find({}, {"_id": 0})))
    raise

print("Material consumption import successful.")
print("Imported records:", collection.count_documents({}))
print("Backup records:", backup.count_documents({}))
