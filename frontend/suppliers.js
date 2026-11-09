
const API_URL = "http://127.0.0.1:8000";

async function loadSuppliers() {
    const table = document.getElementById("suppliers-table");
    const status = document.getElementById("page-status");

    try {
        const response = await fetch(`${API_URL}/suppliers`);

        if (!response.ok) {
            throw new Error("Unable to load suppliers");
        }

        const suppliers = await response.json();

        table.innerHTML = "";

        suppliers.forEach(supplier => {
            const row = document.createElement("tr");

            [
                supplier.supplier_id,
                supplier.supplier_name,
                supplier.location,
                supplier.status
            ].forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value ?? "-";
                row.appendChild(cell);
            });

            table.appendChild(row);
        });

        status.textContent =
            `Loaded ${suppliers.length} suppliers successfully.`;

    } catch (error) {
        table.innerHTML =
            '<tr><td colspan="4">Failed to load suppliers.</td></tr>';
        status.textContent = error.message;
    }
}

loadSuppliers();
