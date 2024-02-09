import smtplib
from email.mime.text import MIMEText


endmsg = "\r\n.\r\n"


msg = "\r\n I love computer networks!"
sender = "pax@isphere.net"
recipient = "placeholder"
password = "placeholder"

msg = MIMEText(msg)
msg['Subject'] = "SMTP Test"
msg['From'] = 'pax@isphere.net'
msg['To'] = 'pax@isphere.net'

smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.starttls()
smtp_server.login(sender, password)
smtp_server.sendmail(sender,recipient, msg.as_string())





# used https://mailtrap.io/blog/python-send-email-gmail/ to learn smtplib syntax
