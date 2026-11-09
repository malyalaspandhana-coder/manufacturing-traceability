
const API_URL = "http://127.0.0.1:8000";

async function loadProducts() {
    const table = document.getElementById("products-table");
    const status = document.getElementById("page-status");

    try {
        const response = await fetch(`${API_URL}/products`);

        if (!response.ok) {
            throw new Error("Unable to load products");
        }

        const products = await response.json();

        table.innerHTML = "";

        products.forEach(product => {
            const row = document.createElement("tr");

            [
                product.product_id,
                product.product_name,
                product.category,
                product.status
            ].forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value ?? "-";
                row.appendChild(cell);
            });

            table.appendChild(row);
        });

        status.textContent = `Loaded ${products.length} products successfully.`;

    } catch (error) {
        table.innerHTML =
            '<tr><td colspan="4">Failed to load products.</td></tr>';
        status.textContent = error.message;
    }
}

loadProducts();
