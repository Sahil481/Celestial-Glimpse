from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


class EmailSender:
    def __init__(self, sender_email, password, smtp_server='smtp.gmail.com', smtp_port=587):
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, to_email, subject, message, url):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        html_file = open("../Pages/APOD.html", "r")
        html_content = html_file.read()
        html_file.close()

        html_content = html_content.replace("{hdurl}", url)
        html_content = html_content.replace("{DESC}", message)

        # Create a MIMEText object for the HTML message
        html_part = MIMEText(html_content, 'html')

        # Attach the HTML message to the email message
        msg.attach(html_part)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, to_email, msg.as_string())

    def send_verification_create_email(self, to_email, subject, url):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        html_file = open("../Pages/verify_create.html", "r")
        html_content = html_file.read()
        html_file.close()

        html_content = html_content.replace("INSERT_VERIFICATION_LINK_HERE", url)

        # Create a MIMEText object for the HTML message
        html_part = MIMEText(html_content, 'html')

        # Attach the HTML message to the email message
        msg.attach(html_part)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, to_email, msg.as_string())

    def send_verification_delete_email(self, to_email, subject, url):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        html_file = open("../Pages/verify_delete.html", "r")
        html_content = html_file.read()
        html_file.close()

        html_content = html_content.replace("INSERT_UNSUBSCRIPTION_LINK_HERE", url)

        # Create a MIMEText object for the HTML message
        html_part = MIMEText(html_content, 'html')

        # Attach the HTML message to the email message
        msg.attach(html_part)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, to_email, msg.as_string())
