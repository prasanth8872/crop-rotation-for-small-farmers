import os
import sys
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_email(to_email, subject, html_content=None, text_content=None):
    """
    Send an email using SendGrid
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        html_content (str, optional): HTML content of the email
        text_content (str, optional): Plain text content of the email
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    # Get SendGrid API key from environment variables
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    
    if not sendgrid_key:
        logging.error("SENDGRID_API_KEY environment variable not set")
        return False
    
    # Set sender email - admin email (farmhub04@gmail.com)
    from_email = "farmhub04@gmail.com"
    
    # Create message
    message = Mail(
        from_email=Email(from_email),
        to_emails=To(to_email),
        subject=subject
    )
    
    # Set content (prefer HTML over plain text)
    if html_content:
        message.content = Content("text/html", html_content)
    elif text_content:
        message.content = Content("text/plain", text_content)
    else:
        logging.error("Either html_content or text_content must be provided")
        return False
    
    try:
        # Get SendGrid client
        sg = SendGridAPIClient(sendgrid_key)
        
        # Send email
        response = sg.send(message)
        
        # Log response
        logging.info(f"Email sent successfully to {to_email}, status code: {response.status_code}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        return False

def send_contact_notification(contact_message):
    """
    Send notification email to admin when a new contact message is received
    
    Args:
        contact_message: ContactMessage object from the database
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    # Admin email
    admin_email = "farmhub04@gmail.com"
    
    # Email subject
    subject = f"New Contact Message: {contact_message.subject}"
    
    # Email content
    html_content = f"""
    <h2>New Contact Message</h2>
    <p><strong>From:</strong> {contact_message.email}</p>
    <p><strong>Subject:</strong> {contact_message.subject}</p>
    <p><strong>Inquiry Type:</strong> {contact_message.inquiry_type}</p>
    <p><strong>Message:</strong></p>
    <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #007bff;">
        {contact_message.message.replace('\n', '<br>')}
    </div>
    <p>Please log in to the admin dashboard to respond.</p>
    """
    
    return send_email(admin_email, subject, html_content=html_content)

def send_reply_email(contact_message):
    """
    Send reply email to user
    
    Args:
        contact_message: ContactMessage object from the database with admin_reply
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    # Check if the message has a reply
    if not contact_message.admin_reply:
        logging.error(f"Contact message {contact_message.id} has no admin reply")
        return False
    
    # Email subject
    subject = f"Re: {contact_message.subject}"
    
    # Email content
    html_content = f"""
    <h2>Response to your inquiry</h2>
    <p>Thank you for contacting Quantum Precision Agriculture. Below is our response to your inquiry:</p>
    
    <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #28a745;">
        {contact_message.admin_reply.replace('\n', '<br>')}
    </div>
    
    <p style="margin-top: 20px;"><strong>Your original message:</strong></p>
    <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #6c757d; color: #666;">
        {contact_message.message.replace('\n', '<br>')}
    </div>
    
    <p style="margin-top: 20px;">If you have any further questions, please don't hesitate to contact us again.</p>
    
    <p>Best regards,<br>Quantum Precision Agriculture Team</p>
    """
    
    return send_email(contact_message.email, subject, html_content=html_content)