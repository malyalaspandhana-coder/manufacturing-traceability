import pandas as pd
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "generated"

print("Starting Manufacturing Data Analysis...")

# Load datasets
products = pd.read_csv(DATA_DIR / "products.csv")
suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
orders = pd.read_csv(DATA_DIR / "production_orders.csv")
inspections = pd.read_csv(DATA_DIR / "inspection_results.csv")

# Dataset summary
print("\n--- Dataset Summary ---")
print("Total Products:", len(products))
print("Total Suppliers:", len(suppliers))
print("Total Production Orders:", len(orders))
print("Total Inspections:", len(inspections))

# Inspection analysis
print("\n--- Inspection Results ---")
print(inspections["result"].value_counts())

# Defect analysis
total_inspected = inspections["inspected_quantity"].sum()
total_defects = inspections["defect_quantity"].sum()

defect_rate = (total_defects / total_inspected) * 100

print("\nTotal Inspected:", total_inspected)
print("Total Defects:", total_defects)
print("Defect Rate:", round(defect_rate, 2), "%")

print("\nEDA Analysis Completed Successfully!")
import matplotlib.pyplot as plt

# Pass vs Fail Inspection Chart
inspection_counts = inspections["result"].value_counts()

plt.figure(figsize=(7, 5))

plt.bar(
    inspection_counts.index,
    inspection_counts.values
)

plt.title("Manufacturing Inspection Results")
plt.xlabel("Inspection Result")
plt.ylabel("Number of Inspections")

plt.tight_layout()
plt.show()
# Defect Rate Visualization

plt.figure(figsize=(7, 5))

plt.bar(
    ["Defective", "Non-Defective"],
    [total_defects, total_inspected - total_defects]
)

plt.title("Manufacturing Defect Analysis")
plt.xlabel("Product Quality")
plt.ylabel("Total Quantity")

plt.tight_layout()
plt.show()