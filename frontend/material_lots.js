
const API_URL = "http://127.0.0.1:8000";

async function loadMaterialLots() {
    const table = document.getElementById("material-lots-table");

    try {
        const response = await fetch(`${API_URL}/material-lots`);

        if (!response.ok) {
            throw new Error("Failed to load material lots");
        }

        const lots = await response.json();
        table.innerHTML = "";

        lots.forEach(lot => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${lot.lot_id ?? ""}</td>
                <td>${lot.supplier_id ?? ""}</td>
                <td>${lot.material_name ?? ""}</td>
                <td>${lot.quantity_received ?? ""}</td>
                <td>${lot.status ?? ""}</td>
            `;

            table.appendChild(row);
        });

    } catch (error) {
        table.innerHTML =
            `<tr><td colspan="5">${error.message}</td></tr>`;
        console.error(error);
    }
}

loadMaterialLots();
