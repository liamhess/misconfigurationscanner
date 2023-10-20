import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass

def send_email_alerts(ips, ports):
    sender_email = 'liro08@gmx.ch'
    receiver_email = 'simeon.schaer1@gmail.com'
    password = getpass.getpass('Bitte gib dein E-Mail Passwort ein: ')
    
    # Verbindung zum E-Mail-Server herstellen
    smtp_server = 'mail.gmx.net'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # TLS-Verschlüsselung aktivieren

    # Anmeldung beim E-Mail-Konto
    server.login(sender_email, password)


    # Erstellen der E-Mail-Nachricht
    message = MIMEMultipart()
    #port_text = ', '.join(ports)  # Konvertiere die Liste der Ports zu einem kommagetrennten String
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Securitywarning for Servers with the IPs:'

    body = f'This is a warning, on servers with the following IPs: {ips}, the following ports are open: {ports}! \n\n The Admin interface is open, please fix this immediately! \n\n This poses a major risk to our security \n\n On this page you will learn how to close the port:\nhttps://www.acunetix.com/blog/articles/close-unused-open-ports/\n'
    message.attach(MIMEText(body, 'plain'))

    # E-Mail senden
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Verbindung zum E-Mail-Server beenden
    server.quit()

# E-Mail-Konfiguration

ips = '127.0.0.1'
ports = ['44', '10000', '25']

# Funktion aufrufen, um E-Mails zu senden
send_email_alerts(ips, ports)
