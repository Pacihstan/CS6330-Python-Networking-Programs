from socket import socket, AF_INET, SOCK_STREAM

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', 8888))
tcpSerSock.listen(5)

for i in range(5):
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received connection from:', addr)
    try:
        message = tcpCliSock.recv(1024).decode()
        print(message)
    except:
        print('#failed to decode message')
        continue

    # Extract filename
    try:
        print(message.split()[1])
        filename = message.split()[1].split("/")[1]
        print('successfully split message')
    except:
        print('#Failed to split message')
        filename = ''
    print('Filename:' + filename)

    c = socket(AF_INET, SOCK_STREAM)
    hostn = filename.replace("www.", "", 1)
    print('Hostname: ' + hostn)
    c.connect((hostn, 80))

    # Formulate and send HTTP request
    request = "GET /" + filename + " HTTP/1.1\r\nHost: " + hostn + "\r\n\r\n"
    c.sendall(request.encode())

    # Receive and process HTTP response
    response = b""
    while True:
        data = c.recv(1024)
        if not data:
            break
        response += data

    # Send response to client
    tcpCliSock.sendall(response)

    # Write response to file
    with open(filename, 'wb') as f:
        f.write(response)

    # Close client socket
    tcpCliSock.close()

# Close server socket
tcpSerSock.close()
