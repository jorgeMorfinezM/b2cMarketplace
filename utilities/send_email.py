# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorgemorfinez@ofix.mx)"
__copyright__ = "Copyright 2019, Jorge Morfinez Mojica"
__license__ = "Ofix S.A. de C.V."
__history__ = """ """
__version__ = "1.19.L20.Prod ($Rev: 100 $)"


import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from constants.constants import Constants as Const

# port = 465  # For SSL
# smtp_server = "smtp.gmail.com"
# sender_email = "monitoreo-ti@ofix.mx"
# receiver_email = "ti@ofix.mx"
# password = "Y*0am1%Oidfo9jYYVod&"


# Define y obtiene el configurador para las constantes del sistema:
def get_config_constant_file():
    """
        Contiene la obtencion del objeto config
        para setear datos de constantes en archivo
        configurador

    :rtype: object
    """

    # TEST
    _constants_file = "constants/constants.yml"

    # PROD
    # _constants_file = "/ofix/tienda_virtual/parserCt/constants/constants.yml"

    cfg = Const.get_constants_file(_constants_file)

    return cfg


cfg = get_config_constant_file()

port = cfg['EMAIL_SETTINGS']['PORT']
smtp_server = cfg['EMAIL_SETTINGS']['SMTP_SERVER']
sender_email = cfg['EMAIL_SETTINGS']['SENDER_EMAIL']
receiver_email = cfg['EMAIL_SETTINGS']['RECEIVER_EMAIL']
password = cfg['EMAIL_SETTINGS']['PASSWORD']

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

