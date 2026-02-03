import "./styles/main.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { updateBoxes } from "./overview/boxes.js"
import { createChart } from "./overview/chart.js"
import { createChartRevenuesPerDay } from "./overview/chart.js";
import { createChartTransactionsPourcentage } from "./overview/chart.js";
import { createTable  } from "./overview/table.js";
import { createPaymentsTable } from "./payments/payments.js";
import { setupFormProvider } from "./settings/settings.js";
import { checkProviderState } from "./settings/checkProviderState.js";
import { updateBoxTransactions } from "./analytics/analytics.js";
import { syncProviders } from "./analytics/sync.js";

const api_url = 'http://localhost:8080/dashboard/overview'

const page = document.body.dataset.page;

if (page === "overview") {
    updateBoxes(api_url);
    
    createChart();
    
    createTable()
}

if (page === "payments") {
    
    let page = 1;
    const limit = 15;
    let start = 0;
    let end = 0;

    const periodStartSelect = document.getElementById("start");
    periodStartSelect.addEventListener("change", () => {
        if (periodStartSelect.value === "")
            start = 0
        else
            start = periodStartSelect.value
    })

    document.getElementById("apply-btn").addEventListener("click", () => {
        createPaymentsTable(page, limit, start);
    })

    createPaymentsTable(page, limit, start);
    
    document.getElementById("next").addEventListener("click", () => {
        if (page >= 1) {
            page++;
            createPaymentsTable(page, limit, start);
            console.log(page);
        }
    });
    
    document.getElementById("prev").addEventListener("click", () => {
        if (page > 1) {
            page--;
            createPaymentsTable(page, limit, start);
            console.log(page);
        }
    });
}

if (page === "analytics") {
    let start = 0
    const providerSelect = document.getElementById("provider");
    const applyBtn = document.getElementById("apply-btn")
    const syncBtn = document.getElementById("sync-btn");

    applyBtn.addEventListener("click", () => {
        if (!providerSelect.value)
            return ;

        let providers = [];

        if (providerSelect.value === "all") {
            providers = ["mollie", "stripe"];
        }
        else {
            providers = [providerSelect.value]
        }
    })

    providerSelect.addEventListener("change", () => {
        if (providerSelect.value === "") {
            syncBtn.disabled = true;
        } else {
            syncBtn.disabled = false;

            let providers = [];

            if (providerSelect.value === "all") {
                providers = ["mollie", "stripe"];
            }
            else {
                providers = [providerSelect.value]
            }
            createChartRevenuesPerDay(providers)
            createChartTransactionsPourcentage(providers)
            updateBoxTransactions("http://localhost:8080/dashboard/transactions", providers, start)
        }
    })

    syncBtn.addEventListener("click", async () => {
        await syncProviders(providerSelect, syncBtn);

        let providers = [];

        if (providerSelect.value === "all") {
            providers = ["mollie", "stripe"];
        }
        else {
            providers = [providerSelect.value]
        }

        updateBoxTransactions("http://localhost:8080/dashboard/transactions", providers)
    })
}

if (page === "settings") {
    const stripe_state = await checkProviderState("stripe", "http://localhost:8080/settings/provider/status")
    const mollie_state = await checkProviderState("mollie", "http://localhost:8080/settings/provider/status")

    if (!stripe_state)
        setupFormProvider("stripe", "http://localhost:8080/settings/key/add");
    if (!mollie_state)
        setupFormProvider("mollie", "http://localhost:8080/settings/key/add");
}