import smtplib
from email.message import EmailMessage
import os

def send_mail(receiver, subject, message, attachment=None, server='smtp.poczta.onet.pl',
              port=465, from_email='wppen@poczta.onet.pl', password='t3l3k0mun1kacj@'):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = receiver
    msg.set_content(message)
    
    if attachment:
        file_path = os.path.abspath(attachment)  # Pobierz bezwzględną ścieżkę do pliku
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    
    try:
        with smtplib.SMTP_SSL(server, port) as server:
            server.login(from_email, password)
            server.send_message(msg)
        print('Successfully sent the mail.')
    except smtplib.SMTPAuthenticationError as e:
        print('Authentication error:', e)
    except smtplib.SMTPException as e:
        print('SMTP error occurred:', e)

def create_table_of_mails(file_path):
    try:
        with open(file_path, 'r') as file:
            emails = file.readlines()
            # Remove trailing newline characters from each email
            emails = [email.strip() for email in emails]
        return emails
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

to_mails = create_table_of_mails("mails.txt")

for mail in to_mails:
    send_mail(receiver=mail, 
              subject='[Turbo Scanner] - Automatic report', message='This message has been automatically generated from application Turbo Scanner.', 
              attachment='report.zip')
