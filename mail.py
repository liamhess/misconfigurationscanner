import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import hashlib

def hash_password(password):
    # Hier wird das Passwort mit SHA-256 gehasht, Sie können eine andere Methode verwenden
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

def send_email_alerts(ips, ports):
    sender_email = 'SENDER_EMAIL'
    receiver_email = 'RECEIVER_EMAIL'
    password = 'PASSWORD'

    # Erstellen der E-Mail-Nachricht
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Securitywarning for Servers with the IPs:'

    body = f'This is a warning, on servers with the following IPs: {ips}, the following ports are open: {ports}! \n\n The Admin interface is open, please fix this immediately! \n\n This poses a major risk to our security \n\n On this page you will learn how to close the port:\nhttps://www.acunetix.com/blog/articles/close-unused-open-ports/\n'
    message.attach(MIMEText(body, 'plain'))

    # Verbindung zum E-Mail-Server herstellen
    smtp_server = 'SMTP_SERVER'
    smtp_port ='SMTP_PORT'
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # TLS-Verschlüsselung aktivieren

    # Anmeldung beim E-Mail-Konto mit dem gehashten Passwort
    server.login(sender_email, password)

    # E-Mail senden
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Verbindung zum E-Mail-Server beenden
    server.quit()

# E-Mail-Konfiguration
ips = '127.0.0.1'
ports = ['44', '10000', '25']

# E-Mail senden
send_email_alerts(ips, ports)
