// JavaScript for analysis page

document.addEventListener('DOMContentLoaded', function() {
    // Initialize chart toggles
    const chartToggles = document.querySelectorAll('.chart-toggle');
    chartToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.dataset.target;
            const targetChart = document.getElementById(targetId);
            
            if (targetChart) {
                targetChart.classList.toggle('d-none');
                this.textContent = targetChart.classList.contains('d-none') ? 
                    'Show Chart' : 'Hide Chart';
            }
        });
    });

    // Initialize interactive elements
    if (typeof Chart !== 'undefined') {
        initInteractiveCharts();
    }
});

function initInteractiveCharts() {
    // Sample interactive chart - price trends over time
    const priceTrendCtx = document.getElementById('priceTrendChart');
    if (priceTrendCtx) {
        const days = Array.from({length: 30}, (_, i) => i + 1);
        const prices = days.map(day => 10000 + Math.random() * 15000 - (day * 200));
        
        new Chart(priceTrendCtx, {
            type: 'line',
            data: {
                labels: days,
                datasets: [{
                    label: 'Average Price (₹)',
                    data: prices,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Days Before Departure'
                        },
                        reverse: true
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Price (₹)'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Price: ₹${context.raw.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Sample interactive chart - price distribution by airline
    const airlinePriceCtx = document.getElementById('airlinePriceChart');
    if (airlinePriceCtx) {
        const airlines = ['Vistara', 'Air India', 'Indigo', 'SpiceJet', 'AirAsia'];
        const prices = airlines.map(() => 5000 + Math.random() * 20000);
        
        new Chart(airlinePriceCtx, {
            type: 'bar',
            data: {
                labels: airlines,
                datasets: [{
                    label: 'Average Price (₹)',
                    data: prices,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Price (₹)'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Average: ₹${context.raw.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });
    }
}