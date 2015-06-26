#!/usr/bin/python
import subprocess
import sys
from zte import zte
from curses import ascii
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename
from email import Encoders
from email.mime.base import MIMEBase

if __name__ == "__main__":
	fileName = sys.argv[1]
	phoneNumber = "0882506400"
	smsText = "BHuMAHuE!"
	
	modem = zte.openModem('/dev/ttyUSB1', 2)
	zte.setModemTextMode(modem)
	zte.sendSMS(modem, phoneNumber, smsText)
	zte.closeModem(modem)
	FROM = "ico.borisov@gmail.com"	
	TO = "ico.borisov@gmail.com, bornel@abv.bg"
	MESSAGE = "BHuMAHuE!!!"

	msg = MIMEMultipart('related')
	msg["From"] = FROM
	msg["To"] = TO
	msg["Subject"] = MESSAGE + " - " + basename(fileName)
	msg.attach(MIMEText(MESSAGE))

	atPart = MIMEBase('application', "octet-stream")
	attach = open(fileName, 'rb')
	atPart.set_payload(attach.read())
	Encoders.encode_base64(atPart)
	atPart.add_header('Content-Disposition', 'attachment; filename="%s"' % basename(fileName))
	msg.attach(atPart)

	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.login("ico.borisov@gmail.com", "Em@1lPwD")
	msg.as_string()
	server.sendmail(FROM, TO, msg.as_string())
	server.close()
