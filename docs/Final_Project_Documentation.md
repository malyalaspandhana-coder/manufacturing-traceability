# YottaFlex Manufacturing Traceability System

## 1. Introduction
The YottaFlex Manufacturing Traceability System is designed to track manufacturing activities, material consumption, quality inspections, defects and corrective actions. It provides end-to-end traceability from a defect to its inspection result, production order, consumed material lots and suppliers.

## 2. Problem Statement
Manufacturing organisations need accurate tracking of materials, production activities and quality issues. Disconnected records make it difficult to identify the source of defects, trace affected materials and monitor corrective actions.

This project addresses these challenges through a centralised manufacturing traceability system.

## 3. Objectives
- Maintain product, supplier and material lot records.
- Track production orders and manufacturing process steps.
- Record material consumption against production orders.
- Monitor inspection results and defects.
- Track corrective and preventive actions (CAPA).
- Trace defects back to consumed material lots and suppliers.
- Validate relationships and quantities across records.

## 4. Technologies Used
- Frontend: HTML, CSS and JavaScript.
- Backend: Python and FastAPI.
- Database: MongoDB.
- API testing: Swagger UI.
- Development environment: Visual Studio Code.

## 5. System Modules
1. Product Management
2. Supplier Management
3. Material Lot Management
4. Production Order Management
5. Machine and Process Management
6. Quality Inspection Management
7. Defect Management
8. CAPA Management
9. Material Consumption Management
10. Traceability Investigation
11. Dashboard and Reporting

## 6. Database Design
The system contains the following core entities:

Product, BOM, Supplier, MaterialLot, ProductionOrder, Machine, ProcessStep, InspectionPlan, InspectionResult, Defect, CorrectiveAction and MaterialConsumption.

These entities are connected through identifiers and relationships to maintain traceability.

## 7. Traceability Workflow
Defect → Inspection Result → Production Order → Material Consumption → Material Lot → Supplier.

The system also connects production orders to process steps and machines, and defects to corrective actions.

## 8. Validation and Business Rules
- Validate unique record identifiers.
- Check that referenced records exist.
- Prevent material consumption from exceeding received quantity.
- Ensure defect quantity does not exceed inspected quantity.
- Check production order and product consistency.
- Prevent CAPA closure before verification.
- Detect broken traceability relationships.
- Preserve historical manufacturing records.

## 9. API and Testing
The backend exposes REST API endpoints through FastAPI. Swagger UI is used to inspect and test API operations.

Validation scenarios include:
- Nonexistent material lot.
- BOM material not fully consumed.
- CAPA closure without verification.
- Defect quantity exceeding inspected quantity.
- Broken traceability relationship.

## 10. Frontend
The web interface provides pages for dashboard monitoring, products, suppliers, material lots, production orders, machines, inspections, defects, CAPA, material consumption and traceability investigation.

## 11. Expected Outcomes
- Centralised manufacturing information.
- Improved material and supplier traceability.
- Easier defect investigation.
- Better monitoring of inspection and corrective actions.
- Improved data consistency through validation.

## 12. Future Enhancements
- Role-based user authentication.
- Real-time alerts for quality issues.
- Advanced analytics and reporting.
- Barcode or QR-code-based material tracking.
- Integration with enterprise manufacturing systems.

## 13. Conclusion
The YottaFlex Manufacturing Traceability System provides a structured approach to managing manufacturing records and investigating quality issues. By connecting production, materials, suppliers, inspections and corrective actions, it supports better visibility and accountability across the manufacturing process.

