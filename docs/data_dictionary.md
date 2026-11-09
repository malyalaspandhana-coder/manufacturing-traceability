# Manufacturing Traceability Data Dictionary

## 1. Product
- product_id: Unique product ID (SKU format)
- product_name: Product name
- category: Product category
- status: Active or Inactive

## 2. Supplier
- supplier_id: Unique supplier ID
- supplier_name: Supplier name
- location: Supplier location
- status: Active or Inactive

## 3. BOM
- bom_id: Unique BOM ID
- product_id: Reference to Product
- material_name: Raw material name
- required_quantity: Required material quantity

## 4. MaterialLot
- lot_id: Unique material lot ID
- supplier_id: Reference to Supplier
- material_name: Material name
- received_quantity: Quantity received
- received_date: Date received

## 5. ProductionOrder
- order_id: Unique production order ID
- product_id: Reference to Product
- planned_quantity: Production quantity
- status: Order status

## 6. Machine
- machine_id: Unique machine ID
- machine_name: Machine name
- machine_type: Machine category
- status: Machine status

## 7. ProcessStep
- step_id: Unique process step ID
- order_id: Reference to ProductionOrder
- machine_id: Reference to Machine
- step_name: Manufacturing step

## 8. InspectionPlan
- plan_id: Unique inspection plan ID
- product_id: Reference to Product
- inspection_type: Type of inspection

## 9. InspectionResult
- inspection_id: Unique inspection ID
- order_id: Reference to ProductionOrder
- inspected_quantity: Quantity inspected
- defect_quantity: Defective quantity
- result: Pass or Fail

## 10. Defect
- defect_id: Unique defect ID
- inspection_id: Reference to InspectionResult
- lot_id: Reference to MaterialLot
- defect_type: Type of defect
- severity: Low, Medium or High

## 11. CorrectiveAction
- capa_id: Unique corrective action ID
- defect_id: Reference to Defect
- action_description: Corrective action
- status: Open, In Progress or Closed
- verified: True or False

## 12. Relationships

- Product 1:N BOM
- Product 1:N ProductionOrder
- Supplier 1:N MaterialLot
- ProductionOrder 1:N ProcessStep
- Machine 1:N ProcessStep
- ProductionOrder 1:N InspectionPlan
- InspectionPlan 1:N InspectionResult
- MaterialLot 1:N ProductionOrder (through lot consumption records)
- MaterialLot 1:N Defect
- ProductionOrder 1:N Defect
- ProcessStep 1:N Defect
- Defect 1:N CorrectiveAction

## 13. Validation Rules

1. All primary keys must be unique.
2. Every foreign key must reference an existing record.
3. Consumed quantity must not exceed received quantity.
4. Defective quantity must not exceed inspected quantity.
5. End date must not be earlier than start date.
6. Defects must reference valid production records.
7. Corrective actions cannot close before verification.
8. Historical events must never be overwritten.
9. All generated IDs must follow the required naming convention.
10. Derived values must be calculated from source records.
