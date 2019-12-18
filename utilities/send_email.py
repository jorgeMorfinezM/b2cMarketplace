# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorgemorfinez@ofix.mx)"
__copyright__ = "Copyright 2019, Jorge Morfinez Mojica"
__license__ = "Ofix S.A. de C.V."
__history__ = """ """
__version__ = "1.19.I20.Prod ($Rev: 100 $)"


import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "monitoreo-ti@ofix.mx"
receiver_email = "ti@ofix.mx"
password = "Y*0am1%Oidfo9jYYVod&"

message = MIMEMultipart("alternative")
message["Subject"] = "Python Multipart Email Test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
This message is sending by Python"""

html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
# part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
# message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
         sender_email, receiver_email, message.as_string()
    )

message_2 = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message_2)

server.quit()

