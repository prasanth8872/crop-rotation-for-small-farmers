/**
 * Weather visualization and data fetching functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize weather chart if container exists
    const weatherChartContainer = document.getElementById('weather-chart');
    if (weatherChartContainer) {
        initWeatherChart();
    }

    // Weather forecast if container exists
    const forecastContainer = document.getElementById('weather-forecast');
    if (forecastContainer) {
        loadWeatherForecast();
    }
});

/**
 * Initialize weather history chart
 */
function initWeatherChart() {
    const ctx = document.getElementById('weather-chart').getContext('2d');
    
    // Sample data for demonstration - in a real app, this would come from the API
    const labels = [];
    const tempData = [];
    const humidityData = [];
    
    // Generate labels for last 7 days
    for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }));
        
        // Generate realistic temperature data for Coimbatore (20-35°C)
        tempData.push(Math.floor(Math.random() * (35 - 20 + 1)) + 20);
        
        // Generate realistic humidity data for Coimbatore (40-90%)
        humidityData.push(Math.floor(Math.random() * (90 - 40 + 1)) + 40);
    }
    
    // Create chart
    const weatherChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: tempData,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    yAxisID: 'y'
                },
                {
                    label: 'Humidity (%)',
                    data: humidityData,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Weather Trends - Past 7 Days',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                if (context.datasetIndex === 0) {
                                    label += context.parsed.y + '°C';
                                } else {
                                    label += context.parsed.y + '%';
                                }
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    },
                    min: 15,
                    max: 40,
                    grid: {
                        drawOnChartArea: false
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Humidity (%)'
                    },
                    min: 0,
                    max: 100,
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

/**
 * Load weather forecast data
 */
function loadWeatherForecast() {
    const forecastContainer = document.getElementById('weather-forecast');
    if (!forecastContainer) return;
    
    // In a real app, this would fetch data from a weather API
    // For now, generate realistic forecast data for Coimbatore
    
    const forecasts = [];
    const today = new Date();
    
    // Generate 5-day forecast
    for (let i = 1; i <= 5; i++) {
        const date = new Date(today);
        date.setDate(date.getDate() + i);
        
        // Coimbatore typical weather range
        const minTemp = Math.floor(Math.random() * (25 - 18 + 1)) + 18;
        const maxTemp = Math.floor(Math.random() * (38 - 28 + 1)) + 28;
        
        // Weather conditions probabilities based on season
        const month = date.getMonth() + 1;
        let conditions;
        
        if (month in [12, 1, 2]) { // Winter (dry)
            conditions = getRandomWeighted(['Clear', 'Partly Cloudy', 'Cloudy', 'Light Rain'], [50, 30, 15, 5]);
        } else if (month in [3, 4, 5]) { // Summer (hot)
            conditions = getRandomWeighted(['Clear', 'Partly Cloudy', 'Cloudy', 'Light Rain'], [60, 25, 10, 5]);
        } else if (month in [6, 7, 8, 9]) { // Monsoon
            conditions = getRandomWeighted(['Rain', 'Heavy Rain', 'Thunderstorm', 'Cloudy', 'Partly Cloudy'], [30, 20, 15, 25, 10]);
        } else { // Post-monsoon
            conditions = getRandomWeighted(['Partly Cloudy', 'Cloudy', 'Clear', 'Light Rain'], [35, 25, 30, 10]);
        }
        
        forecasts.push({
            date: date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }),
            conditions: conditions,
            minTemp: minTemp,
            maxTemp: maxTemp,
            icon: getWeatherIcon(conditions)
        });
    }
    
    // Create forecast HTML
    let forecastHTML = `
        <h4 class="mb-3">5-Day Forecast for Coimbatore</h4>
        <div class="row">
    `;
    
    forecasts.forEach(function(forecast) {
        forecastHTML += `
            <div class="col">
                <div class="card text-center">
                    <div class="card-body p-2">
                        <h5 class="card-title">${forecast.date}</h5>
                        <img src="https://openweathermap.org/img/wn/${forecast.icon}@2x.png" alt="${forecast.conditions}" width="50">
                        <p class="card-text">${forecast.conditions}</p>
                        <p class="card-text">
                            <span class="text-primary">${forecast.maxTemp}°C</span> / 
                            <span class="text-secondary">${forecast.minTemp}°C</span>
                        </p>
                    </div>
                </div>
            </div>
        `;
    });
    
    forecastHTML += `
        </div>
    `;
    
    forecastContainer.innerHTML = forecastHTML;
}

/**
 * Get weather icon code based on condition
 * @param {string} condition - Weather condition
 * @returns {string} - Icon code for OpenWeatherMap icons
 */
function getWeatherIcon(condition) {
    switch(condition.toLowerCase()) {
        case 'clear':
            return '01d';
        case 'partly cloudy':
            return '02d';
        case 'cloudy':
            return '03d';
        case 'light rain':
            return '10d';
        case 'rain':
            return '09d';
        case 'heavy rain':
            return '09d';
        case 'thunderstorm':
            return '11d';
        default:
            return '01d';
    }
}

/**
 * Get random element from array with weighted probabilities
 * @param {Array} items - Array of items to choose from
 * @param {Array} weights - Array of weights corresponding to items
 * @returns {*} - Randomly selected item based on weights
 */
function getRandomWeighted(items, weights) {
    // Normalize weights
    const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);
    const normalizedWeights = weights.map(weight => weight / totalWeight);
    
    // Calculate cumulative weights
    const cumulativeWeights = [];
    let sum = 0;
    
    for (let weight of normalizedWeights) {
        sum += weight;
        cumulativeWeights.push(sum);
    }
    
    // Generate random number and find corresponding item
    const random = Math.random();
    
    for (let i = 0; i < cumulativeWeights.length; i++) {
        if (random <= cumulativeWeights[i]) {
            return items[i];
        }
    }
    
    // Fallback (should never happen with properly normalized weights)
    return items[0];
}
