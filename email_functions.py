import requests
import json
import logging
from typing import List, Dict, Optional

BASE_URL = "https://graph.microsoft.com/v1.0"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_email(access_token: str, subject: str, body: str, to_recipients: List[str], attachments: Optional[List[Dict]] = None) -> bool:
    endpoint = f"{BASE_URL}/me/sendMail"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    email_body = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [{"emailAddress": {"address": recipient}} for recipient in to_recipients]
        }
    }
    
    if attachments:
        email_body["message"]["attachments"] = attachments

    try:
        response = requests.post(endpoint, headers=headers, json=email_body)
        response.raise_for_status()
        logger.info(f"Email sent successfully to {', '.join(to_recipients)}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send email: {str(e)}")
        logger.error(f"Response content: {e.response.content if e.response else 'No response content'}")
        return False

def read_emails(access_token: str, top: int = 10, skip: int = 0) -> List[Dict]:
    endpoint = f"{BASE_URL}/me/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    all_emails = []
    while True:
        params = {
            "$top": min(top - len(all_emails), 1000),
            "$skip": skip,
            "$select": "subject,from,receivedDateTime,bodyPreview"
        }
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            emails = data.get("value", [])
            all_emails.extend(emails)
            skip += len(emails)
            
            if len(all_emails) >= top or "@odata.nextLink" not in data:
                break
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve emails: {str(e)}")
            break
    
    logger.info(f"Retrieved {len(all_emails)} emails")
    return all_emails[:top]

def create_folder(access_token: str, folder_name: str) -> Optional[str]:
    endpoint = f"{BASE_URL}/me/mailFolders"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "displayName": folder_name
    }
    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        folder_id = response.json().get("id")
        logger.info(f"Created folder '{folder_name}' with ID: {folder_id}")
        return folder_id
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create folder: {str(e)}")
        return None

def move_email(access_token: str, message_id: str, folder_id: str) -> bool:
    endpoint = f"{BASE_URL}/me/messages/{message_id}/move"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "destinationId": folder_id
    }
    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        logger.info(f"Moved message {message_id} to folder {folder_id}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to move message: {str(e)}")
        return False