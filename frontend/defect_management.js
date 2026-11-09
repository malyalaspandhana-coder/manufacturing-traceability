
const API_URL = "http://127.0.0.1:8000";

async function loadDefects() {
    const table = document.getElementById("defect-table");
    const status = document.getElementById("defect-status");

    try {
        const response = await fetch(`${API_URL}/defects`);

        if (!response.ok) {
            throw new Error("Failed to fetch defect records");
        }

        const defects = await response.json();

        table.innerHTML = "";

        if (defects.length === 0) {
            table.innerHTML =
                '<tr><td colspan="7">No defect records found.</td></tr>';
        } else {
            defects.forEach(defect => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${defect.defect_id ?? ""}</td>
                    <td>${defect.inspection_id ?? ""}</td>
                    <td>${defect.order_id ?? ""}</td>
                    <td>${defect.defect_type ?? ""}</td>
                    <td>${defect.severity ?? ""}</td>
                    <td>${defect.defect_quantity ?? ""}</td>
                    <td>${defect.status ?? ""}</td>
                `;

                table.appendChild(row);
            });
        }

        status.textContent =
            `Loaded ${defects.length} defect records successfully.`;

    } catch (error) {
        table.innerHTML =
            '<tr><td colspan="7">Failed to load defect records.</td></tr>';

        status.textContent = error.message;
        console.error(error);
    }
}

loadDefects();
