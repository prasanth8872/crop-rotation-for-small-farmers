/**
 * Crop recommendation and rotation functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize crop rotation visualization if container exists
    const rotationContainer = document.getElementById('crop-rotation-visualization');
    if (rotationContainer) {
        initCropRotationVisualization();
    }
    
    // Handle crop recommendation form
    const recommendationForm = document.getElementById('crop-recommendation-form');
    if (recommendationForm) {
        recommendationForm.addEventListener('submit', function(event) {
            // Form is handled server-side, no need to prevent default
            
            // Show loading indicator
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = `
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    Processing...
                `;
            }
        });
    }
    
    // Handle quantum optimization toggle
    const quantumToggle = document.getElementById('quantum-optimization');
    if (quantumToggle) {
        quantumToggle.addEventListener('change', function() {
            const quantumInfo = document.getElementById('quantum-info');
            if (quantumInfo) {
                if (this.checked) {
                    quantumInfo.style.display = 'block';
                } else {
                    quantumInfo.style.display = 'none';
                }
            }
        });
    }
    
    // Crop details expansion
    const cropDetailsBtns = document.querySelectorAll('.crop-details-btn');
    cropDetailsBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const detailsElement = document.getElementById(targetId);
            
            if (detailsElement) {
                if (detailsElement.style.display === 'none' || !detailsElement.style.display) {
                    detailsElement.style.display = 'block';
                    this.innerHTML = 'Show Less <i class="bi bi-chevron-up"></i>';
                } else {
                    detailsElement.style.display = 'none';
                    this.innerHTML = 'Show More <i class="bi bi-chevron-down"></i>';
                }
            }
        });
    });
});

/**
 * Initialize crop rotation visualization
 */
function initCropRotationVisualization() {
    const container = document.getElementById('crop-rotation-visualization');
    if (!container) return;
    
    // Sample data for demonstration - in a real app, this would come from the database
    const rotationData = [
        { season: 'Season 1', crop: 'Rice', icon: '🌾' },
        { season: 'Season 2', crop: 'Pulses', icon: '🌱' },
        { season: 'Season 3', crop: 'Vegetables', icon: '🥬' },
        { season: 'Season 4', crop: 'Groundnut', icon: '🥜' }
    ];
    
    // Create visualization
    let html = `
        <h4 class="mb-4">Recommended Crop Rotation Cycle</h4>
        <div class="crop-rotation-cycle">
    `;
    
    rotationData.forEach(function(item, index) {
        html += `
            <div class="crop-rotation-item">
                <div class="crop-rotation-icon">${item.icon}</div>
                <div class="crop-rotation-label">${item.season}</div>
                <div class="crop-rotation-name">${item.crop}</div>
                ${index < rotationData.length - 1 ? '<div class="crop-rotation-arrow">→</div>' : ''}
            </div>
        `;
    });
    
    html += `
        </div>
        <div class="crop-rotation-note mt-3">
            <p class="text-muted"><i class="bi bi-info-circle"></i> Crop rotation improves soil health, reduces pests and diseases, and increases yield sustainability.</p>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Add CSS for the visualization
    const style = document.createElement('style');
    style.textContent = `
        .crop-rotation-cycle {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            margin-bottom: 2rem;
        }
        
        .crop-rotation-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0 10px;
            position: relative;
        }
        
        .crop-rotation-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background-color: rgba(14, 138, 77, 0.1);
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid var(--primary-color);
        }
        
        .crop-rotation-label {
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.25rem;
        }
        
        .crop-rotation-name {
            font-weight: 600;
        }
        
        .crop-rotation-arrow {
            position: absolute;
            right: -30px;
            top: 30px;
            font-size: 1.5rem;
            color: var(--accent-color);
        }
        
        @media (max-width: 768px) {
            .crop-rotation-cycle {
                flex-direction: column;
            }
            
            .crop-rotation-item {
                margin: 15px 0;
            }
            
            .crop-rotation-arrow {
                position: absolute;
                right: 50%;
                top: 100%;
                transform: translateX(50%) rotate(90deg);
            }
        }
    `;
    
    document.head.appendChild(style);
}

/**
 * Calculate suitability score for a crop based on soil type and weather
 * @param {string} cropName - Name of the crop
 * @param {string} soilType - Type of soil
 * @param {Object} weather - Weather data
 * @returns {number} - Suitability score (0-100)
 */
function calculateCropSuitability(cropName, soilType, weather) {
    // This would be a complex algorithm in a real app
    // For demonstration, we'll return a random score between 60 and 100
    return Math.floor(Math.random() * (100 - 60 + 1)) + 60;
}

/**
 * Generate quantum-enhanced crop recommendations
 * This is a simulated function for demonstration purposes
 * In a real quantum agriculture system, this would use quantum algorithms
 * @param {Object} params - Input parameters
 * @returns {Array} - Enhanced crop recommendations
 */
function generateQuantumEnhancedRecommendations(params) {
    // Simulate quantum enhancement factor (5-25% improvement)
    const quantumFactor = 1 + Math.random() * 0.2;
    
    // Sample crops with enhanced scores
    return [
        { name: 'Rice', score: Math.min(100, Math.floor(85 * quantumFactor)) },
        { name: 'Maize', score: Math.min(100, Math.floor(78 * quantumFactor)) },
        { name: 'Cotton', score: Math.min(100, Math.floor(72 * quantumFactor)) },
        { name: 'Groundnut', score: Math.min(100, Math.floor(68 * quantumFactor)) },
        { name: 'Pulses', score: Math.min(100, Math.floor(65 * quantumFactor)) }
    ];
}
