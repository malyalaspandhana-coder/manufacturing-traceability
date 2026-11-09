from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI(title="Manufacturing Traceability API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

db = client["manufacturing_traceability"]

# Home API
@app.get("/")
def home():
    return {
        "message": "Manufacturing Traceability API is running!"
    }

# Get all products
@app.get("/products")
def get_products():
    products = list(
        db.products.find({}, {"_id": 0}).limit(100)
    )
    return products

# Get all suppliers
@app.get("/suppliers")
def get_suppliers():
    suppliers = list(
        db.suppliers.find({}, {"_id": 0}).limit(100)
    )
    return suppliers
# Get all material lots
@app.get("/material-lots")
def get_material_lots():
    return list(db.material_lots.find({}, {"_id": 0}).limit(100))


# Get all production orders
@app.get("/production-orders")
def get_production_orders():
    return list(db.production_orders.find({}, {"_id": 0}).limit(100))


# Get all inspection results
@app.get("/inspections")
def get_inspections():
    return list(db.inspection_results.find({}, {"_id": 0}).limit(100))


# Get all machines
@app.get("/machines")
def get_machines():
    return list(db.machines.find({}, {"_id": 0}).limit(100))


# Get all process steps
@app.get("/process-steps")
def get_process_steps():
    return list(db.process_steps.find({}, {"_id": 0}).limit(100))


# Get all defect records
@app.get("/defects")
def get_defects():
    return list(db.defect_records.find({}, {"_id": 0}).limit(100))


# Get all CAPA records
@app.get("/capa")
def get_capa():
    return list(db.capa_records.find({}, {"_id": 0}).limit(100))
# Get material consumption records
@app.get("/material-consumption")
def get_material_consumption():
    return list(
        db.material_consumption.find({}, {"_id": 0}).limit(100)
    )

# Get all BOM records
@app.get("/bom")
def get_bom():
    return list(db.bom.find({}, {"_id": 0}).limit(100))


# Get all inspection plans
@app.get("/inspection-plans")
def get_inspection_plans():
    return list(db.inspection_plans.find({}, {"_id": 0}).limit(100))

# End-to-end manufacturing traceability investigation
@app.get("/traceability/{defect_id}")
def traceability_investigation(defect_id: str):

    defect = db.defect_records.find_one(
        {"defect_id": defect_id}, {"_id": 0}
    )

    if not defect:
        return {"error": "Defect ID not found"}

    inspection = db.inspection_results.find_one(
        {"inspection_id": defect.get("inspection_id")},
        {"_id": 0}
    )

    order_id = defect.get("order_id") or (
        inspection.get("order_id") if inspection else None
    )

    order = db.production_orders.find_one(
        {"order_id": order_id}, {"_id": 0}
    ) if order_id else None

    product = db.products.find_one(
        {"product_id": order.get("product_id")}, {"_id": 0}
    ) if order else None

    consumptions = list(
        db.material_consumption.find(
            {"order_id": order_id}, {"_id": 0}
        )
    ) if order_id else []

    materials = []

    for consumption in consumptions:
        lot = db.material_lots.find_one(
            {"lot_id": consumption.get("lot_id")}, {"_id": 0}
        )

        supplier = db.suppliers.find_one(
            {"supplier_id": lot.get("supplier_id")}, {"_id": 0}
        ) if lot else None

        materials.append({
            "consumption": consumption,
            "material_lot": lot,
            "supplier": supplier
        })

    steps = list(
        db.process_steps.find(
            {"order_id": order_id}, {"_id": 0}
        )
    ) if order_id else []

    machine_details = []

    for step in steps:
        machine = db.machines.find_one(
            {"machine_id": step.get("machine_id")}, {"_id": 0}
        )

        machine_details.append({
            "process_step": step,
            "machine": machine
        })

    capas = list(
        db.capa_records.find(
            {"defect_id": defect_id}, {"_id": 0}
        )
    )

    return {
        "defect": defect,
        "inspection": inspection,
        "production_order": order,
        "product": product,
        "materials_and_suppliers": materials,
        "machines_and_process_steps": machine_details,
        "corrective_actions": capas
    }



# Dashboard collection counts
@app.get("/dashboard/counts")
def get_dashboard_counts():
    return {
        "products": db.products.count_documents({}),
        "suppliers": db.suppliers.count_documents({}),
        "material_lots": db.material_lots.count_documents({}),
        "production_orders": db.production_orders.count_documents({}),
        "inspection_results": db.inspection_results.count_documents({}),
        "machines": db.machines.count_documents({}),
        "process_steps": db.process_steps.count_documents({}),
        "defect_records": db.defect_records.count_documents({}),
        "capa_records": db.capa_records.count_documents({}),
        "material_consumption": db.material_consumption.count_documents({})
    }

from fastapi import HTTPException
from pydantic import BaseModel, Field


class MaterialConsumptionInput(BaseModel):
    consumption_id: str
    order_id: str
    lot_id: str
    product_id: str
    quantity_consumed: float = Field(gt=0)


@app.post("/validate/material-consumption")
def validate_material_consumption(data: MaterialConsumptionInput):

    order = db.production_orders.find_one({
        "order_id": data.order_id
    })

    if not order:
        raise HTTPException(404, "Production order does not exist")

    if order.get("product_id") != data.product_id:
        raise HTTPException(400, "Product does not match production order")

    lot = db.material_lots.find_one({
        "lot_id": data.lot_id
    })

    if not lot:
        raise HTTPException(404, "Material lot does not exist")

    if lot.get("status", "").lower() in {
        "blocked", "quarantine", "inactive", "rejected"
    }:
        raise HTTPException(400, "Material lot is not available")

    already_consumed = db.material_consumption.aggregate([
        {"$match": {"lot_id": data.lot_id}},
        {"$group": {
            "_id": None,
            "total": {"$sum": "$quantity_consumed"}
        }}
    ])

    previous = list(already_consumed)
    used = previous[0]["total"] if previous else 0

    received = float(lot.get("quantity_received", 0))

    if used + data.quantity_consumed > received:
        raise HTTPException(400, "Material lot stock exceeded")

    if db.material_consumption.find_one({
        "consumption_id": data.consumption_id
    }):
        raise HTTPException(409, "Consumption ID already exists")

    return {
        "message": "Material consumption validation successful",
        "valid": True
    }

class BOMValidationInput(BaseModel):
    order_id: str


@app.post("/validate/bom-consumption")
@app.post("/validate/bom-consumption")
def validate_bom_consumption(data: BOMValidationInput):
    order = db.production_orders.find_one(
        {"order_id": data.order_id}
    )

    if not order:
        raise HTTPException(404, "Production order not found")

    product_id = order.get("product_id")
    ordered_qty = float(order.get("quantity_ordered", 0))

    bom_items = list(db.bom.find({"product_id": product_id}))

    if not bom_items:
        raise HTTPException(404, "BOM not found for product")

    missing_materials = []

    for item in bom_items:
        material_name = item.get("material_name")
        required_qty = (
            float(item.get("quantity_required", 0)) * ordered_qty
        )

        lots = list(db.material_lots.find(
            {"material_name": material_name},
            {"_id": 0, "lot_id": 1}
        ))

        lot_ids = [lot["lot_id"] for lot in lots]

        consumed = sum(
            float(record.get("quantity_consumed", 0))
            for record in db.material_consumption.find({
                "order_id": data.order_id,
                "lot_id": {"$in": lot_ids}
            })
        )

        if consumed < required_qty:
            missing_materials.append({
                "material": material_name,
                "required": required_qty,
                "consumed": consumed,
                "shortage": required_qty - consumed
            })

    return {
        "order_id": data.order_id,
        "valid": len(missing_materials) == 0,
        "missing_materials": missing_materials
    }
class CAPAClosureInput(BaseModel):
    status: str
    verified: bool


@app.post("/validate/capa-closure")
def validate_capa_closure(data: CAPAClosureInput):

    if data.status.lower() in ["closed", "completed"] and not data.verified:
        raise HTTPException(
            status_code=400,
            detail="CAPA cannot be closed before verification"
        )

    return {
        "valid": True,
        "message": "CAPA closure validation successful"
    }
class DefectQuantityInput(BaseModel):
    inspection_id: str
    defect_quantity: int = Field(gt=0)


@app.post("/validate/defect-quantity")
def validate_defect_quantity(data: DefectQuantityInput):

    inspection = db.inspection_results.find_one(
        {"inspection_id": data.inspection_id}
    )

    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")

    inspected = int(inspection.get("inspected_quantity", 0))

    if data.defect_quantity > inspected:
        raise HTTPException(
            status_code=400,
            detail="Defect quantity cannot exceed inspected quantity"
        )

    return {
        "valid": True,
        "message": "Defect quantity validation successful"
    }
@app.get("/validate/traceability/{defect_id}")
def validate_traceability(defect_id: str):

    defect = db.defect_records.find_one({"defect_id": defect_id})

    if not defect:
        raise HTTPException(
            status_code=404,
            detail="Broken traceability: Defect record not found"
        )

    order = db.production_orders.find_one(
        {"order_id": defect.get("order_id")}
    )

    if not order:
        raise HTTPException(
            status_code=400,
            detail="Broken traceability: Production order not found"
        )

    inspection = db.inspection_results.find_one(
        {"inspection_id": defect.get("inspection_id")}
    )

    if not inspection:
        raise HTTPException(
            status_code=400,
            detail="Broken traceability: Inspection record not found"
        )

    return {"valid": True, "message": "Traceability links are valid"}