from auth import get_access_token
from email_functions import read_emails, send_email, create_folder, move_email
import os
from dotenv import load_dotenv
import base64
import time
import random
import string

# Load environment variables
load_dotenv()

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def main():
    access_token = get_access_token()
    if access_token:
        print("Successfully obtained access token.")
        
        # Test reading emails with pagination
        emails = read_emails(access_token, top=15)
        if emails:
            print(f"Successfully retrieved {len(emails)} emails.")
            for email in emails:
                print(f"Subject: {email['subject']}")
        else:
            print("Failed to retrieve emails.")
        
        # Test sending an email with attachment
        test_email_recipient = os.getenv("TEST_EMAIL_RECIPIENT")
        if test_email_recipient:
            # Generate a unique subject to avoid duplicate email detection
            subject = f"Test Email from Graph API with Attachment - {generate_random_string(8)}"
            body = f"This is a test email sent using Microsoft Graph API with an attachment. Timestamp: {time.time()}"
            to_recipients = [test_email_recipient]
            
            # Create a simple text file as an attachment
            attachment_content = f"This is a test attachment. Timestamp: {time.time()}"
            
            attachments = [{
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": "test_attachment.txt",
                "contentBytes": base64.b64encode(attachment_content.encode()).decode()
            }]
            
            success = send_email(access_token, subject, body, to_recipients, attachments)
            if success:
                print(f"Successfully sent test email with attachment to {test_email_recipient}")
            else:
                print(f"Failed to send test email to {test_email_recipient}")
        else:
            print("TEST_EMAIL_RECIPIENT not set in .env file")
        
        # Test creating a folder and moving an email
        folder_name = f"Test Folder {generate_random_string(8)}"
        folder_id = create_folder(access_token, folder_name)
        if folder_id:
            print(f"Successfully created folder: {folder_name}")
            
            # Move the first email to the new folder
            if emails:
                message_id = emails[0]['id']
                success = move_email(access_token, message_id, folder_id)
                if success:
                    print(f"Successfully moved email to folder: {folder_name}")
                else:
                    print("Failed to move email to folder")
            else:
                print("No emails available to move")
        else:
            print("Failed to create folder")
    else:
        print("Failed to obtain access token.")

if __name__ == "__main__":
    main()