import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings import config

def is_valid_email(email):
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.match(email))

def send_email(subject, body, recipient_email):
    sender_email = config['smtp_email']
    sender_password = config['smtp_password']

    message = MIMEMultipart()
    message["From"] = f'Britt Shook AQI API <{sender_email}>'
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        
def send_alert_email(subscriber_email, alert_type, air_quality_indicator, subscriber_threshold, current_level):
    if alert_type == 'alert_message':
        send_email(f'Air Quality Alert: {air_quality_indicator} Above Threshold',  f'{air_quality_indicator} levels have surpassed your threshold of {subscriber_threshold}.\nCurrent {air_quality_indicator}: {current_level} µg/m³', subscriber_email)
    elif alert_type == 'clear_alert_message':
        send_email(f'Air Quality Update: {air_quality_indicator} Below Threshold',  f'{air_quality_indicator} levels have returned below your threshold of {subscriber_threshold}.\nCurrent {air_quality_indicator}: {current_level} µg/m³', subscriber_email)