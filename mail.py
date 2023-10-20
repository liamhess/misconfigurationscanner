import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass

def send_email_alerts(sender_email, receiver_email, password, ip_ports):
    # Verbindung zum E-Mail-Server herstellen
    smtp_server = 'mail.gmx.net'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # TLS-Verschlüsselung aktivieren

    # Anmeldung beim E-Mail-Konto
    server.login(sender_email, password)

    # Erstelle eine leere Menge, um zu überprüfen, ob eine IP bereits verarbeitet wurde
    processed_ips = set()

    for ip, port in ip_ports:
        if ip not in processed_ips:
            # Erstellen der E-Mail-Nachricht
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = f'Offene Ports bei {ip}'

            # E-Mail-Inhalt mit formatierter IP-Adresse und Liste der offenen Ports
            open_ports = [p for i, p in ip_ports if i == ip]
            body = f'Dies ist ein Notfall, weil bei dem Server {ip} die folgenden Ports offen sind: {", ".join(open_ports)}'
            message.attach(MIMEText(body, 'plain'))

            # E-Mail senden
            server.sendmail(sender_email, receiver_email, message.as_string())

            # Füge die verarbeitete IP zur Menge hinzu
            processed_ips.add(ip)

    # Verbindung zum E-Mail-Server beenden
    server.quit()

# E-Mail-Konfiguration
sender_email = 'liro08@gmx.ch'
receiver_email = 'simeon.schaer1@gmail.com'
password = getpass.getpass('Bitte gib dein E-Mail Passwort ein: ')
ip_ports = [('127.0.0.1', '44'), ('192.168.1.1', '10000'), ('10.0.0.1', '10000')]

# Funktion aufrufen, um E-Mails zu senden
send_email_alerts(sender_email, receiver_email, password, ip_ports)
