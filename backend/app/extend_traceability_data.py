import pandas as pd
import random
from pathlib import Path

from config import (
    NUM_MACHINES,
    NUM_PROCESS_STEPS,
    MACHINE_PREFIX,
    PROCESS_STEP_PREFIX
)

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "generated"

random.seed(42)

# Load existing datasets
products = pd.read_csv(DATA_DIR / "products.csv")
production_orders = pd.read_csv(DATA_DIR / "production_orders.csv")

print("Existing datasets loaded successfully!")

# STEP 1: Generate Machines
machines = []

machine_types = [
    "CNC Machine",
    "Assembly Machine",
    "Welding Machine",
    "Packaging Machine",
    "Cutting Machine"
]

for i in range(NUM_MACHINES):
    machines.append({
        "machine_id": f"{MACHINE_PREFIX}-{i+1:04d}",
        "machine_name": f"Machine {i+1}",
        "machine_type": random.choice(machine_types),
        "status": random.choice(["Active", "Maintenance"])
    })

machines_df = pd.DataFrame(machines)

machines_df.to_csv(
    DATA_DIR / "machines.csv",
    index=False
)

print("25 Machines generated successfully!")

# STEP 2: Generate Process Steps
process_steps = []

step_names = [
    "Raw Material Preparation",
    "Cutting",
    "Machining",
    "Assembly",
    "Welding",
    "Quality Inspection",
    "Packaging"
]

# Convert orders once, outside the loop
orders_list = production_orders.to_dict("records")

for i in range(NUM_PROCESS_STEPS):
    order = random.choice(orders_list)
    machine = random.choice(machines)

    process_steps.append({
        "process_step_id": f"{PROCESS_STEP_PREFIX}-{i+1:06d}",
        "order_id": order["order_id"],
        "machine_id": machine["machine_id"],
        "step_name": random.choice(step_names),
        "status": random.choice([
            "Pending",
            "In Progress",
            "Completed"
        ])
    })

process_steps_df = pd.DataFrame(process_steps)

process_steps_df.to_csv(
    DATA_DIR / "process_steps.csv",
    index=False
)

print("15000 Process Steps generated successfully!")

print("\nDataset Summary")
print("Machines:", len(machines_df))
print("Process Steps:", len(process_steps_df))
# STEP 3: Validate Machine and Process Step relationships

invalid_orders = (
    set(process_steps_df["order_id"])
    - set(production_orders["order_id"])
)

invalid_machines = (
    set(process_steps_df["machine_id"])
    - set(machines_df["machine_id"])
)

duplicate_machine_ids = machines_df["machine_id"].duplicated().sum()

duplicate_step_ids = process_steps_df["process_step_id"].duplicated().sum()

print("\nMACHINE AND PROCESS STEP VALIDATION")
print("Invalid Order IDs:", len(invalid_orders))
print("Invalid Machine IDs:", len(invalid_machines))
print("Duplicate Machine IDs:", duplicate_machine_ids)
print("Duplicate Process Step IDs:", duplicate_step_ids)

if (
    len(invalid_orders) == 0
    and len(invalid_machines) == 0
    and duplicate_machine_ids == 0
    and duplicate_step_ids == 0
):
    print("Validation successful!")
else:
    print("Validation failed!")