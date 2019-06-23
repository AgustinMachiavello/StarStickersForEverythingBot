import smtplib, ssl, os, datetime

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

def SendEmailNotification(msg, sender_email, receiver_email):
    """Returns a Boolean

    Sends an email
    """
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = sender_email
    receiver_email = receiver_email
    password = 'aaa'
    save_time = datetime.datetime.now()
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)
    return True

# EXAMPLE
SendEmailNotification("this is a message", 'aaa@gmail.com', 'bbb@gmail.com')


