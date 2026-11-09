
const API_URL = "http://127.0.0.1:8000";

async function loadInspections() {
    const table = document.getElementById("inspection-table");
    const status = document.getElementById("inspection-status");

    try {
        const response = await fetch(`${API_URL}/inspections`);

        if (!response.ok) {
            throw new Error("Unable to load inspection records");
        }

        const inspections = await response.json();

        table.innerHTML = "";

        if (inspections.length === 0) {
            table.innerHTML =
                '<tr><td colspan="5">No inspection records found.</td></tr>';
            status.textContent = "No records available.";
            return;
        }

        inspections.forEach((item) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${item.inspection_id ?? ""}</td>
                <td>${item.order_id ?? ""}</td>
                <td>${item.inspected_quantity ?? 0}</td>
                <td>${item.defect_quantity ?? 0}</td>
                <td>${item.result ?? ""}</td>
            `;

            table.appendChild(row);
        });

        status.textContent =
            `Loaded ${inspections.length} inspection records successfully.`;

    } catch (error) {
        table.innerHTML =
            '<tr><td colspan="5">Failed to load inspection records.</td></tr>';

        status.textContent = error.message;
        console.error(error);
    }
}

loadInspections();
