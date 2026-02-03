export async function updateBoxes(api_url) {
    let revenues = document.getElementById("revenues")
    let transactions = document.getElementById("transactions-succeeded")
    let last_sync = document.getElementById("last_sync")

    try {
        const response = await fetch(api_url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                hours: 72
            })
        });
        const data = await response.json();

        const rev = data.revenues;
        const currencies = Object.keys(rev);
        const transactions_data = data.transactions;
        const last_sync_data = data.last_sync;

        let html = "";
        const obj = Object.entries(rev); // Passer de {} a []
        for (const [currency, value] of obj) {
            html += `<div>${currency.toUpperCase()}: ${value / 100}<div>`
        }

        revenues.innerHTML = html;
        transactions.textContent = transactions_data
        const date = new Date(last_sync_data)
        last_sync.textContent = date.toLocaleDateString('en-GB', {
            hour: '2-digit',
            minute: '2-digit'
        });

    } catch (err) {
        console.error(err);
    }
    
}