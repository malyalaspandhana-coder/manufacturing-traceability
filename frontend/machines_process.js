
const API_URL = "http://127.0.0.1:8000";

async function loadMachines() {
    const table = document.getElementById("machines-table");

    try {
        const response = await fetch(`${API_URL}/machines`);

        if (!response.ok) {
            throw new Error("Failed to load machines");
        }

        const machines = await response.json();
        table.innerHTML = "";

        machines.forEach(machine => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${machine.machine_id ?? ""}</td>
                <td>${machine.machine_name ?? ""}</td>
                <td>${machine.machine_type ?? ""}</td>
                <td>${machine.status ?? ""}</td>
            `;

            table.appendChild(row);
        });

    } catch (error) {
        table.innerHTML =
            `<tr><td colspan="4">${error.message}</td></tr>`;
    }
}

async function loadProcessSteps() {
    const table = document.getElementById("process-steps-table");

    try {
        const response = await fetch(`${API_URL}/process-steps`);

        if (!response.ok) {
            throw new Error("Failed to load process steps");
        }

        const steps = await response.json();
        table.innerHTML = "";

        steps.forEach(step => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${step.process_step_id ?? ""}</td>
                <td>${step.order_id ?? ""}</td>
                <td>${step.machine_id ?? ""}</td>
                <td>${step.step_name ?? ""}</td>
                <td>${step.status ?? ""}</td>
            `;

            table.appendChild(row);
        });

    } catch (error) {
        table.innerHTML =
            `<tr><td colspan="5">${error.message}</td></tr>`;
    }
}

loadMachines();
loadProcessSteps();
