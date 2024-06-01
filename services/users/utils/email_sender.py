import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import logging


def send_verification_code(email: str, code: int) -> int:
    logging.basicConfig(level=logging.INFO, filename="send_email.log", format="%(asctime)s %(levelname)s %(message)s")
    with open('config.json', 'r') as f:
        params = json.load(f)
        sender_email = params['email']
        password = params['password']
        user = params['user']
        f.close()
    mes = MIMEMultipart()
    mes['From'] = sender_email
    mes['To'] = email
    mes['Subject'] = 'Код подтверждения'
    msg_text = MIMEText(f'''Здравствуйте!<br><br>
    Одноразовый код для подтверждения регистрации аккаунта в
    приложении умного дома:<br><br>
    <h1>{code}</h1>''', 'html')
    mes.attach(msg_text)
    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.set_debuglevel(1)
    server.ehlo(email)
    server.login(user, password)
    server.auth_plain()
    try:
        server.sendmail(sender_email, email, mes.as_string())
        server.quit()
        return 0
    except Exception as e:
        logging.error(e)
        server.quit()
        return 255
