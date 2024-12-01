import json
import os
import requests
from dotenv import load_dotenv

class OneSignalMailer:
    def __init__(self):
        # Load environment variables
        # load_dotenv()
        
        # Initialize configuration
        self.one_signal_app_id = os.getenv('ONESIGNAL_APP_ID')
        self.one_signal_api_key = os.getenv('ONESIGNAL_API_KEY')
        self.email_from = os.getenv('EMAIL_FROM')
        self.sender_name = os.getenv('SENDER_NAME')
        
        # Default email template
        self.email_template = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #333333; background-color: #f4f4f4;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                <tr>
                    <td style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 8px 8px 0 0;">
                        <h2 style="margin: 0; color: #2c3e50;">{subject}</h2>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 30px 20px; background-color: #ffffff;">
                        {message}
                    </td>
                </tr>
                <tr>
                    <td style="text-align: center; padding: 20px; color: #666666; font-size: 12px; background-color: #f8f9fa; border-radius: 0 0 8px 8px;">
                        <p style="margin: 0;">This email was sent by {sender_name}</p>
                        <p style="margin: 10px 0 0 0;">If you no longer wish to receive these emails, you can unsubscribe by replying with "UNSUBSCRIBE"</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        '''
        
        if not all([self.one_signal_app_id, self.one_signal_api_key, 
                   self.email_from, self.sender_name]):
            raise ValueError("Missing required environment variables. Please check .env file.")

    def set_email_template(self, template):
        """Update the email template"""
        self.email_template = template

    def get_email_template(self):
        """Get the current email template"""
        return self.email_template

    def send_mail(self, message, subject, recipient_email):
        # Format the HTML message using the template
        html_message = self.email_template.format(
            message=message,
            subject=subject,
            sender_name=self.sender_name
        )

        # Construct the request payload with improved parameters
        payload = {
            'app_id': self.one_signal_app_id,
            'contents': {'en': message},  # Plain text version
            'headings': {'en': subject},
            'email_from_name': self.sender_name,
            'email_from_address': self.email_from,
            'email_reply_to_address': self.email_from,
            'email_subject': subject,
            'include_email_tokens': [recipient_email],
            'email_body': html_message,  # HTML version
            'email_click_tracking': True,  # Enable click tracking
            'email_open_tracking': True,   # Enable open tracking
            'email_format': 'multipart/alternative',  # Send both HTML and plain text
        }

        # Set up request headers
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': f'Basic {self.one_signal_api_key}',
        }

        # Send the POST request
        response = requests.post(
            'https://onesignal.com/api/v1/notifications',
            data=json.dumps(payload),
            headers=headers
        )

        # Raise an exception for bad responses
        response.raise_for_status()
        
        return response.json()

def main():
    # Example usage
    try:
        mailer = OneSignalMailer()
        
        # Send a test email
        response = mailer.send_mail(
            message="Hello! This is a test email sent via OneSignal API.",
            subject="Test Email",
            recipient_email="recipient@example.com"
        )
        
        print("Email sent successfully!")
        print("Response:", json.dumps(response, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
