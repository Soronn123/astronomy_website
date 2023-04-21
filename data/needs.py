import bcrypt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import secrets


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


def checked_email(email):
    sender = "bratsk.post@yandex.ru"
    password_sender = "post-bratsk2023"

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = 'Код подтверждения почты!'

    alphabet = string.ascii_letters + string.digits
    body = ''.join(secrets.choice(alphabet) for i in range(8))
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(sender, password_sender)
    server.send_message(msg)
    server.quit()
    return body
