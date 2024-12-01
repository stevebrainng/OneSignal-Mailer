# OneSignal Email Mailer by xioBrain

A simple Python program for sending emails using the OneSignal API service, with support for email templates and interval sending, and error handling. It includes a modern GUI interface for easy management of settings, templates, and email sending, I built this program in my leisure time.

## Features

- Modern GUI interface for all operations
- Environment-based configuration
- Simple API for sending emails
- Customizable email templates with HTML support
- Interval-based email sending
- Error handling and validation
- Proper response handling
- Real-time logging display

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file based on `.env.example` and fill in your OneSignal credentials:
```bash
cp .env.example .env
```

3. Edit the `.env` file with your actual credentials:
```
ONESIGNAL_APP_ID=your_app_id_here
ONESIGNAL_API_KEY=your_api_key_here
EMAIL_FROM=your_email@example.com
SENDER_NAME=Your Company Name
```

## Using the GUI

To start the GUI application:
```bash
python gui.py
```

The GUI consists of three main sections:

### 1. Settings
- Configure your OneSignal credentials
- Set email sender information
- All settings are saved automatically
- Access via the "Settings" button in the sidebar

### 2. Template Editor
- Create and edit HTML email templates
- Use placeholders: {message}, {subject}, {sender_name}
- Preview template formatting
- Save templates for future use
- Access via the "Template Editor" button in the sidebar

### 3. Email Sender
- Send emails to multiple recipients
- Set custom subject and message
- Configure sending intervals
- View real-time sending logs
- Start/stop email sending process
- Access via the "Main" button in the sidebar

## Programmatic Usage

You can also use the mailer programmatically:

```python
from onesignal_mailer import OneSignalMailer

# Initialize the mailer
mailer = OneSignalMailer()

# Send an email
response = mailer.send_mail(
    message="Hello! This is a test email.",
    subject="Test Email",
    recipient_email="recipient@example.com"
)

print("Email sent successfully!")
print(response)
```

## Template Customization

The default template includes:
- Responsive HTML design
- Clean, modern layout
- Support for custom styling
- Unsubscribe information
- Click and open tracking

To customize the template:
1. Open the Template Editor in the GUI
2. Edit the HTML template
3. Use placeholders: {message}, {subject}, {sender_name}
4. Click "Save" to store your changes

## Error Handling

The application includes comprehensive error handling:
- Validation of OneSignal credentials
- Template format verification
- Network error handling
- Real-time error logging
- User-friendly error messages

## Logging

All operations are logged in real-time:
- Email sending status
- Template changes
- Configuration updates
- Error messages
- Success confirmations

## Requirements

- Python 3.6+
- customtkinter
- requests
- python-dotenv
- Internet connection for OneSignal API access

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.
