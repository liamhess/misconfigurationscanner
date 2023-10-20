import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass

# E-Mail-Konfiguration
sender_email = 'liro08@gmx.ch'
receiver_email = 'simeon.schaer1@gmail.com'
password = getpass.getpass('Bitte gib dein E-Mail Passwort ein: ')
ips = ['127.0.0.1', '192.168.1.1', '10.0.0.1']  # Eine Liste von IPs

# Verbindung zum E-Mail-Server herstellen
smtp_server = 'mail.gmx.net'
smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  # TLS-Verschlüsselung aktivieren

# Anmeldung beim E-Mail-Konto
server.login(sender_email, password)

for ip in ips:
    # Erstellen der E-Mail-Nachricht
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = f'Port 10000 offen bei {ip}'

    # E-Mail-Inhalt mit formatierter IP-Adresse
    body = f'Dies ist ein Notfall, weil bei dem Server {ip} der Port 10000 offen ist.'
    message.attach(MIMEText(body, 'plain'))

    # E-Mail senden
    server.sendmail(sender_email, receiver_email, message.as_string())

# Verbindung zum E-Mail-Server beenden
server.quit()
