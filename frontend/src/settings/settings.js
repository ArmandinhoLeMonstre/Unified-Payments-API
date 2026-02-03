export async function setupFormProvider(provider, api_url) {
    const form = document.getElementById(`${provider}-form`);
    const api_key = document.getElementById(`${provider}-api-key`);
    const status = document.getElementById(`${provider}-status-message`);

    if (!form)
        return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); 

        try {
            const response = await fetch(api_url, {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    provider: provider,
                    api_key: api_key.value
                })
            });
            api_key.value = "";

            if (!response.ok) {
                status.className = "provider-status-message error";
                throw new Error(`HTTP error ${response.status}`);
            }
            status.className = "provider-status-message success";
            form.classList.add("hidden");
            const data = await response.json();
            status.textContent = `${provider} has been added`;

        } catch(err) {
            console.error(err)
            status.textContent = err.message;
        }
    })
}