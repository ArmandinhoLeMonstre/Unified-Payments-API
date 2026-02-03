export async function updateBoxTransactions(api_url, providers, start) {
    let transactions_succeeded = document.getElementById("transactions-succeeded")
    let transactions_pending = document.getElementById("transactions-pending")
    let transactions_failed = document.getElementById("transactions-failed")
    let transactions_requires_actions = document.getElementById("transactions-requires-action")

    let duration = start / 24;

    try {
        const response = await fetch (api_url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                providers: providers,
                statuses: ["succeeded", "pending", "failed", "requires_action"],
                hours: 720
            })
        });

        if (!response.ok) {
            console.error("HTTP error", response.status);
            return;
        }
        const data = await response.json();

        let total_succeeded = 0;
        let total_failed = 0;
        let total_pending = 0;
        let total_requires_action = 0;

        for (const provider of providers) {
            const succeeded = data?.transactions?.[provider]?.succeeded ?? 0;
            total_succeeded += succeeded

            const failed = data?.transactions?.[provider]?.failed ?? 0;
            total_failed += failed

            const pending = data?.transactions?.[provider]?.pending ?? 0;
            total_pending += pending

            const requires_action = data?.transactions?.[provider]?.requires_action ?? 0;
            total_requires_action += requires_action
        }
        
        transactions_succeeded.textContent = total_succeeded;
        transactions_pending.textContent = total_pending;
        transactions_failed.textContent = total_failed;
        transactions_requires_actions.textContent = total_requires_action;
    } catch (err) {
        console.error(err);
    }
}