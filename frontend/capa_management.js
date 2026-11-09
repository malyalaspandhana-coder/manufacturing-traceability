
const API_BASE = "http://127.0.0.1:8000";

async function loadCAPA() {
    const table = document.getElementById("capa-table");
    const status = document.getElementById("capa-status");

    try {
        const response = await fetch(`${API_BASE}/capa`);

        if (!response.ok) {
            throw new Error("Unable to fetch CAPA records");
        }

        const records = await response.json();

        table.innerHTML = "";

        records.forEach(item => {
            const row = document.createElement("tr");

            const values = [
                item.capa_id,
                item.defect_id,
                item.order_id || "N/A",
                item.root_cause,
                item.corrective_action,
                item.preventive_action,
                item.status
            ];

            values.forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value ?? "N/A";
                row.appendChild(cell);
            });

            table.appendChild(row);
        });

        status.textContent = `Loaded ${records.length} CAPA records.`;

    } catch (error) {
        status.textContent = "Error loading CAPA records. Check the backend server.";
        console.error(error);
    }
}

loadCAPA();
