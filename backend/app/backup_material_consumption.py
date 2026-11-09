
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["manufacturing_traceability"]

source = db["material_consumption"]
backup = db["material_consumption_backup_20261109"]

# Do not overwrite an existing backup.
if backup.count_documents({}) > 0:
    raise RuntimeError(
        "Backup already contains records. No changes made."
    )

records = list(source.find({}))

if records:
    for record in records:
        record.pop("_id", None)

    backup.insert_many(records)

print("Backup completed.")
print("Original records:", source.count_documents({}))
print("Backup records:", backup.count_documents({}))

if source.count_documents({}) != backup.count_documents({}):
    raise RuntimeError("Backup count mismatch!")
