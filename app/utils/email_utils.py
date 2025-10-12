import smtplib
from email.message import EmailMessage
from config import Config
import os

def send_email_notification(to_email, to_name, subject, html_content):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = f"{Config.SENDER_NAME} <{Config.MAIL_USERNAME}>"
        msg['To'] = to_email
        msg.set_content("This is an HTML email. Please view in HTML-compatible client.")
        msg.add_alternative(html_content, subtype='html')

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False
