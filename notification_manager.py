import smtplib
import os
from twilio.rest import Client


class NotificationManager:

    def __init__(self):
        # Initialize the Twilio Client using your SID and Token
        self.client = Client(os.environ['TWILIO_SID'], os.environ["TWILIO_AUTH_TOKEN"])
        self.email = os.environ["MY_EMAIL"]
        self.email_password = os.environ["MY_EMAIL_PASSWORD"]
        # Removed the duplicate self.client definition from here
    def send_sms(self, message_body):
        """
        Sends an SMS using TWILIO_FROM (your Twilio number)
        and TWILIO_TO (your personal verified number).
        """
        message = self.client.messages.create(
            from_=os.environ["TWILIO_FROM"],
            body=message_body,
            to=os.environ["TWILIO_TO"]
        )
        # Prints the unique Message SID to confirm it was sent
        print(f"SMS Sent successfully: {message.sid}")

    def send_emails(self, email_list, email_body):
        """Connects to SMTP server, logs in, and fires emails to the customer list."""
        # Spin up the connection context right here so it safely cleans up per execution
        with smtplib.SMTP(os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"], port=587) as connection:
            connection.starttls()
            connection.login(self.email, self.email_password)

            for email in email_list:
                connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )
        print("Emails sent successfully to all subscribers!")

