/**
 * Main JavaScript file for Quantum Precision Agriculture Application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Auto-hide alert messages after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            const alertInstance = new bootstrap.Alert(alert);
            alertInstance.close();
        });
    }, 5000);

    // Submit confirmation for forms with data-confirm attribute
    const formsWithConfirm = document.querySelectorAll('form[data-confirm]');
    formsWithConfirm.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            const confirmMessage = this.getAttribute('data-confirm');
            if (!confirm(confirmMessage)) {
                event.preventDefault();
            }
        });
    });

    // Enable location access if element exists
    const locationButton = document.getElementById('get-location');
    if (locationButton) {
        locationButton.addEventListener('click', function() {
            getLocation();
        });
    }

    // Handle mobile navigation
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            document.body.classList.toggle('nav-open');
        });
    }

    // Initialize date pickers for date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // Flatpickr or other date picker could be initialized here
        // We're keeping it simple with native date inputs
    });

    // Implement custom file input display
    const fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'No file chosen';
            const label = e.target.nextElementSibling;
            if (label) {
                label.textContent = fileName;
            }
        });
    });

    // Load weather data on homepage
    if (document.getElementById('weather-widget')) {
        loadWeatherData();
    }
});

/**
 * Get user's current location
 */
function getLocation() {
    const locationDisplay = document.getElementById('location-display');
    const locationSpinner = document.getElementById('location-spinner');
    
    if (locationSpinner) locationSpinner.style.display = 'inline-block';
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            // Success callback
            function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                
                if (locationDisplay) {
                    locationDisplay.innerHTML = `Latitude: ${lat.toFixed(6)}, Longitude: ${lng.toFixed(6)}`;
                }
                
                // You can use the coordinates to fetch location-specific data
                // For example, get weather data for this location
                // Or find nearby farms, soil data, etc.
                
                if (locationSpinner) locationSpinner.style.display = 'none';
                
                // Store coordinates in hidden inputs if they exist
                const latInput = document.getElementById('latitude');
                const lngInput = document.getElementById('longitude');
                
                if (latInput) latInput.value = lat;
                if (lngInput) lngInput.value = lng;
                
                // Show success message
                showAlert('Location detected successfully!', 'success');
            },
            // Error callback
            function(error) {
                if (locationSpinner) locationSpinner.style.display = 'none';
                
                let errorMessage;
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = "User denied the request for geolocation.";
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = "Location information is unavailable.";
                        break;
                    case error.TIMEOUT:
                        errorMessage = "The request to get user location timed out.";
                        break;
                    case error.UNKNOWN_ERROR:
                        errorMessage = "An unknown error occurred when trying to get location.";
                        break;
                }
                
                if (locationDisplay) {
                    locationDisplay.innerHTML = `Error: ${errorMessage}`;
                }
                
                showAlert(errorMessage, 'danger');
            }
        );
    } else {
        if (locationSpinner) locationSpinner.style.display = 'none';
        
        const errorMessage = "Geolocation is not supported by this browser.";
        
        if (locationDisplay) {
            locationDisplay.innerHTML = `Error: ${errorMessage}`;
        }
        
        showAlert(errorMessage, 'danger');
    }
}

/**
 * Show alert message
 * @param {string} message - Alert message
 * @param {string} type - Alert type (success, danger, warning, info)
 */
function showAlert(message, type = 'info') {
    const alertsContainer = document.getElementById('alerts-container');
    if (!alertsContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertsContainer.appendChild(alert);
    
    // Auto dismiss after 5 seconds
    setTimeout(function() {
        const alertInstance = new bootstrap.Alert(alert);
        alertInstance.close();
    }, 5000);
}

/**
 * Load weather data for the weather widget
 */
function loadWeatherData() {
    const weatherWidget = document.getElementById('weather-widget');
    if (!weatherWidget) return;
    
    const city = weatherWidget.getAttribute('data-city') || 'Coimbatore';
    
    // Show loading spinner
    weatherWidget.innerHTML = `
        <div class="text-center p-4">
            <div class="spinner-border text-light" role="status">
                <span class="visually-hidden">Loading weather data...</span>
            </div>
            <p class="mt-2 mb-0">Loading weather data...</p>
        </div>
    `;
    
    // Fetch weather data from API
    fetch(`/api/weather?city=${encodeURIComponent(city)}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.city) {
                // Update weather widget with data
                weatherWidget.innerHTML = `
                    <div class="weather-info">
                        <div>
                            <div class="weather-temp">${Math.round(data.temperature)}°C</div>
                            <div class="weather-city">${data.city}</div>
                            <div class="weather-condition">${data.conditions}</div>
                        </div>
                        <div class="weather-details">
                            <p><i class="bi bi-droplet-fill"></i> Humidity: ${data.humidity}%</p>
                            <p><i class="bi bi-wind"></i> Wind: ${data.wind_speed} km/h</p>
                            <p><i class="bi bi-clock"></i> Updated: ${new Date(data.timestamp).toLocaleTimeString()}</p>
                        </div>
                    </div>
                `;
            } else {
                weatherWidget.innerHTML = `
                    <div class="text-center p-3">
                        <i class="bi bi-exclamation-triangle" style="font-size: 2rem;"></i>
                        <p class="mt-2 mb-0">Unable to load weather data</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            weatherWidget.innerHTML = `
                <div class="text-center p-3">
                    <i class="bi bi-exclamation-triangle" style="font-size: 2rem;"></i>
                    <p class="mt-2 mb-0">Error loading weather data</p>
                </div>
            `;
        });
}
