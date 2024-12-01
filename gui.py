import customtkinter as ctk
from tkinter import messagebox, scrolledtext
from onesignal_mailer import OneSignalMailer
import logging
from datetime import datetime
import os
import time
import threading
import json

# Set appearance mode and default color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class PageHeader(ctk.CTkFrame):
    def __init__(self, parent, title):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        
        # Title with custom styling
        self.title = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        self.title.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 5))
        
        # Separator line
        self.separator = ctk.CTkFrame(self, height=2, fg_color=("gray70", "gray30"))
        self.separator.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, mailer):
        super().__init__(parent)
        self.mailer = mailer
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header = PageHeader(self, "Settings")
        self.header.grid(row=0, column=0, sticky="ew")
        
        # Form Frame
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)
        
        # OneSignal App ID
        ctk.CTkLabel(form_frame, text="OneSignal App ID:").grid(row=0, column=0, sticky="w", padx=20, pady=10)
        self.app_id = ctk.CTkEntry(form_frame, width=300)
        self.app_id.grid(row=0, column=1, sticky="ew", padx=(0, 20), pady=10)
        
        # OneSignal API Key
        ctk.CTkLabel(form_frame, text="OneSignal API Key:").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.api_key = ctk.CTkEntry(form_frame, width=300)
        self.api_key.grid(row=1, column=1, sticky="ew", padx=(0, 20), pady=10)
        
        # Email From
        ctk.CTkLabel(form_frame, text="Email From:").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.email_from = ctk.CTkEntry(form_frame, width=300)
        self.email_from.grid(row=2, column=1, sticky="ew", padx=(0, 20), pady=10)
        
        # Sender Name
        ctk.CTkLabel(form_frame, text="Sender Name:").grid(row=3, column=0, sticky="w", padx=20, pady=10)
        self.sender_name = ctk.CTkEntry(form_frame, width=300)
        self.sender_name.grid(row=3, column=1, sticky="ew", padx=(0, 20), pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, pady=(0, 20))
        
        ctk.CTkButton(button_frame, text="Save", command=self.save_settings).pack(side="left", padx=0)
        
        # Load existing settings
        self.load_settings()
        
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.app_id.insert(0, settings.get('app_id', ''))
                self.api_key.insert(0, settings.get('api_key', ''))
                self.email_from.insert(0, settings.get('email_from', ''))
                self.sender_name.insert(0, settings.get('sender_name', ''))
        except FileNotFoundError:
            pass
    
    def save_settings(self):
        settings = {
            'app_id': self.app_id.get(),
            'api_key': self.api_key.get(),
            'email_from': self.email_from.get(),
            'sender_name': self.sender_name.get()
        }
        
        # Validate that all fields are filled
        if not all(settings.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
        
        messagebox.showinfo("Success", "Settings saved successfully!")

class TemplateEditorFrame(ctk.CTkFrame):
    def __init__(self, parent, mailer):
        super().__init__(parent)
        self.mailer = mailer
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header = PageHeader(self, "Email Template Editor")
        self.header.grid(row=0, column=0, sticky="ew")
        
        # Instructions
        instructions = ctk.CTkLabel(
            self, 
            text="Create and edit email templates. Use {name} as a placeholder for recipient names.",
            wraplength=600,
            justify="left"
        )
        instructions.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))
        
        # Template Editor
        self.template_editor = ctk.CTkTextbox(self, height=600)
        self.template_editor.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Load current template
        self.template_editor.insert("1.0", self.mailer.get_email_template())
        
        # Buttons Frame
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=3, column=0, pady=(0, 20))
        
        ctk.CTkButton(button_frame, text="Save", 
                     command=self.save_template).pack(side="left", padx=2)
        ctk.CTkButton(button_frame, text="Reset to Default",
                     command=self.reset_template, fg_color="red", hover_color="dark red").pack(side="left", padx=2)
    
    def save_template(self):
        template = self.template_editor.get("1.0", "end-1c").strip()
        if not template:
            messagebox.showerror("Error", "Template cannot be empty!")
            return
        
        try:
            # Verify template format
            test_str = template.format(
                message="Test message",
                subject="Test subject",
                sender_name="Test sender"
            )
            
            # Save template
            self.mailer.set_email_template(template)
            messagebox.showinfo("Success", "Template saved successfully!")
            
        except KeyError as e:
            messagebox.showerror("Error", f"Invalid placeholder in template: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving template: {str(e)}")
    
    def reset_template(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset to the default template?"):
            self.mailer = OneSignalMailer()  # This will load the default template
            self.template_editor.delete("1.0", "end")
            self.template_editor.insert("1.0", self.mailer.get_email_template())

class EmailSenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OneSignal Mailer")
        self.root.geometry("1000x800")
        
        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Initialize mailer first
        if not self.initialize_mailer():
            return
            
        # Create sidebar
        self.create_sidebar()
        
        # Create frames
        self.main_frame = ctk.CTkFrame(self.root)
        self.settings_frame = SettingsFrame(self.root, self.mailer)
        self.template_frame = TemplateEditorFrame(self.root, self.mailer)
        
        # Create main content
        self.create_main_content()
        
        # Set up logging
        self.setup_logging()
        
        # Load existing logs
        self.load_existing_logs()
        
        # Initialize flags
        self.stop_flag = False
        self.sending_thread = None
        
        # Show main frame by default
        self.show_frame("main")
        
    def create_sidebar(self):
        # Create sidebar frame
        sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # App Name
        app_name = ctk.CTkLabel(sidebar_frame, text="OneSignal Mailer",
                               font=ctk.CTkFont(size=20, weight="bold"))
        app_name.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Navigation Buttons
        ctk.CTkButton(sidebar_frame, text="Email Sender",
                     command=lambda: self.show_frame("main")).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(sidebar_frame, text="Template Editor",
                     command=lambda: self.show_frame("template")).grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkButton(sidebar_frame, text="Settings",
                     command=lambda: self.show_frame("settings")).grid(row=3, column=0, padx=20, pady=10)
        
    def show_frame(self, frame_name):
        # Hide all frames
        self.main_frame.grid_remove()
        self.settings_frame.grid_remove()
        self.template_frame.grid_remove()
        
        # Show selected frame
        if frame_name == "main":
            self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif frame_name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif frame_name == "template":
            self.template_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def create_main_content(self):
        # Main content frame
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header = PageHeader(self.main_frame, "Create Campaign")
        self.header.grid(row=0, column=0, sticky="ew")
        
        # Form Frame
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Recipients
        ctk.CTkLabel(form_frame, text="Recipients:").grid(row=0, column=0, sticky="w", padx=20, pady=10)
        self.recipients = ctk.CTkTextbox(form_frame, height=100)
        self.recipients.grid(row=0, column=1, sticky="ew", padx=(0, 20), pady=10)
        
        # Subject
        ctk.CTkLabel(form_frame, text="Subject:").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.subject = ctk.CTkEntry(form_frame)
        self.subject.grid(row=1, column=1, sticky="ew", padx=(0, 20), pady=10)
        
        # Message
        ctk.CTkLabel(form_frame, text="Message:").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.message = ctk.CTkTextbox(form_frame, height=200)
        self.message.grid(row=2, column=1, sticky="ew", padx=(0, 20), pady=10)
        
        # Interval
        interval_frame = ctk.CTkFrame(form_frame)
        interval_frame.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=10)
        
        ctk.CTkLabel(interval_frame, text="Interval (seconds):").pack(side="left", padx=(0, 10))
        self.interval = ctk.CTkEntry(interval_frame, width=100)
        self.interval.pack(side="left")
        self.interval.insert(0, "5")
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, bg_color="transparent")
        button_frame.grid(row=4, column=1, sticky="e", padx=(0, 20), pady=20)
        
        self.start_button = ctk.CTkButton(button_frame, text="Start Campaign", command=self.start_sending)
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = ctk.CTkButton(button_frame, text="Stop", command=self.stop_sending,
                                       fg_color="gray", state="disabled")
        self.stop_button.pack(side="left", padx=10)
        
        # Log Frame
        log_frame = ctk.CTkFrame(self.main_frame)
        log_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        ctk.CTkLabel(log_frame, text="Activity Log", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5), padx=10, anchor="w")
        
        self.log_viewer = ctk.CTkTextbox(log_frame, height=300)
        self.log_viewer.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def setup_logging(self):
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Set up logger
        self.logger = logging.getLogger('EmailSender')
        self.logger.setLevel(logging.INFO)

        # Create handlers
        log_file = os.path.join('logs', 'email_sender.log')
        file_handler = logging.FileHandler(log_file)
        
        # Create formatters
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)

    def load_existing_logs(self):
        try:
            log_file = os.path.join('logs', 'email_sender.log')
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    # Get last 50 lines of logs
                    lines = f.readlines()[-50:]
                    self.update_log_viewer(''.join(lines))
        except Exception as e:
            self.logger.error(f"Error loading existing logs: {str(e)}")

    def update_log_viewer(self, message):
        self.log_viewer.config(state="normal")
        self.log_viewer.insert(ctk.END, message)
        self.log_viewer.see(ctk.END)  # Scroll to the bottom
        self.log_viewer.config(state="disabled")

    def log_and_display(self, message, level='info'):
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {message}\n"
        
        # Log to file based on level
        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'warning':
            self.logger.warning(message)
            
        # Update log viewer
        self.update_log_viewer(log_message)

    def get_interval_seconds(self):
        try:
            value = float(self.interval.get())
            if value < 0:
                raise ValueError("Interval must be non-negative")
            return value
        except ValueError as e:
            raise ValueError("Please enter a valid number for the interval")

    def start_sending(self):
        # Get values from fields
        recipients = [email.strip() for email in self.recipients.get("1.0", ctk.END).splitlines() if email.strip()]
        subject_text = self.subject.get().strip()
        message_text = self.message.get("1.0", ctk.END).strip()

        # Validate inputs
        if not recipients:
            messagebox.showerror("Error", "Please enter at least one email address")
            self.log_and_display("Email sending failed: No recipients specified", 'error')
            return
        if not all([subject_text, message_text]):
            messagebox.showerror("Error", "Please fill in all fields")
            self.log_and_display("Email sending failed: Missing subject or message", 'error')
            return

        try:
            interval = self.get_interval_seconds()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.log_and_display(f"Email sending failed: {str(e)}", 'error')
            return

        # Disable input fields and send button, enable stop button
        self.recipients.config(state="disabled")
        self.subject.config(state="disabled")
        self.message.config(state="disabled")
        self.interval.config(state="disabled")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.stop_flag = False

        # Start sending thread
        self.sending_thread = threading.Thread(
            target=self.send_emails_with_interval,
            args=(recipients, subject_text, message_text, interval)
        )
        self.sending_thread.start()

    def stop_sending(self):
        self.stop_flag = True
        self.log_and_display("Stopping email sending process...", 'warning')

    def toggle_input_state(self, state):
        self.recipients.config(state=state)
        self.subject.config(state=state)
        self.message.config(state=state)
        self.interval.config(state=state)
        self.start_button.config(state=state)

    def send_emails_with_interval(self, recipients, subject_text, message_text, interval):
        total_recipients = len(recipients)
        success_count = 0
        failed_recipients = []

        try:
            self.log_and_display(f"Starting to send emails to {total_recipients} recipients with {interval} seconds interval")
            
            for i, recipient in enumerate(recipients, 1):
                if self.stop_flag:
                    self.log_and_display("Email sending process stopped by user", 'warning')
                    break

                self.log_and_display(f"Sending email to {recipient} ({i}/{total_recipients})...")
                
                try:
                    # Send email
                    response = self.mailer.send_mail(
                        message=message_text,
                        subject=subject_text,
                        recipient_email=recipient
                    )
                    success_count += 1
                    self.log_and_display(f"Successfully sent email to {recipient}")
                    
                    # Wait for interval if not the last email and not stopped
                    if i < total_recipients and not self.stop_flag:
                        self.log_and_display(f"Waiting {interval} seconds before sending next email...")
                        time.sleep(interval)
                        
                except Exception as e:
                    error_msg = f"Failed to send email to {recipient}: {str(e)}"
                    failed_recipients.append(f"{recipient} ({str(e)})")
                    self.log_and_display(error_msg, 'error')

            # Show results
            if success_count == total_recipients:
                success_msg = f"All {success_count} emails sent successfully!"
                messagebox.showinfo("Success", success_msg)
                self.log_and_display(success_msg)
                # Clear fields only if all emails were sent successfully
                self.recipients.delete("1.0", ctk.END)
                self.subject.delete(0, ctk.END)
                self.message.delete("1.0", ctk.END)
            else:
                failed_msg = "\n".join(failed_recipients)
                partial_msg = f"Successfully sent {success_count} out of {total_recipients} emails."
                messagebox.showwarning("Partial Success", f"{partial_msg}\n\nFailed recipients:\n{failed_msg}")
                self.log_and_display(f"{partial_msg} Failed recipients: {failed_msg}", 'warning')
            
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.log_and_display(error_msg, 'error')
        
        finally:
            # Re-enable input fields and send button, disable stop button
            self.toggle_input_state("normal")
            self.stop_button.config(state="disabled")
            self.stop_flag = False

    def initialize_mailer(self):
        try:
            if not os.path.exists('settings.json'):
                messagebox.showwarning("Settings Required", "Please configure your settings first.")
                self.show_frame("settings")
                return
            
            with open('settings.json', 'r') as f:
                settings = json.load(f)
            
            os.environ['ONESIGNAL_APP_ID'] = settings['app_id']
            os.environ['ONESIGNAL_API_KEY'] = settings['api_key']
            os.environ['EMAIL_FROM'] = settings['email_from']
            os.environ['SENDER_NAME'] = settings['sender_name']
            
            self.mailer = OneSignalMailer()
            return True
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            messagebox.showerror("Configuration Error", str(e))
            return False

def main():
    root = ctk.CTk()
    app = EmailSenderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
