
const API_URL = "http://127.0.0.1:8000";

async function loadDashboard() {
    try {
        const productResponse = await fetch(`${API_URL}/products`);
        const supplierResponse = await fetch(`${API_URL}/suppliers`);
        const machineResponse = await fetch(`${API_URL}/machines`);
const processResponse = await fetch(`${API_URL}/process-steps`);
const defectResponse = await fetch(`${API_URL}/defects`);
const capaResponse = await fetch(`${API_URL}/capa`);

        if (
    !productResponse.ok ||
    !supplierResponse.ok ||
    !machineResponse.ok ||
    !processResponse.ok ||
    !defectResponse.ok ||
    !capaResponse.ok
) {
    throw new Error("API request failed");
}
        const products = await productResponse.json();
        const suppliers = await supplierResponse.json();
        
// ===== PRODUCT CATEGORY CHART =====

const categoryCounts = {};

products.forEach(product => {
    const category = product.category || "Other";
    categoryCounts[category] = (categoryCounts[category] || 0) + 1;
});

const categoryCanvas = document.getElementById("categoryChart");

if (window.categoryChartInstance) {
    window.categoryChartInstance.destroy();
}

window.categoryChartInstance = new Chart(categoryCanvas, {
    type: "doughnut",
    data: {
        labels: Object.keys(categoryCounts),
        datasets: [{
            data: Object.values(categoryCounts),
            backgroundColor: [
                "#2563eb",
                "#06b6d4",
                "#14b8a6",
                "#f59e0b",
                "#8b5cf6",
                "#ec4899"
            ],
            borderWidth: 3,
            borderColor: "#ffffff",
            hoverOffset: 10
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: "bottom"
            }
        }
    }
});

// ===== SUPPLIER STATUS CHART =====

const supplierCounts = {};

suppliers.forEach(supplier => {
    const status = supplier.status || "Unknown";
    supplierCounts[status] = (supplierCounts[status] || 0) + 1;
});

const supplierCanvas = document.getElementById("supplierChart");

if (window.supplierChartInstance) {
    window.supplierChartInstance.destroy();
}

window.supplierChartInstance = new Chart(supplierCanvas, {
    type: "bar",
    data: {
        labels: Object.keys(supplierCounts),
        datasets: [{
            label: "Number of Suppliers",
            data: Object.values(supplierCounts),
            backgroundColor: ["#0ea5e9", "#14b8a6", "#f59e0b"],
            borderRadius: 8
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    precision: 0
                }
            }
        }
    }
});

        // Display Products
const productTable = document.getElementById("products-table");

productTable.innerHTML = products.map(product => `
    <tr>
        <td>${product.product_id || "-"}</td>
        <td>${product.product_name || "-"}</td>
        <td>${product.category || "-"}</td>
    </tr>
`).join("");

// Display Suppliers
const supplierTable = document.getElementById("suppliers-table");

supplierTable.innerHTML = suppliers.map(supplier => `
    <tr>
        <td>${supplier.supplier_id || "-"}</td>
        <td>${supplier.supplier_name || "-"}</td>
        <td>${supplier.location || "-"}</td>
        <td>${supplier.status || "-"}</td>
    </tr>
`).join("");

        // Get actual counts from MongoDB
const countResponse = await fetch(`${API_URL}/dashboard/counts`);

if (!countResponse.ok) {
    throw new Error("Dashboard counts API failed");
}

const counts = await countResponse.json();

// Update dashboard cards
document.getElementById("products").textContent = counts.products;
document.getElementById("suppliers").textContent = counts.suppliers;
document.getElementById("inspections").textContent = counts.inspection_results;
document.getElementById("machines").textContent = counts.machines;
document.getElementById("process-steps").textContent = counts.process_steps;
document.getElementById("defects").textContent = counts.defect_records;
document.getElementById("capa").textContent = counts.capa_records;
document.getElementById("material-consumption").textContent = counts.material_consumption;

document.getElementById("status").textContent = "Connected";

    } catch (error) {
        document.getElementById("status").textContent =
            "Connection Failed";

        console.error(error);
    }
}

loadDashboard();
