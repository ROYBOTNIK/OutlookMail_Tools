# Microsoft Graph Email Functions

This project provides Python functions to interact with the Microsoft Graph API for sending and reading emails in Outlook, as well as managing email folders.

## Features

- Send emails with attachments
- Read emails with pagination
- Create email folders
- Move emails between folders
- Logging functionality
- Error handling

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/microsoft-graph-email.git
   cd microsoft-graph-email
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Microsoft Azure application:
   - Go to the Azure Portal (https://portal.azure.com/)
   - Create a new App Registration
   - Set the redirect URI to `https://login.microsoftonline.com/common/oauth2/nativeclient`
   - Under "Authentication", add a new platform of type "Mobile and desktop applications"
   - Set the redirect URI to `https://login.microsoftonline.com/common/oauth2/nativeclient`
   - Under "API permissions", add the following Microsoft Graph permissions:
     - Mail.Read
     - Mail.Send
     - MailboxSettings.Read
     - MailboxSettings.ReadWrite
   - Note down the Client ID and Tenant ID

4. Create a `.env` file in the project root with your credentials:
   ```plaintext
   MICROSOFT_CLIENT_ID=your_client_id_here
   MICROSOFT_TENANT_ID=your_tenant_id_here
   TEST_EMAIL_RECIPIENT=your_test_email@example.com
   ```

   Replace the placeholder values with your actual Microsoft Graph API credentials and test email address.

## Usage

Here's an example of how to use the email functions:

## Get access token
access_token = get_access_token()
## Send an email with attachment
subject = "Test Email"
body = "This is a test email sent using Microsoft Graph API."
to_recipients = ["recipient@example.com"]
attachments = [{
"@odata.type": "#microsoft.graph.fileAttachment",
"name": "test.txt",
"contentBytes": "SGVsbG8gV29ybGQh" # Base64 encoded content
}]
success = send_email(access_token, subject, body, to_recipients, attachments)
print(f"Email sent successfully: {success}")

## Read emails with pagination
emails = read_emails(access_token, top=20)
for email in emails:
print(f"Subject: {email['subject']}")
print(f"From: {email['from']['emailAddress']['address']}")
print(f"Received: {email['receivedDateTime']}")
print(f"Preview: {email['bodyPreview']}")
print("---")

## Create a new folder
folder_name = "Important Emails"
folder_id = create_folder(access_token, folder_name)
if folder_id:
print(f"Folder created with ID: {folder_id}")

## Move an email to the new folder
if emails and folder_id:
message_id = emails[0]['id']
success = move_email(access_token, message_id, folder_id)
print(f"Email moved successfully: {success}")


## Running Tests

To run the tests and see the functions in action, execute:

```bash
python test_setup.py
```

This script will:
1. Authenticate and get an access token
2. Read the latest 15 emails
3. Send a test email with an attachment
4. Create a new folder
5. Move an email to the new folder

## Logging

The functions include logging functionality. Logs are printed to the console and can be found in the application output.

## Error Handling

All functions include error handling and will log any errors that occur during execution.

## Note on Authentication

This project uses the device code flow for authentication, which is suitable for desktop or CLI applications. For web applications, you would need to implement a different authentication flow.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.