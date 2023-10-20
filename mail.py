import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config

def send_email_alerts(ips, ports):
    sender_email = config('SENDER_EMAIL')
    receiver_email = config('RECEIVER_EMAIL')
    password = config('PASSWORD')

    # Erstellen der E-Mail-Nachricht
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Securitywarning for Servers with the IPs:'

    body = f'This is a warning, on servers with the following IPs: {ips}, the following ports are open: {ports}! \n\n The Admin interface is open, please fix this immediately! \n\n This poses a major risk to our security \n\n On this page you will learn how to close the port:\nhttps://www.acunetix.com/blog/articles/close-unused-open-ports/\n'
    message.attach(MIMEText(body, 'plain'))

    # Verbindung zum E-Mail-Server herstellen
    smtp_server = config('SMTP_SERVER')
    smtp_port = config('SMTP_PORT')
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # TLS-Verschlüsselung aktivieren

    # Anmeldung beim E-Mail-Konto mit dem gehashten Passwort
    server.login(sender_email, password)

    # E-Mail senden
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Verbindung zum E-Mail-Server beenden
    server.quit()
