import os
import base64
import re
from html import unescape

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


def connect_gmail():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service


def get_emails(service, max_results=10):

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for message in messages:

        msg = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=["Subject", "From"]
        ).execute()

        headers = msg.get("payload", {}).get("headers", [])

        subject = "(No subject)"
        sender = ""

        for header in headers:

            name = header["name"].lower()
            value = header["value"]

            if name == "subject":
                subject = value

            elif name == "from":
                sender = value

        emails.append({
            "id": message["id"],
            "subject": subject,
            "sender": sender
        })

    return emails


def decode_email_body(data):

    if not data:
        return ""

    try:
        decoded = base64.urlsafe_b64decode(data)
        return decoded.decode("utf-8", errors="ignore")

    except Exception:
        return ""


def clean_html(html_text):

    # Remove scripts and styles
    html_text = re.sub(
        r"<(script|style).*?>.*?</\1>",
        "",
        html_text,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Replace common HTML line breaks
    html_text = re.sub(
        r"<br\s*/?>",
        "\n",
        html_text,
        flags=re.IGNORECASE
    )

    html_text = re.sub(
        r"</(p|div|tr|h1|h2|h3|li)>",
        "\n",
        html_text,
        flags=re.IGNORECASE
    )

    # Remove remaining HTML tags
    html_text = re.sub(
        r"<[^>]+>",
        "",
        html_text
    )

    # Convert HTML entities
    html_text = unescape(html_text)

    # Clean extra spaces and blank lines
    lines = []

    for line in html_text.splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_email_body(payload):

    plain_text = []
    html_text = []

    def process_part(part):

        mime_type = part.get("mimeType", "")
        body_data = part.get("body", {}).get("data")

        # Plain text
        if mime_type == "text/plain":

            if body_data:
                text = decode_email_body(body_data)

                if text.strip():
                    plain_text.append(text)

        # HTML
        elif mime_type == "text/html":

            if body_data:
                text = decode_email_body(body_data)

                if text.strip():
                    html_text.append(text)

        # Check nested parts
        for nested_part in part.get("parts", []):
            process_part(nested_part)

    process_part(payload)

    # Prefer plain text
    if plain_text:

        return "\n\n".join(plain_text).strip()

    # If no plain text, use HTML
    if html_text:

        combined_html = "\n\n".join(html_text)

        return clean_html(combined_html)

    return ""


def get_email(service, message_id):

    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = message.get("payload", {})

    headers = payload.get("headers", [])

    subject = "(No subject)"
    sender = ""

    for header in headers:

        name = header["name"].lower()
        value = header["value"]

        if name == "subject":
            subject = value

        elif name == "from":
            sender = value

    body = extract_email_body(payload)

    return {
        "id": message_id,
        "subject": subject,
        "sender": sender,
        "body": body
    }