
import csv
from pathlib import Path
from mongodb_connection import bom, inspection_plans

PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_DIR / "data" / "generated"


def import_csv(file_name, collection, id_field):
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    imported = 0

    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for record in reader:
            record_id = record.get(id_field)

            if not record_id:
                continue

            collection.update_one(
                {id_field: record_id},
                {"$set": record},
                upsert=True
            )
            imported += 1

    print(f"{file_name}: {imported} records processed.")
    print(f"MongoDB total: {collection.count_documents({})}")


if __name__ == "__main__":
    import_csv("bom.csv", bom, "bom_id")
    import_csv("inspection_plans.csv", inspection_plans, "plan_id")
    print("Import completed.")
