
const API_BASE = "http://127.0.0.1:8000";

function createCard(title, data) {
    const card = document.createElement("div");
    card.className = "trace-card";

    const heading = document.createElement("h4");
    heading.textContent = title;
    card.appendChild(heading);

    if (!data || (Array.isArray(data) && data.length === 0)) {
        const empty = document.createElement("p");
        empty.textContent = "No related records found.";
        card.appendChild(empty);
        return card;
    }

    const records = Array.isArray(data) ? data : [data];

    records.forEach(record => {
        Object.entries(record).forEach(([key, value]) => {
            const row = document.createElement("p");
            const label = document.createElement("strong");

            label.textContent =
                key.replaceAll("_", " ").replace(/\b\w/g, c => c.toUpperCase()) + ": ";

            row.appendChild(label);

            if (value && typeof value === "object") {
    const nested = document.createElement("div");
    nested.className = "nested-details";

    Object.entries(value).forEach(([nestedKey, nestedValue]) => {
        const detail = document.createElement("p");

        detail.textContent =
            nestedKey.replaceAll("_", " ").replace(/\b\w/g, c => c.toUpperCase())
            + ": " + (nestedValue ?? "N/A");

        nested.appendChild(detail);
    });

    row.appendChild(nested);
} else {
    row.appendChild(document.createTextNode(value ?? "N/A"));
}

            card.appendChild(row);
        });
    });

    return card;
}

function showSection(elementId, title, data) {
    const container = document.getElementById(elementId);
    container.innerHTML = "";
    container.appendChild(createCard(title, data));
}

async function investigateDefect() {
    const defectId = document.getElementById("defect-id").value.trim();
    const status = document.getElementById("trace-status");
    const results = document.getElementById("trace-results");

    if (!defectId) {
        status.textContent = "Please enter a Defect ID.";
        results.style.display = "none";
        return;
    }

    status.textContent = "Investigating defect...";
    results.style.display = "none";

    try {
        const response = await fetch(
            `${API_BASE}/traceability/${encodeURIComponent(defectId)}`
        );

        const data = await response.json();

        if (!response.ok || data.error) {
            throw new Error(data.error || "Investigation failed.");
        }

        showSection("defect-details", "Defect Information", data.defect);
        showSection("inspection-details", "Inspection Information", data.inspection);
        showSection("order-details", "Production Order and Product", {
            production_order: data.production_order,
            product: data.product
        });
        showSection("material-details", "Material Lots and Suppliers", data.materials_and_suppliers);
        showSection("machine-details", "Machines and Process Steps", data.machines_and_process_steps);
        showSection("capa-details", "Corrective and Preventive Actions", data.corrective_actions);

        results.style.display = "block";
        status.textContent = "Investigation completed successfully.";

    } catch (error) {
        status.textContent = error.message;
        console.error(error);
    }
}
