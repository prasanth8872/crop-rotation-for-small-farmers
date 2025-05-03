from flask import render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import requests
import logging

from app import app, db
from models import User, Farm, SoilData, CropCycle, Query, WeatherData, UserRecommendation
from forms import LoginForm, RegistrationForm, QueryForm, FarmForm, UserRecommendationForm
from utils import get_weather_data, get_crop_recommendation
from crop_data import crop_data

# Home page
@app.route('/')
def index():
    # Get latest weather data for Coimbatore
    weather = get_weather_data('Coimbatore')
    
    # Store weather data in database
    if weather:
        weather_record = WeatherData(
            city='Coimbatore',
            temperature=weather.get('temperature', 0),
            humidity=weather.get('humidity', 0),
            pressure=weather.get('pressure', 0),
            wind_speed=weather.get('wind_speed', 0),
            conditions=weather.get('conditions', 'Unknown')
        )
        db.session.add(weather_record)
        db.session.commit()
    
    # Get some featured crops from our database
    featured_crops = crop_data[:6]  # Just using first 6 crops for featured display
    
    return render_template('index.html', weather=weather, featured_crops=featured_crops)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            
            if user.is_admin:
                return redirect(next_page or url_for('admin_dashboard'))
            else:
                return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please use a different one.', 'danger')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            address=form.address.data,
            city=form.city.data or 'Coimbatore',
            state=form.state.data or 'Tamil Nadu'
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# User dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's farms
    farms = Farm.query.filter_by(user_id=current_user.id).all()
    
    # Get user's latest crop cycles
    crop_cycles = CropCycle.query.join(Farm).filter(Farm.user_id == current_user.id).order_by(CropCycle.created_at.desc()).limit(5).all()
    
    # Get latest weather data
    weather = WeatherData.query.filter_by(city='Coimbatore').order_by(WeatherData.recorded_at.desc()).first()
    
    # Get user's latest queries
    queries = Query.query.filter_by(user_id=current_user.id).order_by(Query.submitted_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                          farms=farms, 
                          crop_cycles=crop_cycles, 
                          weather=weather, 
                          queries=queries)

# Admin dashboard
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get count of users
    user_count = User.query.filter_by(is_admin=False).count()
    
    # Get count of farms
    farm_count = Farm.query.count()
    
    # Get count of queries
    query_count = Query.query.count()
    
    # Get latest weather data
    weather = WeatherData.query.filter_by(city='Coimbatore').order_by(WeatherData.recorded_at.desc()).first()
    
    # Get latest users
    latest_users = User.query.filter_by(is_admin=False).order_by(User.date_joined.desc()).limit(5).all()
    
    # Get latest queries
    latest_queries = Query.query.order_by(Query.submitted_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          user_count=user_count, 
                          farm_count=farm_count, 
                          query_count=query_count,
                          weather=weather,
                          latest_users=latest_users,
                          latest_queries=latest_queries)

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all non-admin users
    users = User.query.filter_by(is_admin=False).order_by(User.date_joined.desc()).all()
    
    return render_template('admin/users.html', users=users)

@app.route('/admin/queries')
@login_required
def admin_queries():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all queries
    queries = Query.query.order_by(Query.submitted_at.desc()).all()
    
    return render_template('admin/queries.html', queries=queries)

# Crop recommendation
@app.route('/crop-recommendation', methods=['GET', 'POST'])
@login_required
def crop_recommendation():
    form = QueryForm()
    
    if form.validate_on_submit():
        # Get recommendation based on form data
        recommended_crop = get_crop_recommendation(
            form.land_type.data,
            form.soil_type.data,
            form.previous_crop.data,
            form.previous_yield.data
        )
        
        # Save query to database
        query = Query(
            user_id=current_user.id,
            land_type=form.land_type.data,
            soil_type=form.soil_type.data,
            previous_crop=form.previous_crop.data,
            previous_yield=form.previous_yield.data,
            recommended_crop=recommended_crop
        )
        
        db.session.add(query)
        db.session.commit()
        
        flash(f'Based on your inputs, we recommend growing {recommended_crop} for your next crop cycle.', 'success')
        
        # Store result in session for display
        session['recommended_crop'] = recommended_crop
        session['query_id'] = query.id
        
        return redirect(url_for('crop_recommendation'))
    
    # Get recommended crop from session if exists
    recommended_crop = session.get('recommended_crop')
    query_id = session.get('query_id')
    
    # Clear session after retrieving
    if 'recommended_crop' in session:
        session.pop('recommended_crop')
    if 'query_id' in session:
        session.pop('query_id')
    
    # Get crop details if recommendation exists
    crop_details = None
    if recommended_crop:
        for crop in crop_data:
            if crop['name'].lower() == recommended_crop.lower():
                crop_details = crop
                break
    
    return render_template('crop_recommendation.html', form=form, recommended_crop=recommended_crop, crop_details=crop_details)

# User recommendations (community sharing)
@app.route('/user-recommendations', methods=['GET', 'POST'])
@login_required
def user_recommendations():
    form = UserRecommendationForm()
    
    if form.validate_on_submit():
        recommendation = UserRecommendation(
            user_id=current_user.id,
            title=form.title.data,
            content=form.content.data,
            crop_name=form.crop_name.data
        )
        
        db.session.add(recommendation)
        db.session.commit()
        
        flash('Your recommendation has been shared with the community. Thank you!', 'success')
        return redirect(url_for('user_recommendations'))
    
    # Get all user recommendations
    recommendations = UserRecommendation.query.order_by(UserRecommendation.created_at.desc()).all()
    
    return render_template('user_recommendations.html', form=form, recommendations=recommendations)

# Farm management
@app.route('/farms', methods=['GET', 'POST'])
@login_required
def farms():
    form = FarmForm()
    
    if form.validate_on_submit():
        farm = Farm(
            name=form.name.data,
            location=form.location.data,
            area=form.area.data,
            soil_type=form.soil_type.data,
            user_id=current_user.id
        )
        
        db.session.add(farm)
        db.session.commit()
        
        flash('Farm added successfully!', 'success')
        return redirect(url_for('farms'))
    
    # Get user's farms
    user_farms = Farm.query.filter_by(user_id=current_user.id).all()
    
    return render_template('farms.html', form=form, farms=user_farms)

# Static pages
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/crop-guide')
def crop_guide():
    return render_template('crop_guide.html', crops=crop_data)

# API routes for AJAX requests
@app.route('/api/weather')
def get_weather_api():
    city = request.args.get('city', 'Coimbatore')
    weather = get_weather_data(city)
    return jsonify(weather)

@app.route('/api/soil-data/<int:farm_id>')
@login_required
def get_soil_data_api(farm_id):
    farm = Farm.query.get_or_404(farm_id)
    
    # Check if user owns the farm
    if farm.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get soil data for the farm
    soil_data = SoilData.query.filter_by(farm_id=farm_id).order_by(SoilData.recorded_at.desc()).limit(10).all()
    
    data = [{
        'id': sd.id,
        'moisture_level': sd.moisture_level,
        'ph_value': sd.ph_value,
        'nitrogen': sd.nitrogen,
        'phosphorus': sd.phosphorus,
        'potassium': sd.potassium,
        'temperature': sd.temperature,
        'recorded_at': sd.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
    } for sd in soil_data]
    
    return jsonify(data)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
