export async function checkProviderState(provider, api_url) {
    const status = document.getElementById(`${provider}-status-message`);
    const form = document.getElementById(`${provider}-form`);

    try {
        const response = await fetch(api_url, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'                
            },
            body: JSON.stringify({
                provider: provider
            })
        })
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
        }
        const data = await response.json();

        if (data === true) {
            status.textContent = "Connected"
            status.className = "provider-status-message success";
            form.classList.add("hidden");

            return (true)
        }

        return (false)
    } catch (err){
        console.error(err)
    }
    
}