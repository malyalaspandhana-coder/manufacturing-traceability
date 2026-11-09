
const API_BASE = "http://127.0.0.1:8000";

async function loadMaterialConsumption() {
    const table = document.getElementById("consumption-table");
    const status = document.getElementById("consumption-status");

    try {
        const response = await fetch(`${API_BASE}/material-consumption`);

        if (!response.ok) {
            throw new Error("Unable to fetch material consumption");
        }

        const records = await response.json();

        table.innerHTML = "";

        records.forEach(item => {
            const row = document.createElement("tr");

            const values = [
                item.consumption_id,
                item.order_id,
                item.lot_id,
                item.product_id,
                item.quantity_consumed
            ];

            values.forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value ?? "N/A";
                row.appendChild(cell);
            });

            table.appendChild(row);
        });

        status.textContent = `Loaded ${records.length} records.`;

    } catch (error) {
        status.textContent = "Unable to load records. Check the backend server.";
        console.error(error);
    }
}

loadMaterialConsumption();
