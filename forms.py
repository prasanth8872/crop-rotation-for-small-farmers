from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=64)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=256)])
    city = StringField('City', validators=[Optional(), Length(max=64)], default='Coimbatore')
    state = StringField('State', validators=[Optional(), Length(max=64)], default='Tamil Nadu')
    submit = SubmitField('Register')

class QueryForm(FlaskForm):
    land_type = SelectField('Type of Land', choices=[
        ('flat', 'Flat Land'),
        ('sloped', 'Sloped Land'),
        ('terraced', 'Terraced Land'),
        ('wetland', 'Wetland')
    ], validators=[DataRequired()])
    
    soil_type = SelectField('Type of Soil', choices=[
        ('red_soil', 'Red Soil'),
        ('black_soil', 'Black Soil'),
        ('alluvial_soil', 'Alluvial Soil'),
        ('sandy_soil', 'Sandy Soil'),
        ('clay_soil', 'Clay Soil'),
        ('loamy_soil', 'Loamy Soil')
    ], validators=[DataRequired()])
    
    previous_crop = StringField('Previous Crop', validators=[DataRequired(), Length(max=128)])
    previous_yield = FloatField('Previous Yield (in kg/acre)', validators=[DataRequired()])
    submit = SubmitField('Get Recommendation')

class FarmForm(FlaskForm):
    name = StringField('Farm Name', validators=[DataRequired(), Length(max=128)])
    location = StringField('Location', validators=[DataRequired(), Length(max=256)])
    area = FloatField('Area (in acres)', validators=[DataRequired()])
    soil_type = SelectField('Soil Type', choices=[
        ('red_soil', 'Red Soil'),
        ('black_soil', 'Black Soil'),
        ('alluvial_soil', 'Alluvial Soil'),
        ('sandy_soil', 'Sandy Soil'),
        ('clay_soil', 'Clay Soil'),
        ('loamy_soil', 'Loamy Soil')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Farm')

class UserRecommendationForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Your Experience/Recommendation', validators=[DataRequired()])
    crop_name = StringField('Crop Name', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Share with Community')

class ContactForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=128)])
    message = TextAreaField('Message', validators=[DataRequired()])
    inquiry_type = SelectField('Inquiry Type', choices=[
        ('technical', 'Technical Support'),
        ('agricultural', 'Agricultural Advice'),
        ('feedback', 'Feedback/Suggestions'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    submit = SubmitField('Send Message')

class AdminReplyForm(FlaskForm):
    reply = TextAreaField('Reply Message', validators=[DataRequired()])
    submit = SubmitField('Send Reply')

class SearchHistorySearchForm(FlaskForm):
    search_term = StringField('Search Term', validators=[Optional()])
    start_date = StringField('Start Date', validators=[Optional()])
    end_date = StringField('End Date', validators=[Optional()])
    submit = SubmitField('Search')
