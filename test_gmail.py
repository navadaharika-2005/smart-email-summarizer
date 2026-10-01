from gmail_service import connect_gmail, search_emails

print("Connecting to Gmail...")

service = connect_gmail()

print("Gmail connection successful!")

emails = search_emails(service, query="in:inbox", max_results=5)

print("\nLatest inbox emails:")

for email in emails:
    print("------------------------------")
    print("Sender:", email["sender"])
    print("Subject:", email["subject"])
    print("Date:", email["date"])
    print("Preview:", email["snippet"])

print("\nGmail test completed.")