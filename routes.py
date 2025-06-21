from flask import render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import requests
import logging

from app import app, db
from models import User, Farm, SoilData, CropCycle, Query, WeatherData, UserRecommendation, ContactMessage, ContactMessageStatus, SearchHistory
from forms import LoginForm, RegistrationForm, QueryForm, FarmForm, UserRecommendationForm, ContactForm, AdminReplyForm, SearchHistorySearchForm, DeleteForm
from utils import get_weather_data, get_crop_recommendation
from crop_data import crop_data

# Helper function to log search history
def log_search(user_id, search_term, search_type):
    """
    Log a search to the SearchHistory table
    
    Args:
        user_id (int): ID of the user performing the search
        search_term (str): The search query or term
        search_type (str): Type of search (e.g., 'crop', 'soil', etc.)
    """
    try:
        search_entry = SearchHistory(
            user_id=user_id,
            search_term=search_term,
            search_type=search_type
        )
        db.session.add(search_entry)
        db.session.commit()
        logging.info(f"Search logged: {search_term} ({search_type}) by user {user_id}")
    except Exception as e:
        logging.error(f"Failed to log search: {str(e)}")
        db.session.rollback()

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
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Log the username being used for login
        logging.info(f"Login attempt with username: {form.username.data}")
        
        # Check if the user exists in the database
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            logging.info(f"User found: {user.username}, is_admin: {user.is_admin}")
        else:
            logging.warning(f"User not found: {form.username.data}")
        
        # Verify the password
        if user and check_password_hash(user.password_hash, form.password.data):
            logging.info(f"Password verification successful for user: {user.username}")
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            
            # Admin users are always redirected to admin dashboard
            if user.is_admin:
                logging.info(f"Redirecting admin user {user.username} to admin dashboard.")
                flash(f"Welcome back, Admin {user.username}!", 'success')
                return redirect(next_page or url_for('admin_dashboard'))
            else:
                logging.info(f"Redirecting regular user {user.username} to dashboard.")
                flash(f"Welcome back, {user.first_name}!", 'success')
                return redirect(next_page or url_for('dashboard'))
        else:
            logging.warning(f"Invalid login attempt for username: {form.username.data}")
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
    
    # Get user's contact messages with replies
    contact_messages = ContactMessage.query.filter_by(
        user_id=current_user.id, 
        status=ContactMessageStatus.REPLIED
    ).order_by(ContactMessage.replied_at.desc()).limit(5).all()
    
    # Also check messages sent via email without login
    email_messages = ContactMessage.query.filter_by(
        email=current_user.email, 
        status=ContactMessageStatus.REPLIED
    ).order_by(ContactMessage.replied_at.desc()).limit(5).all()
    
    # Combine both message lists
    all_messages = list(contact_messages)
    for msg in email_messages:
        if msg not in all_messages:
            all_messages.append(msg)
    
    # Sort combined messages by replied_at date
    all_messages.sort(key=lambda x: x.replied_at if x.replied_at else x.created_at, reverse=True)
    
    return render_template('dashboard.html', 
                          farms=farms, 
                          crop_cycles=crop_cycles, 
                          weather=weather, 
                          queries=queries,
                          messages=all_messages[:5])

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

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Don't allow deleting admins
    if user.is_admin:
        flash('Cannot delete admin users.', 'danger')
        return redirect(url_for('admin_users'))
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.username} has been deleted.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Don't allow editing admins
    if user.is_admin and user.id != current_user.id:
        flash('Cannot edit other admin users.', 'danger')
        return redirect(url_for('admin_users'))
    
    form = RegistrationForm(obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.address = form.address.data
        user.city = form.city.data
        user.state = form.state.data
        
        # Only update password if a new one is provided
        if form.password.data:
            user.password_hash = generate_password_hash(form.password.data)
        
        db.session.commit()
        
        flash(f'User {user.username} has been updated.', 'success')
        return redirect(url_for('admin_users'))
    
    # Don't prefill password fields
    form.password.data = ''
    form.confirm_password.data = ''
    
    return render_template('admin/edit_user.html', form=form, user=user)

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
        
        # Log this as a search
        search_term = f"{form.soil_type.data} soil, {form.land_type.data} land, previous crop: {form.previous_crop.data}"
        log_search(current_user.id, search_term, 'crop_recommendation')
        
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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Create a new contact message
        contact_message = ContactMessage(
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
            inquiry_type=form.inquiry_type.data,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        
        db.session.add(contact_message)
        db.session.commit()
        
        # Send email notification to admin
        try:
            from email_service import send_contact_notification
            send_contact_notification(contact_message)
        except Exception as e:
            logging.error(f"Failed to send contact notification email: {str(e)}")
            # Failure to send email shouldn't affect user experience
            pass
        
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    # Pass a unique CSRF token id to the template
    csrf_token_id = f"csrf_token_{id(form)}"
    return render_template('contact.html', form=form, csrf_token_id=csrf_token_id)

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

# Admin messages management
@app.route('/admin/messages')
@login_required
def admin_messages():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all messages
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    
    # Create DeleteForm for CSRF protection
    form = DeleteForm()
    
    return render_template('admin/messages.html', messages=messages, form=form)

@app.route('/admin/message/<int:message_id>')
@login_required
def admin_view_message(message_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    message = ContactMessage.query.get_or_404(message_id)
    
    # Update message status to READ if it's NEW
    if message.status == ContactMessageStatus.NEW:
        message.status = ContactMessageStatus.READ
        db.session.commit()
    
    # Create reply form
    form = AdminReplyForm()
    
    # Create delete form for CSRF protection
    delete_form = DeleteForm()
    
    return render_template('admin/view_message.html', message=message, form=form, delete_form=delete_form)

@app.route('/admin/message/<int:message_id>/reply', methods=['POST'])
@login_required
def admin_reply_message(message_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    message = ContactMessage.query.get_or_404(message_id)
    form = AdminReplyForm()
    
    if form.validate_on_submit():
        message.admin_reply = form.reply.data
        message.replied_at = datetime.utcnow()
        message.status = ContactMessageStatus.REPLIED
        db.session.commit()
        
        # Send email reply to user
        try:
            from email_service import send_reply_email
            send_reply_email(message)
            flash('Your reply has been sent to the user!', 'success')
        except Exception as e:
            logging.error(f"Failed to send reply email: {str(e)}")
            flash('Reply saved, but there was an issue sending the email. Check SendGrid settings.', 'warning')
        
        return redirect(url_for('admin_messages'))
    
    return render_template('admin/view_message.html', message=message, form=form)

@app.route('/admin/message/<int:message_id>/delete', methods=['POST'])
@login_required
def admin_delete_message(message_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Create and validate form for CSRF protection
    form = DeleteForm()
    if form.validate_on_submit():
        message = ContactMessage.query.get_or_404(message_id)
        
        db.session.delete(message)
        db.session.commit()
        
        flash('Message has been deleted.', 'success')
    else:
        flash('Invalid form submission. CSRF token missing or expired.', 'danger')
        
    return redirect(url_for('admin_messages'))

@app.route('/admin/message/<int:message_id>/archive', methods=['POST'])
@login_required
def admin_archive_message(message_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Create and validate form for CSRF protection
    form = DeleteForm()
    if form.validate_on_submit():
        message = ContactMessage.query.get_or_404(message_id)
        
        message.status = ContactMessageStatus.ARCHIVED
        db.session.commit()
        
        flash('Message has been archived.', 'success')
    else:
        flash('Invalid form submission. CSRF token missing or expired.', 'danger')
        
    return redirect(url_for('admin_messages'))

# Admin search history management
@app.route('/admin/search-history')
@login_required
def admin_search_history():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = SearchHistorySearchForm()
    
    # Get filter parameters
    search_term = request.args.get('search_term', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    # Build query
    query = SearchHistory.query
    
    if search_term:
        query = query.filter(SearchHistory.search_term.ilike(f'%{search_term}%'))
    
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(SearchHistory.created_at >= start_date_obj)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(SearchHistory.created_at <= end_date_obj)
        except ValueError:
            pass
    
    search_history = query.order_by(SearchHistory.created_at.desc()).all()
    
    return render_template('admin/search_history.html', search_history=search_history, form=form)
