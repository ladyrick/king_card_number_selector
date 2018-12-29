import smtplib
from email.mime.text import MIMEText
from email.header import Header

from config import mail_user, mail_pass, mail_host


def smtp_send(subject, msg):
    sender = mail_user
    receivers = [mail_user]  # send to yourself

    message = MIMEText(str(msg), "plain", "utf-8")
    message["From"] = mail_user
    message["To"] = mail_user
    message["Subject"] = subject

    try:
        with smtplib.SMTP_SSL(mail_host, 465) as smtpObj:
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except:
        return False


if __name__ == "__main__":
    smtp_send("Python smtp test.")
