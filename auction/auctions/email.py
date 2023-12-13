from datetime import datetime
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "jeff.chism@gmail.com"
sender_password = ""
recipient_email = "jeff.chism@gmail.com"

def send_email(body, filename): 
    with open(filename, "rb") as attachment:
        # Add the attachment to the message
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= '{filename}'".format(filename=filename),
    )

    message = MIMEMultipart()
    message['Subject'] = datetime.today().strftime('%Y-%m-%d %H:%M') + " - Report"
    message['From'] = sender_email
    message['To'] = recipient_email
    html_part = MIMEText(body)
    message.attach(html_part)
    message.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
