
const API_URL = "http://127.0.0.1:8000";

async function loadProductionOrders() {
    const table = document.getElementById("production-orders-table");

    try {
        const response = await fetch(`${API_URL}/production-orders`);

        if (!response.ok) {
            throw new Error("Failed to load production orders");
        }

        const orders = await response.json();
        table.innerHTML = "";

        orders.forEach(order => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${order.order_id ?? ""}</td>
                <td>${order.product_id ?? ""}</td>
                <td>${order.quantity_ordered ?? ""}</td>
                <td>${order.status ?? ""}</td>
            `;

            table.appendChild(row);
        });

    } catch (error) {
        table.innerHTML =
            `<tr><td colspan="4">${error.message}</td></tr>`;
        console.error(error);
    }
}

loadProductionOrders();
