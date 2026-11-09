import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/generated")

files = [
    "products.csv",
    "suppliers.csv",
    "material_lots.csv",
    "production_orders.csv",
    "inspection_results.csv"
]

print("Starting Data Validation...\n")

for file in files:
    print(f"\nChecking: {file}")

    df = pd.read_csv(DATA_DIR / file)

    print("Rows:", len(df))
    print("Missing values:", df.isnull().sum().sum())
    print("Duplicate rows:", df.duplicated().sum())

print("\nData Validation Completed!")