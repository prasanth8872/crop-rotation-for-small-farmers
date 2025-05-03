# This file contains crop data, soil types, and season information for the application

# Soil types commonly found in Coimbatore region
soil_types = [
    'Red Soil',
    'Black Soil',
    'Alluvial Soil',
    'Sandy Soil',
    'Clay Soil',
    'Loamy Soil'
]

# Seasons in Tamil Nadu/Coimbatore
seasons = [
    'Winter',     # Dec-Feb
    'Summer',     # Mar-May
    'Monsoon',    # Jun-Sep
    'Post-monsoon'  # Oct-Nov
]

# Comprehensive crop data for the Coimbatore region
crop_data = [
    {
        'name': 'Rice',
        'scientific_name': 'Oryza sativa',
        'description': 'Major staple food crop in Coimbatore. Requires plenty of water and is typically grown in wetlands or irrigated fields.',
        'suitable_soil_types': ['Alluvial Soil', 'Clay Soil', 'Loamy Soil'],
        'growing_seasons': ['Monsoon', 'Winter'],
        'growth_duration': '90-150 days',
        'water_requirements': 'High',
        'nutrition_requirements': {
            'nitrogen': 'High',
            'phosphorus': 'Medium',
            'potassium': 'Medium'
        },
        'optimal_temperature': '20-35°C',
        'average_yield': '6000-7500 kg/hectare',
        'rotation_crops': ['Pulses', 'Groundnut', 'Vegetables']
    },
    {
        'name': 'Sugarcane',
        'scientific_name': 'Saccharum officinarum',
        'description': 'Important cash crop in Coimbatore. The region has multiple sugar factories processing sugarcane.',
        'suitable_soil_types': ['Loamy Soil', 'Clay Soil', 'Alluvial Soil'],
        'growing_seasons': ['Winter', 'Summer'],
        'growth_duration': '10-12 months',
        'water_requirements': 'High',
        'nutrition_requirements': {
            'nitrogen': 'High',
            'phosphorus': 'Medium',
            'potassium': 'High'
        },
        'optimal_temperature': '20-35°C',
        'average_yield': '80000-100000 kg/hectare',
        'rotation_crops': ['Pulses', 'Vegetables']
    },
    {
        'name': 'Cotton',
        'scientific_name': 'Gossypium hirsutum',
        'description': 'Major commercial crop in Coimbatore. The region is known for textile industries using cotton.',
        'suitable_soil_types': ['Black Soil', 'Red Soil', 'Alluvial Soil'],
        'growing_seasons': ['Monsoon', 'Post-monsoon'],
        'growth_duration': '150-180 days',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'Medium',
            'phosphorus': 'Medium',
            'potassium': 'High'
        },
        'optimal_temperature': '20-30°C',
        'average_yield': '1500-2500 kg/hectare',
        'rotation_crops': ['Pulses', 'Cereals']
    },
    {
        'name': 'Maize',
        'scientific_name': 'Zea mays',
        'description': 'Important cereal crop in Coimbatore used for both human consumption and as animal feed.',
        'suitable_soil_types': ['Loamy Soil', 'Sandy Soil', 'Red Soil'],
        'growing_seasons': ['Winter', 'Monsoon'],
        'growth_duration': '90-120 days',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'High',
            'phosphorus': 'Medium',
            'potassium': 'Medium'
        },
        'optimal_temperature': '20-30°C',
        'average_yield': '5000-7000 kg/hectare',
        'rotation_crops': ['Pulses', 'Vegetables']
    },
    {
        'name': 'Groundnut',
        'scientific_name': 'Arachis hypogaea',
        'description': 'Major oilseed crop in Coimbatore, important for both oil production and direct consumption.',
        'suitable_soil_types': ['Sandy Soil', 'Loamy Soil', 'Red Soil'],
        'growing_seasons': ['Monsoon', 'Post-monsoon'],
        'growth_duration': '90-120 days',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'Low',
            'phosphorus': 'Medium',
            'potassium': 'Medium'
        },
        'optimal_temperature': '25-30°C',
        'average_yield': '1500-2500 kg/hectare',
        'rotation_crops': ['Cereals', 'Vegetables']
    },
    {
        'name': 'Turmeric',
        'scientific_name': 'Curcuma longa',
        'description': 'Coimbatore is famous for its turmeric production, especially the Erode variety which is known for its quality.',
        'suitable_soil_types': ['Loamy Soil', 'Clay Soil', 'Red Soil'],
        'growing_seasons': ['Monsoon'],
        'growth_duration': '8-9 months',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'Medium',
            'phosphorus': 'High',
            'potassium': 'High'
        },
        'optimal_temperature': '20-30°C',
        'average_yield': '25000-30000 kg/hectare',
        'rotation_crops': ['Cereals', 'Pulses']
    },
    {
        'name': 'Ragi (Finger Millet)',
        'scientific_name': 'Eleusine coracana',
        'description': 'Drought-resistant cereal crop suited for the drier areas of Coimbatore region.',
        'suitable_soil_types': ['Red Soil', 'Sandy Soil', 'Loamy Soil'],
        'growing_seasons': ['Monsoon', 'Post-monsoon'],
        'growth_duration': '90-120 days',
        'water_requirements': 'Low',
        'nutrition_requirements': {
            'nitrogen': 'Low',
            'phosphorus': 'Low',
            'potassium': 'Low'
        },
        'optimal_temperature': '20-35°C',
        'average_yield': '1500-3000 kg/hectare',
        'rotation_crops': ['Pulses', 'Oilseeds']
    },
    {
        'name': 'Coconut',
        'scientific_name': 'Cocos nucifera',
        'description': 'Perennial crop widely cultivated in Coimbatore for its various uses including oil, fiber, and food.',
        'suitable_soil_types': ['Sandy Soil', 'Loamy Soil', 'Alluvial Soil'],
        'growing_seasons': ['Year-round (perennial)'],
        'growth_duration': 'First harvest after 5-7 years, productive for 60+ years',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'Medium',
            'phosphorus': 'Medium',
            'potassium': 'High'
        },
        'optimal_temperature': '20-35°C',
        'average_yield': '80-100 nuts per tree per year',
        'intercropping': ['Pulses', 'Vegetables', 'Banana']
    },
    {
        'name': 'Tomato',
        'scientific_name': 'Solanum lycopersicum',
        'description': 'Short-term vegetable crop popular among small farmers in Coimbatore for its quick returns.',
        'suitable_soil_types': ['Loamy Soil', 'Red Soil', 'Sandy Soil'],
        'growing_seasons': ['Winter', 'Post-monsoon'],
        'growth_duration': '90-120 days',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'Medium',
            'phosphorus': 'High',
            'potassium': 'High'
        },
        'optimal_temperature': '20-30°C',
        'average_yield': '20000-40000 kg/hectare',
        'rotation_crops': ['Cereals', 'Legumes']
    },
    {
        'name': 'Brinjal (Eggplant)',
        'scientific_name': 'Solanum melongena',
        'description': 'Popular vegetable crop in Coimbatore that provides regular income to farmers.',
        'suitable_soil_types': ['Loamy Soil', 'Clay Soil', 'Sandy Loam'],
        'growing_seasons': ['Winter', 'Post-monsoon'],
        'growth_duration': '150-180 days',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'Medium',
            'phosphorus': 'Medium',
            'potassium': 'Medium'
        },
        'optimal_temperature': '20-30°C',
        'average_yield': '30000-40000 kg/hectare',
        'rotation_crops': ['Cereals', 'Pulses']
    },
    {
        'name': 'Green Gram (Moong)',
        'scientific_name': 'Vigna radiata',
        'description': 'Short-duration pulse crop suitable for crop rotation in Coimbatore, helps in nitrogen fixation.',
        'suitable_soil_types': ['Sandy Soil', 'Loamy Soil', 'Red Soil'],
        'growing_seasons': ['Winter', 'Post-monsoon'],
        'growth_duration': '60-90 days',
        'water_requirements': 'Low',
        'nutrition_requirements': {
            'nitrogen': 'Low (fixes nitrogen)',
            'phosphorus': 'Medium',
            'potassium': 'Low'
        },
        'optimal_temperature': '25-35°C',
        'average_yield': '800-1200 kg/hectare',
        'rotation_crops': ['Cereals', 'Vegetables']
    },
    {
        'name': 'Black Gram (Urad)',
        'scientific_name': 'Vigna mungo',
        'description': 'Pulse crop suitable for crop rotation in Coimbatore, helps improve soil fertility.',
        'suitable_soil_types': ['Clay Soil', 'Loamy Soil', 'Black Soil'],
        'growing_seasons': ['Monsoon', 'Post-monsoon'],
        'growth_duration': '70-90 days',
        'water_requirements': 'Low',
        'nutrition_requirements': {
            'nitrogen': 'Low (fixes nitrogen)',
            'phosphorus': 'Medium',
            'potassium': 'Low'
        },
        'optimal_temperature': '25-35°C',
        'average_yield': '700-1000 kg/hectare',
        'rotation_crops': ['Cereals', 'Oilseeds']
    },
    {
        'name': 'Sorghum (Jowar)',
        'scientific_name': 'Sorghum bicolor',
        'description': 'Drought-resistant cereal crop suitable for drier parts of Coimbatore.',
        'suitable_soil_types': ['Red Soil', 'Black Soil', 'Loamy Soil'],
        'growing_seasons': ['Winter', 'Monsoon'],
        'growth_duration': '100-120 days',
        'water_requirements': 'Low',
        'nutrition_requirements': {
            'nitrogen': 'Medium',
            'phosphorus': 'Low',
            'potassium': 'Low'
        },
        'optimal_temperature': '25-35°C',
        'average_yield': '2000-3000 kg/hectare',
        'rotation_crops': ['Pulses', 'Oilseeds']
    },
    {
        'name': 'Banana',
        'scientific_name': 'Musa paradisiaca',
        'description': 'Important fruit crop in Coimbatore with varieties like Poovan, Nendran, and Robusta being popular.',
        'suitable_soil_types': ['Loamy Soil', 'Red Soil', 'Alluvial Soil'],
        'growing_seasons': ['Year-round planting possible'],
        'growth_duration': '10-15 months',
        'water_requirements': 'High',
        'nutrition_requirements': {
            'nitrogen': 'High',
            'phosphorus': 'Medium',
            'potassium': 'High'
        },
        'optimal_temperature': '20-35°C',
        'average_yield': '40000-60000 kg/hectare',
        'rotation_crops': ['Pulses', 'Vegetables']
    },
    {
        'name': 'Pearl Millet (Bajra)',
        'scientific_name': 'Pennisetum glaucum',
        'description': 'Drought-resistant cereal crop suitable for rainfed agriculture in Coimbatore.',
        'suitable_soil_types': ['Sandy Soil', 'Red Soil', 'Loamy Soil'],
        'growing_seasons': ['Monsoon'],
        'growth_duration': '80-100 days',
        'water_requirements': 'Low',
        'nutrition_requirements': {
            'nitrogen': 'Low',
            'phosphorus': 'Low',
            'potassium': 'Low'
        },
        'optimal_temperature': '25-35°C',
        'average_yield': '1500-2500 kg/hectare',
        'rotation_crops': ['Pulses', 'Oilseeds']
    },
    {
        'name': 'Okra (Ladies Finger)',
        'scientific_name': 'Abelmoschus esculentus',
        'description': 'Popular vegetable crop in Coimbatore that provides regular income to small farmers.',
        'suitable_soil_types': ['Sandy Loam', 'Loamy Soil', 'Red Soil'],
        'growing_seasons': ['Summer', 'Monsoon'],
        'growth_duration': '45-60 days',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'Medium',
            'phosphorus': 'Medium',
            'potassium': 'Medium'
        },
        'optimal_temperature': '25-35°C',
        'average_yield': '10000-15000 kg/hectare',
        'rotation_crops': ['Cereals', 'Pulses']
    },
    {
        'name': 'Onion',
        'scientific_name': 'Allium cepa',
        'description': 'Important vegetable crop in Coimbatore with high market demand.',
        'suitable_soil_types': ['Loamy Soil', 'Sandy Loam', 'Red Soil'],
        'growing_seasons': ['Winter', 'Post-monsoon'],
        'growth_duration': '130-150 days',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'Medium',
            'phosphorus': 'Medium',
            'potassium': 'High'
        },
        'optimal_temperature': '15-25°C',
        'average_yield': '25000-35000 kg/hectare',
        'rotation_crops': ['Cereals', 'Pulses']
    },
    {
        'name': 'Ginger',
        'scientific_name': 'Zingiber officinale',
        'description': 'Spice crop well-suited to the climate of Coimbatore region.',
        'suitable_soil_types': ['Loamy Soil', 'Red Soil', 'Sandy Loam'],
        'growing_seasons': ['Monsoon'],
        'growth_duration': '8-10 months',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'Medium',
            'phosphorus': 'Medium',
            'potassium': 'Medium'
        },
        'optimal_temperature': '20-30°C',
        'average_yield': '15000-25000 kg/hectare',
        'rotation_crops': ['Cereals', 'Vegetables']
    },
    {
        'name': 'Tapioca (Cassava)',
        'scientific_name': 'Manihot esculenta',
        'description': 'Root crop that is an important food source in parts of Coimbatore region.',
        'suitable_soil_types': ['Red Soil', 'Sandy Soil', 'Loamy Soil'],
        'growing_seasons': ['Monsoon'],
        'growth_duration': '9-12 months',
        'water_requirements': 'Low',
        'nutrition_requirements': {
            'nitrogen': 'Low',
            'phosphorus': 'Low',
            'potassium': 'Medium'
        },
        'optimal_temperature': '25-35°C',
        'average_yield': '25000-35000 kg/hectare',
        'rotation_crops': ['Pulses', 'Cereals']
    },
    {
        'name': 'Coriander',
        'scientific_name': 'Coriandrum sativum',
        'description': 'Short-duration herb crop popular among small farmers for its quick returns.',
        'suitable_soil_types': ['Loamy Soil', 'Sandy Loam', 'Black Soil'],
        'growing_seasons': ['Winter', 'Post-monsoon'],
        'growth_duration': '40-45 days (leaf), 90-120 days (seed)',
        'water_requirements': 'Medium',
        'nutrition_requirements': {
            'nitrogen': 'Low',
            'phosphorus': 'Medium',
            'potassium': 'Low'
        },
        'optimal_temperature': '15-25°C',
        'average_yield': '800-1200 kg/hectare (seed)',
        'rotation_crops': ['Cereals', 'Vegetables']
    }
]
