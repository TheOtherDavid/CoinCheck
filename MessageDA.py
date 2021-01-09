import smtplib
import configparser

config = configparser.ConfigParser()

class MessageDA:

    def send_message(self, message):
        # Read local file `config.ini`.
        config.read("settings.ini")

        # Instead of sending a text directly, we'll send one through e-mail.
        # This will ONLY work for Google Fi numbers currently. Possible enhancements include passing in the
        print(f'Starting send_message')
        number = config.get("personal", "phone_number")
        sms_domain = config.get("personal", "email_sms_domain")
        receiver = number + sms_domain
        sender = config.get("personal", "email_sender")
        login = config.get("personal", "email_login_name")
        password = config.get("personal", "email_login_pass")
        smtp_url = config.get("personal", "email_smtp_url")
        smtp_port = config.get("personal", "email_smtp_port")

        msg = message

        with smtplib.SMTP_SSL(smtp_url, smtp_port) as server:
            #server.set_debuglevel(1)
            server.login(login, password)
            print(f'Login successful')

            server.sendmail(sender, receiver, msg)
            print(f'Mail successful')
