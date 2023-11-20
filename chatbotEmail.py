import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header

def send_email(to_email, subject, message):
    smtp_server = 'smtp.seu_servidor.com'
    smtp_port = 587
    smtp_username = 'seu_email@gmail.com'
    smtp_password = 'sua_senha'

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())

def read_emails():
    imap_server = 'imap.seu_servidor.com'
    imap_port = 993
    imap_username = 'seu_email@gmail.com'
    imap_password = 'sua_senha'

    with imaplib.IMAP4_SSL(imap_server, imap_port) as mail:
        mail.login(imap_username, imap_password)
        mail.select('inbox')

        status, messages = mail.search(None, '(UNSEEN)')

        if status == 'OK':
            for mail_id in messages[0].split():
                _, msg_data = mail.fetch(mail_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        email_message = email.message_from_bytes(response_part[1])

                        subject, encoding = decode_header(email_message['Subject'])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or 'utf-8')

                        sender_email = email.utils.parseaddr(email_message['From'])[1]
                        body = ""

                        if email_message.is_multipart():
                            for part in email_message.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode('utf-8')
                        else:
                            body = email_message.get_payload(decode=True).decode('utf-8')

                        response = "Obrigado por entrar em contato. Vou responder em breve!"
                        send_email(sender_email, "Re: " + subject, response)

                        # Marcar e-mail como lido
                        mail.store(mail_id, '+FLAGS', '(\Seen)')

read_emails()
