from socket import *
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.gmail.com"
s = smtplib.SMTP('smtp.gmail.com', 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver,587))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFromCommand = 'MAIL FROM: pax@isphere.net\r\n'
clientSocket.send(mailFromCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

# Send RCPT TO command and print server response.
rcptCommand = 'RCPT TO pax@isphere.net\r\n'
clientSocket.send(rcptCommand.encode())


# Send DATA command and print server response.
dataCommand = """DATA\r\n',
            Date: Sun, 30 Nov 98 nn:nn:nn EST\r\n,
            From: Paxton <pax@isphere.net>\r\n,
            To: <pax@isphere.net>\r\n,
            Subject: Test\r\n\r\n,
            This is a test message.\r\n"""

# Send message data.
clientSocket.send(dataCommand.encode())

# Message ends with a single period.
clientSocket.send('.\r\n'.encode())

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
