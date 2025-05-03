/**
 * Charts and visualization functionality for the application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize soil moisture chart if container exists
    const moistureChartContainer = document.getElementById('soil-moisture-chart');
    if (moistureChartContainer) {
        initSoilMoistureChart();
    }
    
    // Initialize crop yield comparison chart if container exists
    const yieldChartContainer = document.getElementById('crop-yield-chart');
    if (yieldChartContainer) {
        initCropYieldChart();
    }
    
    // Initialize soil nutrient chart if container exists
    const nutrientChartContainer = document.getElementById('soil-nutrient-chart');
    if (nutrientChartContainer) {
        initSoilNutrientChart();
    }
    
    // Initialize admin dashboard charts if container exists
    if (document.getElementById('admin-user-chart')) {
        initAdminUserChart();
    }
    
    if (document.getElementById('admin-query-chart')) {
        initAdminQueryChart();
    }
});

/**
 * Initialize soil moisture chart
 */
function initSoilMoistureChart() {
    const ctx = document.getElementById('soil-moisture-chart').getContext('2d');
    
    // Get farm ID from data attribute
    const farmId = document.getElementById('soil-moisture-chart').getAttribute('data-farm-id');
    
    if (farmId) {
        // Fetch soil moisture data from API
        fetch(`/api/soil-data/${farmId}`)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    createSoilMoistureChart(ctx, data);
                } else {
                    showChartError('soil-moisture-chart', 'No soil moisture data available');
                }
            })
            .catch(error => {
                console.error('Error fetching soil moisture data:', error);
                showChartError('soil-moisture-chart', 'Error loading soil moisture data');
            });
    } else {
        // Use sample data for demonstration
        const sampleData = generateSampleSoilMoistureData();
        createSoilMoistureChart(ctx, sampleData);
    }
}

/**
 * Create soil moisture chart with provided data
 * @param {CanvasRenderingContext2D} ctx - Canvas rendering context
 * @param {Array} data - Soil moisture data
 */
function createSoilMoistureChart(ctx, data) {
    // Extract data for chart
    const labels = data.map(d => new Date(d.recorded_at).toLocaleDateString());
    const moistureData = data.map(d => d.moisture_level);
    
    // Create chart
    const moistureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Soil Moisture (%)',
                    data: moistureData,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Soil Moisture Levels',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Moisture: ${context.parsed.y}%`;
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
                    title: {
                        display: true,
                        text: 'Moisture Level (%)'
                    },
                    min: 0,
                    max: 100
                }
            }
        }
    });
}

/**
 * Generate sample soil moisture data for demonstration
 * @returns {Array} - Sample soil moisture data
 */
function generateSampleSoilMoistureData() {
    const data = [];
    const today = new Date();
    
    for (let i = 9; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        
        // Generate realistic soil moisture values (20-80%)
        const moisture = Math.floor(Math.random() * (80 - 20 + 1)) + 20;
        
        data.push({
            moisture_level: moisture,
            recorded_at: date.toISOString()
        });
    }
    
    return data;
}

/**
 * Initialize crop yield comparison chart
 */
function initCropYieldChart() {
    const ctx = document.getElementById('crop-yield-chart').getContext('2d');
    
    // Sample data for demonstration - in a real app, this would come from the database
    const cropData = [
        { name: 'Rice', actual_yield: 6200, expected_yield: 7000 },
        { name: 'Sugarcane', actual_yield: 92000, expected_yield: 95000 },
        { name: 'Cotton', actual_yield: 2100, expected_yield: 2300 },
        { name: 'Maize', actual_yield: 5600, expected_yield: 6000 },
        { name: 'Groundnut', actual_yield: 1900, expected_yield: 2000 }
    ];
    
    // Extract data for chart
    const labels = cropData.map(d => d.name);
    const actualYieldData = cropData.map(d => d.actual_yield);
    const expectedYieldData = cropData.map(d => d.expected_yield);
    
    // Create chart
    const yieldChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Actual Yield (kg/hectare)',
                    data: actualYieldData,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Expected Yield (kg/hectare)',
                    data: expectedYieldData,
                    backgroundColor: 'rgba(255, 159, 64, 0.6)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Crop Yield Comparison',
                    font: {
                        size: 16
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Crop'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Yield (kg/hectare)'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

/**
 * Initialize soil nutrient chart
 */
function initSoilNutrientChart() {
    const ctx = document.getElementById('soil-nutrient-chart').getContext('2d');
    
    // Sample data for demonstration - in a real app, this would come from the database
    const nutrientData = {
        nitrogen: 72,
        phosphorus: 45,
        potassium: 68,
        ph: 6.5,
        organic_matter: 58
    };
    
    // Create chart
    const nutrientChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Nitrogen', 'Phosphorus', 'Potassium', 'pH Balance', 'Organic Matter'],
            datasets: [
                {
                    label: 'Current Levels',
                    data: [
                        nutrientData.nitrogen,
                        nutrientData.phosphorus,
                        nutrientData.potassium,
                        nutrientData.ph * 10, // Scale pH (typically 0-14) to match other metrics (0-100)
                        nutrientData.organic_matter
                    ],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(54, 162, 235, 1)',
                    pointRadius: 5
                },
                {
                    label: 'Optimal Levels',
                    data: [80, 60, 75, 70, 65], // Optimal values for comparison
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                    pointRadius: 5
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Soil Nutrient Analysis',
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
                            if (context.parsed.r !== null) {
                                if (context.label === 'pH Balance') {
                                    // Convert scaled pH value back to normal range
                                    label += (context.parsed.r / 10).toFixed(1);
                                } else {
                                    label += context.parsed.r + '%';
                                }
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }
        }
    });
}

/**
 * Initialize admin user registration chart
 */
function initAdminUserChart() {
    const ctx = document.getElementById('admin-user-chart').getContext('2d');
    
    // Sample data for demonstration - in a real app, this would come from the database
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const userData = [5, 8, 12, 15, 20, 18, 22, 25, 28, 30, 32, 35];
    
    // Create chart
    const userChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                {
                    label: 'User Registrations',
                    data: userData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'User Registrations This Year',
                    font: {
                        size: 16
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Month'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Number of Users'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

/**
 * Initialize admin query statistics chart
 */
function initAdminQueryChart() {
    const ctx = document.getElementById('admin-query-chart').getContext('2d');
    
    // Sample data for demonstration - in a real app, this would come from the database
    const queryData = {
        soilTypes: {
            'Red Soil': 45,
            'Black Soil': 30,
            'Alluvial Soil': 15,
            'Sandy Soil': 25,
            'Clay Soil': 20,
            'Loamy Soil': 35
        }
    };
    
    // Extract data for chart
    const labels = Object.keys(queryData.soilTypes);
    const data = Object.values(queryData.soilTypes);
    
    // Generate colors for each soil type
    const backgroundColors = [
        'rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)',
        'rgba(255, 159, 64, 0.6)'
    ];
    
    // Create chart
    const queryChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Queries by Soil Type',
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: backgroundColors.map(color => color.replace('0.6', '1')),
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Queries by Soil Type',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

/**
 * Show error message when chart cannot be loaded
 * @param {string} containerId - ID of the chart container
 * @param {string} message - Error message to display
 */
function showChartError(containerId, message) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    // Create canvas to maintain layout
    const canvas = document.createElement('canvas');
    container.innerHTML = '';
    container.appendChild(canvas);
    
    // Draw error message on canvas
    const ctx = canvas.getContext('2d');
    canvas.width = container.offsetWidth;
    canvas.height = container.offsetHeight;
    
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.font = '16px Arial';
    ctx.fillStyle = '#dc3545';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(message, canvas.width / 2, canvas.height / 2);
}
