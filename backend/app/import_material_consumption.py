
import pandas as pd
from pathlib import Path
from pymongo import MongoClient

# Load CSV
DATA_DIR = Path("data/generated")
file_path = DATA_DIR / "material_consumption.csv"

df = pd.read_csv(file_path)
records = df.to_dict("records")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["manufacturing_traceability"]

collection = db["material_consumption"]

# Prevent duplicate imports using consumption_id
if records:
    existing_ids = set(
        collection.distinct("consumption_id")
    )

    new_records = [
        record for record in records
        if record["consumption_id"] not in existing_ids
    ]

    if new_records:
        collection.insert_many(new_records)

    print("CSV records:", len(records))
    print("New records imported:", len(new_records))
    print("Already existing records skipped:", len(records) - len(new_records))
    print("Total MongoDB records:", collection.count_documents({}))
else:
    print("No records found in CSV.")

client.close()
