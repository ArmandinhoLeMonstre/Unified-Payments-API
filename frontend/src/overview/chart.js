import Chart from 'chart.js/auto'

export async function createChart() {
  try {
    const response = await fetch("http://localhost:8080/charts")
    const data = await response.json()

    const keys = Object.keys(data.chart);
    const values = Object.values(data.chart);

    new Chart(
      document.getElementById('myChart'),
      {
        type: 'line',
        data: {
          labels: keys,
          datasets: [
            {
              label: 'Transactions per day',
              data: values
            }
          ]
        }
      }
    );
  } catch (err) {
    console.log(err);
  }
};

let revenuesChart = null;

export async function createChartRevenuesPerDay(providers) {
  try {

    let query = "";
    providers.forEach(provider => {
    	if (query.length === 0) {
			query += `?providers=${provider}`;
		} else {
			query += `&providers=${provider}`;
		}
    })
    const response = await fetch(`http://localhost:8080/charts/revenues${query}`)
    const data = await response.json()

    const dates = Object.keys(data);

    let total_eur = [];
    let total_usd = [];

    dates.forEach(date => {
      const amount_eur = data[date]?.eur
      if (amount_eur) {
        total_eur.push(amount_eur)
      } else {
        total_eur.push(0)
      }
      const amount_usd = data[date]?.usd
      if (amount_usd) {
        total_usd.push(amount_usd)
      } else {
        total_usd.push(0)
      }

    });
	if (revenuesChart) {
		revenuesChart.destroy()
	}
    revenuesChart = new Chart(
      document.getElementById('chart-revenues'),
      {
        type: 'bar',
        data: {
          labels: dates,
          datasets: [
            {
              label: 'Dollars',
              data: total_usd
            },
            {
              label: 'Euro',
              data: total_eur
            }
          ]
        },
		options: {
			responsive: true,
			maintainAspectRatio: false, 
			}
      }
    );
  } catch (err) {
    console.log(err);
  }
};

let transactionsChart = null

export async function createChartTransactionsPourcentage(providers) {
  try {
    const response = await fetch ("http://localhost:8080/dashboard/transactions", {
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
		let transactions = data.transactions
		console.log(transactions)
		const keys = ["succeeded", "pending", "failed", "requires_action"]
		let values = []

		const totals = {
			succeeded: 0,
			pending: 0,
			failed: 0,
			requires_action: 0
		};
	
		providers.map(provider => {
			console.log(transactions[provider])

			keys.forEach(status => {
				const count = transactions[provider]?.[status] ?? 0;
				totals[status] += count;
			})

			values = Object.values(transactions[provider])
			// console.log(transactions[provider].succeeded)
		})
		const final = Object.values(totals)
		console.log(final)

		if (transactionsChart) {
			transactionsChart.destroy()
		}
		transactionsChart = new Chart(
		document.getElementById('chart-transactions'), {
		type: "pie",
		data: {
			labels: keys,
			datasets: [{
			data: final
			}]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false, 
			}
		});
  } catch (err) {
    console.log(err);
  }
};