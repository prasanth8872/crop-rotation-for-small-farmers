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
    
    # Prepare message with HTML line breaks
    message_html = contact_message.message.replace('\n', '<br>')
    
    # Email content - mobile responsive template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Message - Quantum Precision Agriculture</title>
        <style>
            @media only screen and (max-width: 620px) {{
                table[class=body] h1 {{
                    font-size: 24px !important;
                    margin-bottom: 10px !important;
                }}
                table[class=body] p,
                table[class=body] ul,
                table[class=body] ol,
                table[class=body] td,
                table[class=body] span {{
                    font-size: 16px !important;
                }}
                table[class=body] .wrapper,
                table[class=body] .article {{
                    padding: 10px !important;
                }}
                table[class=body] .content {{
                    padding: 0 !important;
                }}
                table[class=body] .container {{
                    padding: 0 !important;
                    width: 100% !important;
                }}
                table[class=body] .main {{
                    border-left-width: 0 !important;
                    border-radius: 0 !important;
                    border-right-width: 0 !important;
                }}
            }}
        </style>
    </head>
    <body style="background-color: #f6f6f6; font-family: Arial, sans-serif; -webkit-font-smoothing: antialiased; font-size: 16px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
        <table border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background-color: #f6f6f6;">
            <tr>
                <td style="font-family: Arial, sans-serif; font-size: 16px; vertical-align: top;">&nbsp;</td>
                <td class="container" style="font-family: Arial, sans-serif; font-size: 16px; vertical-align: top; display: block; margin: 0 auto; max-width: 580px; padding: 10px; width: 580px;">
                    <div class="content" style="box-sizing: border-box; display: block; margin: 0 auto; max-width: 580px; padding: 10px;">
                        <table class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background: #ffffff; border-radius: 4px;">
                            <tr>
                                <td class="wrapper" style="font-family: Arial, sans-serif; font-size: 16px; vertical-align: top; box-sizing: border-box; padding: 20px;">
                                    <h2 style="color: #333; font-family: Arial, sans-serif; font-weight: 600; line-height: 1.4; margin: 0 0 20px;">New Contact Message</h2>
                                    
                                    <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; margin: 0 0 15px;"><strong>From:</strong> {contact_message.email}</p>
                                    <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; margin: 0 0 15px;"><strong>Subject:</strong> {contact_message.subject}</p>
                                    <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; margin: 0 0 15px;"><strong>Inquiry Type:</strong> {contact_message.inquiry_type}</p>
                                    <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; margin: 0 0 15px;"><strong>Message:</strong></p>
                                    
                                    <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #007bff; margin-bottom: 20px;">
                                        {message_html}
                                    </div>
                                    
                                    <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; margin: 20px 0 0;">Please log in to the admin dashboard to respond.</p>
                                </td>
                            </tr>
                        </table>
                        <div class="footer" style="clear: both; margin-top: 10px; text-align: center; width: 100%;">
                            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                                <tr>
                                    <td class="content-block" style="font-family: Arial, sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; font-size: 12px; color: #999999; text-align: center;">
                                        <span class="apple-link" style="color: #999999; font-size: 12px; text-align: center;">Quantum Precision Agriculture, Coimbatore, Tamil Nadu, India</span>
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </td>
                <td style="font-family: Arial, sans-serif; font-size: 16px; vertical-align: top;">&nbsp;</td>
            </tr>
        </table>
    </body>
    </html>
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
    # Replace newlines with <br> for HTML display
    admin_reply_html = contact_message.admin_reply.replace('\n', '<br>')
    message_html = contact_message.message.replace('\n', '<br>')
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quantum Precision Agriculture - Response</title>
        <style>
            @media only screen and (max-width: 620px) {{
                table[class=body] h1 {{
                    font-size: 24px !important;
                    margin-bottom: 10px !important;
                }}
                table[class=body] p,
                table[class=body] ul,
                table[class=body] ol,
                table[class=body] td,
                table[class=body] span {{
                    font-size: 16px !important;
                }}
                table[class=body] .wrapper,
                table[class=body] .article {{
                    padding: 10px !important;
                }}
                table[class=body] .content {{
                    padding: 0 !important;
                }}
                table[class=body] .container {{
                    padding: 0 !important;
                    width: 100% !important;
                }}
                table[class=body] .main {{
                    border-left-width: 0 !important;
                    border-radius: 0 !important;
                    border-right-width: 0 !important;
                }}
            }}
        </style>
    </head>
    <body style="background-color: #f6f6f6; font-family: Arial, sans-serif; -webkit-font-smoothing: antialiased; font-size: 16px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
        <table border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background-color: #f6f6f6;">
            <tr>
                <td style="font-family: Arial, sans-serif; font-size: 16px; vertical-align: top;">&nbsp;</td>
                <td class="container" style="font-family: Arial, sans-serif; font-size: 16px; vertical-align: top; display: block; margin: 0 auto; max-width: 580px; padding: 10px; width: 580px;">
                    <div class="content" style="box-sizing: border-box; display: block; margin: 0 auto; max-width: 580px; padding: 10px;">
                        <table class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background: #ffffff; border-radius: 4px;">
                            <tr>
                                <td class="wrapper" style="font-family: Arial, sans-serif; font-size: 16px; vertical-align: top; box-sizing: border-box; padding: 20px;">
                                    <h2 style="color: #333; font-family: Arial, sans-serif; font-weight: 600; line-height: 1.4; margin: 0 0 20px;">Response to your inquiry</h2>
                                    <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; margin: 0 0 15px;">Thank you for contacting Quantum Precision Agriculture. Below is our response to your inquiry:</p>
                                    
                                    <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #28a745; margin-bottom: 20px;">
                                        {admin_reply_html}
                                    </div>
                                    
                                    <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; margin: 20px 0 15px;">Your original message:</p>
                                    <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #6c757d; color: #666; margin-bottom: 20px;">
                                        {message_html}
                                    </div>
                                    
                                    <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; margin: 20px 0 15px;">If you have any further questions, please don't hesitate to contact us again.</p>
                                    
                                    <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: normal; margin: 20px 0 0;">Best regards,<br>Quantum Precision Agriculture Team</p>
                                </td>
                            </tr>
                        </table>
                        <div class="footer" style="clear: both; margin-top: 10px; text-align: center; width: 100%;">
                            <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">
                                <tr>
                                    <td class="content-block" style="font-family: Arial, sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; font-size: 12px; color: #999999; text-align: center;">
                                        <span class="apple-link" style="color: #999999; font-size: 12px; text-align: center;">Quantum Precision Agriculture, Coimbatore, Tamil Nadu, India</span>
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </td>
                <td style="font-family: Arial, sans-serif; font-size: 16px; vertical-align: top;">&nbsp;</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    return send_email(contact_message.email, subject, html_content=html_content)