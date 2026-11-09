from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database
db = client["manufacturing_traceability"]

# Select collections
products = db["products"]
suppliers = db["suppliers"]
material_consumption = db["material_consumption"]
bom = db["bom"]
inspection_plans = db["inspection_plans"]
material_lots = db["material_lots"]
production_orders = db["production_orders"]
inspection_results = db["inspection_results"]
# Additional traceability collections
machines = db["machines"]
process_steps = db["process_steps"]
defect_records = db["defect_records"]
capa_records = db["capa_records"]

print("MongoDB Connected Successfully!")

print("Database:", db.name)
print("Collections:", db.list_collection_names())