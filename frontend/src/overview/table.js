export async function createTable() {

    try {
        const response = await fetch("http://localhost:8080/dashboard/payments?limit=5&offset=0");
        const data = await response.json();
        const tbody = document.getElementById("table-body");
        data.forEach(element => {
            const row = document.createElement("tr");

            const obj = Object.entries(element);
            let html = "";
            for (const [key, value] of obj) {
                html += `<td>${value}</td>`
            }

            row.innerHTML = html;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error(err);
        }
        
}