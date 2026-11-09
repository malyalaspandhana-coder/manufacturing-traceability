# YottaFlex Manufacturing Traceability System

## Project Overview
A web-based manufacturing traceability system for monitoring production orders, material consumption, suppliers, quality inspections, defects and corrective actions.

## Technologies
- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI
- Database: MongoDB
- API testing: Swagger UI

## Project Structure
- `backend/app/` — Backend application and validation scripts
- `frontend/` — Web pages and JavaScript
- `data/generated/` — Generated project datasets
- `data/backup/` — Data backups
- `docs/` — Project documentation

## How to Run

### 1. Start MongoDB
Ensure MongoDB is running locally.

### 2. Start the backend
From the project root, activate the virtual environment and run:

```powershell
python -m uvicorn main:app --reload --app-dir backend/app
```

### 3. Open API documentation
Visit: http://127.0.0.1:8000/docs

### 4. Start the frontend
Open another terminal:

```powershell
cd frontend
python -m http.server 5500
```

Visit: http://127.0.0.1:5500/

## Main Features
- Product and supplier management
- Material lot tracking
- Production order management
- Machine and process tracking
- Quality inspection and defect management
- CAPA management
- Material consumption tracking
- End-to-end defect traceability

## Documentation
Refer to `docs/Final_Project_Documentation.md` for the project documentation.
