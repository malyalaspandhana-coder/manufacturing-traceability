
import pandas as pd
from pathlib import Path
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["manufacturing_traceability"]

# CSV folder location
DATA_DIR = Path("data/generated")

# CSV to MongoDB collection mapping
files = {
    "products.csv": "products",
    "suppliers.csv": "suppliers",
    "material_lots.csv": "material_lots",
    "production_orders.csv": "production_orders",
    "inspection_results.csv": "inspection_results"
}

for filename, collection_name in files.items():

    file_path = DATA_DIR / filename

    print(f"\nImporting {filename}...")

    df = pd.read_csv(file_path)

    # Convert CSV data to MongoDB documents
    records = df.to_dict(orient="records")

    collection = db[collection_name]

    # Replace existing generated data safely
    collection.delete_many({})

    if records:
        collection.insert_many(records)

    print(f"{len(records)} records imported into {collection_name}")

print("\nAll CSV files imported successfully!")

client.close()
