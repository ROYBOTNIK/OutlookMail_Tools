import requests

BASE_URL = 'https://graph.microsoft.com/v1.0/me'

def create_draft_message(access_token, message):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f'{BASE_URL}/messages', json=message, headers=headers)
    response.raise_for_status()
    return response.json()['id']

def send_draft_message(access_token, message_id):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(f'{BASE_URL}/messages/{message_id}/send', headers=headers)
    response.raise_for_status()

def create_and_send_message(access_token, message):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {'message': message}
    response = requests.post(f'{BASE_URL}/sendMail', json=payload, headers=headers)
    response.raise_for_status()

def send_email_example(access_token):
    message = {
        'subject': 'Test Email',
        'body': {
            'contentType': 'Text',
            'content': 'This is a test email sent using Microsoft Graph API.'
        },
        'toRecipients': [
            {
                'emailAddress': {
                    'address': 'recipient@example.com'
                }
            }
        ]
    }

    try:
        # Method 1: Create draft and then send
        draft_id = create_draft_message(access_token, message)
        send_draft_message(access_token, draft_id)
        print('Email sent successfully (draft method)')

        # Method 2: Create and send in one operation
        create_and_send_message(access_token, message)
        print('Email sent successfully (single operation method)')
    except requests.exceptions.RequestException as e:
        print(f'Error sending email: {e}')

# Usage example
if __name__ == '__main__':
    access_token = 'your_access_token_here'
    send_email_example(access_token)