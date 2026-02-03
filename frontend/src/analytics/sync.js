export async function syncProviders(providerSelect, syncBtn) {
    const sync_message = document.getElementById("sync-message")
    sync_message.classList.remove("success", "error", "hidden");

    const provider = providerSelect.value
    if (!provider)
        return ;

    let provider_tab;

    if (provider === "all"){
        provider_tab = ["stripe", "mollie"];
    }
    else {
        provider_tab = [provider]
    }
    
    syncBtn.disabled = true;
    syncBtn.innerHTML = `<i class="fa-solid fa-rotate fa-spin"></i> Syncing...`;

    try {
        const res = await fetch("http://localhost:8080/sync/", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                providers: provider_tab
            })
        })

        const data = await res.json()

        syncBtn.disabled = false;
        syncBtn.innerHTML = `<i class="fa-solid fa-rotate"></i> Sync`;

        if (!res.ok) {
            sync_message.classList.add("error");
            const message = data?.detail || `Sync failed (HTTP ${response.status})`;
            sync_message.textContent = message
            throw new Error("Sync failed");
        }

        console.log("here")

        sync_message.classList.add("success");
        sync_message.textContent = `${provider_tab} updated`

    } catch (err) {
        console.error(err);
    }
}
