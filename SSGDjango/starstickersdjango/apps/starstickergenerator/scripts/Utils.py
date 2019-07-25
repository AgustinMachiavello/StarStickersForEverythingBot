# Threading
import threading

# Email sending library
from django.core.mail import send_mail

"""
Originaly thought to be helpul to inform via email if an automated
post was successfully posted.
As Facebook no loger allows automated post, this script is just and extra
"""

# Basic steps:
# 1- Get and save Reddit Comments
# 2- Generate random phrase with Markov Chains
# 3- Generate star sticker with generated phrase
# 4- Post to Facebook
# 5- Send Email notification

# Credentials
from ..credentials import EMAIL_CREDENTIALS

IMAGE_POSTED_TEMPLATE = """
<html>                 
<h2 style="font-family:Arial;color:royalblue">
Image successfully posted at {0} by {1} containing: '{2}' | MKV state {3}
</h2>
</html>
"""


def send_email_notification(data):
    """Returns a Boolean

    Sends an email every time an image is posted
    """
    subject = 'StarStickersBot2001: Image successfully posted'
    body = IMAGE_POSTED_TEMPLATE.format(
        data['date'], data['user'], data['sentence'], data['markov_state'])
    send_mail(
        subject,
        message="",
        html_message=body,
        from_email=EMAIL_CREDENTIALS['default_from_email'],
        recipient_list=[EMAIL_CREDENTIALS['receiver_email']])
    return True


class SendEmailThread(threading.Thread):
    data = None
    subject = 'StarStickersBot2001: Image successfully posted'

    def __init__(self, data):
        self.data = data
        threading.Thread.__init__(self)

    def SendEmailNotification(self, data):
        """Returns a Boolean

        Sends an email every time an image is posted
        """
        body = IMAGE_POSTED_TEMPLATE.format(
            data['date'], data['user'], data['sentence'], data['markov_state'])
        send_mail(
            self.subject,
            message="",
            html_message=body,
            from_email=EMAIL_CREDENTIALS['default_from_email'],
            recipient_list=[EMAIL_CREDENTIALS['receiver_email']])
        return True

    def run(self):
        self.SendEmailNotification(self.data)
        return

    def start(self):
        self.run()
        return

# EXAMPLE
# SendEmailNotification(data, 'aaa@gmail.com', 'bbb@gmail.com')
