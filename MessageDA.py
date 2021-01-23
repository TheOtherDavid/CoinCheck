import os
import smtplib


class MessageDA:

    def send_message(self, message):
        # Instead of sending a text directly, we'll send one through e-mail.
        print(f'Starting send_message')
        number = os.environ.get("phone_number")
        sms_domain = os.environ.get("email_sms_domain")
        receiver = number + sms_domain
        sender = os.environ.get("email_sender")
        login = os.environ.get("email_login_name")
        password = os.environ.get("email_login_pass")
        smtp_url = os.environ.get("email_smtp_url")
        smtp_port = os.environ.get("email_smtp_port")

        msg = message

        with smtplib.SMTP_SSL(smtp_url, smtp_port) as server:
            # server.set_debuglevel(1)
            server.login(login, password)
            print(f'Login successful')

            server.sendmail(sender, receiver, msg)
            print(f'Mail successful')
