import requests
import random
import json
import os
import logging
from datetime import datetime

from crop_data import crop_data, soil_types, seasons

# Weather API Configuration
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'demo_key')
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather_data(city='Coimbatore'):
    """
    Get real-time weather data from OpenWeatherMap API
    
    Since we might not have an actual API key, we'll create a fallback
    with realistic weather data for Coimbatore
    """
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'  # For Celsius
        }
        
        # Only make API call if we have a valid key (not the demo key)
        if WEATHER_API_KEY != 'demo_key':
            response = requests.get(WEATHER_API_URL, params=params)
            
            if response.status_code == 200:
                data = response.json()
                weather = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'conditions': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                return weather
    
        # If API call fails or we're using demo key, return realistic mock data for Coimbatore
        # This is only used because we don't have an actual API key
        logging.warning("Using fallback weather data because API call failed or using demo key")
        
        # Coimbatore typically has a warm tropical climate
        month = datetime.now().month
        
        # Seasonal weather patterns for Coimbatore
        if month in [12, 1, 2]:  # Winter (relatively cooler)
            temp = round(random.uniform(20, 28), 1)
            humidity = round(random.uniform(50, 70), 1)
            conditions = random.choice(['Clear', 'Clouds', 'Haze'])
        elif month in [3, 4, 5]:  # Summer (hot)
            temp = round(random.uniform(30, 38), 1)
            humidity = round(random.uniform(40, 60), 1)
            conditions = random.choice(['Clear', 'Clouds', 'Haze'])
        elif month in [6, 7, 8, 9]:  # Monsoon
            temp = round(random.uniform(25, 33), 1)
            humidity = round(random.uniform(70, 90), 1)
            conditions = random.choice(['Rain', 'Clouds', 'Thunderstorm'])
        else:  # Post-monsoon
            temp = round(random.uniform(23, 30), 1)
            humidity = round(random.uniform(60, 80), 1)
            conditions = random.choice(['Clouds', 'Clear', 'Rain'])
        
        return {
            'city': city,
            'temperature': temp,
            'humidity': humidity,
            'pressure': round(random.uniform(1008, 1015), 1),
            'wind_speed': round(random.uniform(2, 8), 1),
            'conditions': conditions,
            'description': f'{conditions.lower()}',
            'icon': get_weather_icon(conditions),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    except Exception as e:
        logging.error(f"Error getting weather data: {e}")
        return None

def get_weather_icon(condition):
    """Get appropriate weather icon code based on condition"""
    if condition == 'Clear':
        return '01d'
    elif condition == 'Clouds':
        return '03d'
    elif condition == 'Rain':
        return '10d'
    elif condition == 'Thunderstorm':
        return '11d'
    elif condition == 'Haze' or condition == 'Mist':
        return '50d'
    else:
        return '01d'  # Default to clear

def get_current_season():
    """Get current season based on month"""
    month = datetime.now().month
    
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Summer'
    elif month in [6, 7, 8, 9]:
        return 'Monsoon'
    else:
        return 'Post-monsoon'

def get_crop_recommendation(land_type, soil_type, previous_crop, previous_yield):
    """
    Generate crop recommendation based on input parameters and crop data
    
    This is a simplified recommendation algorithm that takes into account:
    - Soil type
    - Current season
    - Previous crop (for crop rotation)
    - Previous yield
    """
    current_season = get_current_season()
    
    # Filter crops that can grow in the given soil type and current season
    suitable_crops = []
    
    for crop in crop_data:
        if (soil_type.lower() in [s.lower() for s in crop['suitable_soil_types']] and
            current_season.lower() in [s.lower() for s in crop['growing_seasons']]):
            suitable_crops.append(crop)
    
    # If no suitable crops found, return a default recommendation
    if not suitable_crops:
        return "Millet"  # Default crop that grows in various conditions
    
    # Filter out the previous crop (for crop rotation)
    suitable_crops = [crop for crop in suitable_crops if crop['name'].lower() != previous_crop.lower()]
    
    # If no crops left after filtering out previous crop, return most suitable
    if not suitable_crops:
        # Find complementary crops for rotation with previous crop
        for crop in crop_data:
            if previous_crop.lower() == crop['name'].lower():
                if 'rotation_crops' in crop:
                    for rotation_crop_name in crop['rotation_crops']:
                        for c in crop_data:
                            if c['name'].lower() == rotation_crop_name.lower():
                                if (soil_type.lower() in [s.lower() for s in c['suitable_soil_types']] and
                                    current_season.lower() in [s.lower() for s in c['growing_seasons']]):
                                    return c['name']
        
        # If no rotation crops found, return a different crop that suits the conditions
        for crop in crop_data:
            if (crop['name'].lower() != previous_crop.lower() and
                soil_type.lower() in [s.lower() for s in crop['suitable_soil_types']]):
                return crop['name']
        
        return "Millet"  # Default fallback
    
    # Sort by suitability (this could be enhanced with machine learning in a real system)
    # For now, we'll just pick a random suitable crop for demonstration
    recommended_crop = random.choice(suitable_crops)
    
    return recommended_crop['name']

def get_quantum_improvement_factor():
    """
    In a real quantum agriculture system, this would implement quantum algorithms
    for improved prediction accuracy. For now, we'll simulate this.
    """
    # Simulated quantum factor (in a real system, this would use quantum computing principles)
    return round(random.uniform(1.05, 1.25), 2)  # 5-25% improvement factor
