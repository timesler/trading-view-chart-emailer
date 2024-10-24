import base64
import os
from pathlib import Path
from python_http_client.exceptions import HTTPError

import functions_framework
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    Disposition,
    Email,
    FileContent,
    FileName,
    FileType,
    Mail,
)

from chart_emailer.scrape import WebDriverManager


URLS_FILES = [
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=TVC%3AUSOIL", "oil.png"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=TVC%3AGOLD", "gold.png"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=ASX%3AXJO", "asx.png"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=FX%3AAUDUSD", "audusd.png"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=BMFBOVESPA%3APETR4", "petrobras.png"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=BMFBOVESPA%3AVALE3", "vale.png"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=SPREADEX%3ANIKKEI", "nikkei.png"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=TVC%3AHSI", "hangseng.png"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=NASDAQ%3ANDX", "nasdaq.png"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=SP%3ASPX", "sp500.png"),
    ("https://www.tradingview.com/chart/ry2ZLXIN/?symbol=NSE%3ANIFTY", "nifty.png"),
]
CALENDAR_URL = "https://www.fxstreet.com/economic-calendar"
TV_GUIDE_URL = "https://www.ourguide.com.au/tv_guide.php?r=melbourne&t=6"
BLOOMBERG_URL = "https://countryeconomy.com/stock-exchange"
CALENDAR_FILENAME = "economic-calendar.png"
TV_GUIDE_FILENAME = "tv-guide.png"
BLOOMBERG_FILENAME = "majorindices.png"


def encode_file_to_base64(filename):
    with filename.open("rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded


def create_attachment(manager, url, filename, save_path, width=None, height=None):
    print(f"Saving {url} to {filename}")
    result = manager.save_tradingview_chart_as_image(url, save_path / filename, width=width, height=height)

    if result:
        print(f"Preparing attachment for {save_path / filename}")
        attachment = Attachment()
        attachment.file_content = FileContent(encode_file_to_base64(save_path / filename))
        attachment.file_type = FileType("image/png")
        attachment.file_name = FileName(filename)
        attachment.disposition = Disposition("attachment")
        return attachment


def send_email(_):
    print("START cloud function")

    print("Loading SendGrid API Key")
    SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']

    print("Creating SendGrid client")
    client = SendGridAPIClient(SENDGRID_API_KEY)

    print("Clearing any existing image files")
    # save_path = Path("images")
    save_path = Path("/tmp/images")
    save_path.mkdir(exist_ok=True, parents=True)
    for path in save_path.glob("*.png"):
        print(f"Deleting {path}")
        path.unlink()

    print("Scraping URLs for charts and attaching to email")
    attachments = []
    manager = WebDriverManager()
    for url, filename in URLS_FILES:
        attachment = create_attachment(manager, url, filename, save_path)
        if attachment:
            attachments.append(attachment)

    print("Composing email")
    email_content = "Hey bro, here's today's charts"
    message = Mail(
        to_emails="229891.ESLER@connectcv.com.au",
        # to_emails="tim.esler+testing@gmail.com",
        from_email=Email("tim.esler@gmail.com", "Tim Esler"),
        subject="Daily charts",
        plain_text_content=email_content,
    )

    print("Adding attachments to email")
    message.attachment = attachments

    try:
        print("Sending email")
        response = client.send(message)
        print(f"{response.status_code = }")
        print(f"{response.body = }")
        print(f"{response.headers = }")
    except HTTPError as e:
        print(f"Sending email failed with error: {e}")
        print(e.message)

    attachments = []
    print("Attaching economic calendar")
    attachment = create_attachment(manager, CALENDAR_URL, CALENDAR_FILENAME, save_path, height=1080 * 4)
    if attachment:
        attachments.append(attachment)

    print("Attaching TV guide")
    attachment = create_attachment(
        manager,
        TV_GUIDE_URL,
        TV_GUIDE_FILENAME,
        save_path,
        width=1920 * 2,
        height=1080 * 7,
    )
    if attachment:
        attachments.append(attachment)

    print("Attaching Bloomberg stock overview")
    attachment = create_attachment(manager, BLOOMBERG_URL, BLOOMBERG_FILENAME, save_path, height=1080 * 2)
    if attachment:
        attachments.append(attachment)

    print("Composing email")
    email_content = "Hey bro, here's the rest of today's attachments"
    message = Mail(
        to_emails="229891.ESLER@connectcv.com.au",
        # to_emails="tim.esler+testing@gmail.com",
        from_email=Email("tim.esler@gmail.com", "Tim Esler"),
        subject="Daily charts",
        plain_text_content=email_content,
    )

    print("Adding attachments to email")
    message.attachment = attachments

    try:
        print("Sending email")
        response = client.send(message)
        print(f"{response.status_code = }")
        print(f"{response.body = }")
        print(f"{response.headers = }")
        return response.status_code
    except HTTPError as e:
        print(f"Sending email failed with error: {e}")
        print(e.message)

    manager.close_driver()


if __name__ == "__main__":
    send_email(None)
