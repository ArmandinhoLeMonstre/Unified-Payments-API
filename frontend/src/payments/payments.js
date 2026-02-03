function formatDate(isoString) {
  const d = new Date(isoString);
  return d.toLocaleString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function shortId(id) {
  if (id.length <= 12) return id;
  return id.slice(0, 6) + "…" + id.slice(-6);
}

export async function createPaymentsTable(page, limit, start) {
 
    try {
        const offset = (page - 1) * limit;
        let url = `http://localhost:8080/dashboard/payments?limit=${limit}&offset=${offset}`
        if (start > 0) {
            const param = `&start=${start}`
            url += param
        }
        const response = await fetch(url);
        const data = await response.json();
        const tbody = document.getElementById("table-body");
        tbody .innerHTML = "";
        data.forEach(element => {
            const row = document.createElement("tr");

            const obj = Object.entries(element);
            let html = "";
            for (const [key, value] of obj) {
                if (key === "status") {
                    html += `
                        <td>
                            <span class="status-badge status-${value}">
                                ${value}
                            </span>
                        </td>
                    `;
                }
                else if (key === "provider") {
                html += `
                    <td>
                    <span class="provider-badge provider-${value}">
                        ${value}
                    </span>
                    </td>
                `;
                }
                else if (key === "provider_id") {
                    html += `<td>${shortId(value)}</td>`
                }
                else if (key === "created_at") {
                    html += `<td>${formatDate(value)}</td>`
                }
                else if (key === "amount") {
                    const amount = value / 100;
                    const currency = element.currency;
                    html += `<td>${amount.toFixed(2)} ${currency.toUpperCase()}</td>`;
                }
                else if (key === "currency") {
                    continue ;
                }
                else
                    html += `<td>${value}</td>`
            }

            row.innerHTML = html;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error(err);
        }
}