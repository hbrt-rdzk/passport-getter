import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Extractor:
    def __init__(self, html_file_path: str) -> None:
        with open(html_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        self.soup = BeautifulSoup(html_content, "html.parser")

    def extract_passport_queue(self) -> None:
        div = self.soup.find("div", text=lambda t: t and "UZ: PASZPORT" in t)
        if div:
            queue_content = div.prettify()
            if "Najbliższy" in queue_content:
                logger.critical("Sa wolne terminy!")
                logger.info(queue_content)
                self.send_email_notification(
                    subject="Wolne terminy paszportowe!",
                    body=f"Są dostępne wolne terminy:\n\n{queue_content}",
                    recipient=os.getenv("RECIPIENT_EMAIL"),
                    sender_email=os.getenv("SENDER_EMAIL"),
                    sender_password=os.getenv("SENDER_PASSWORD"),
                )
            else:
                logger.info("Kolejka paszportowa jest pełna")
        else:
            logger.error("Nie znaleziono elementu z 'UZ: PASZPORT - złożenie wniosku'")

    def send_email_notification(
        self,
        subject: str,
        body: str,
        recipient: str,
        sender_email: str,
        sender_password: str,
    ) -> None:
        try:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient, msg.as_string())

            logger.info(f"E-mail wysłany do {recipient}")
        except Exception as e:
            logger.error(f"Błąd przy wysyłaniu e-maila: {e}")
