import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

from config import SMTP_HOST, SMTP_PORT, SMTP_PASSWORD, SMTP_USER


def send_email(order_id: str, receiver: str, filename: str):
    """
    Отправляет пользователю `receiver` письмо по заказу `order_id` с приложенным файлом `filename`

    Вы можете изменить логику работы данной функции
    """
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        print('send_email', filename)

        email = MIMEMultipart()
        email['Subject'] = f'Изображения. Заказ №{order_id}'
        email['From'] = SMTP_USER
        email['To'] = receiver

        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={filename}'
        )
        email.attach(part)
        text = email.as_string()

        server.sendmail(SMTP_USER, receiver, text)


def newsletter(emails: List):
    """Периодическая информационная рассылка"""

    message = MIMEMultipart()
    message['Subject'] = f'Информационная рассылка сервиса по обработке фото'
    message['From'] = SMTP_USER

    html = """\
    <html>
      <body>
        <p>Привет,<br>
           Как дела?<br>
           <a href="http://127.0.0.1:5000/blur">Размыть фото (API)</a> 
           Сервис по обработке изображений.
        </p>
      </body>
    </html>
    """

    part = MIMEText(html, "html")
    message.attach(part)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        for email in emails:
            print(email)
            message['To'] = email
            server.sendmail(from_addr=SMTP_USER, to_addrs=email, msg=message.as_string())
