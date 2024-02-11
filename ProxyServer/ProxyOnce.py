from socket import socket, AF_INET, SOCK_STREAM

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', 8887))
tcpSerSock.listen(5)

while True:
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
    filename = ''
    port = 80
    try:
        if ("http://" in message):
            filename = message.split()[1].split("/")[3]
        elif ("https://" in message):
            filename = message.split()[1].split("/")[3]
        elif "/" in message:
            filename = message.split()[1].split("/")[0]
        else:
            filename = message.split()[1]
        #this is a test, remove later
        port = filename.split(":")[1]
        print("Port:"+port)
        filename = filename.split(":")[0]
        print('successfully split message')
    except:
        print('#Failed to split message')
        filename = ''
        continue
    print('Filename:' + filename)
    port = int(port)


    c = socket(AF_INET, SOCK_STREAM)
    hostn = filename.replace("www.", "", 1)
    print('Hostname:' + hostn)
    #c.connect((hostn.encode(), port))
    #c.send(message.encode())

    #test a perfectly reasonable exchange
    c.connect((hostn,port))
    c.send(b"GET / HTTP/1.1\r\nHost:https://"+hostn.encode()+b"\r\n\r\n")

    # Formulate and send HTTP request
    #request = message
    #c.sendall(request.encode())

    # Receive and process HTTP response
    c.settimeout(3)
    response = b""
    while True:
        try:
            data = c.recv(1024)
            if not data:
                break
            response += data
        except:
            print('Timeout occurred...')
            break

    #print response
    print('Response message:' + response.decode())

    # Send response to client
    tcpCliSock.sendall(response)

    # Write response to file
    with open(filename, 'wb') as f:
        f.write(response)

    # Close client socket
    tcpCliSock.close()

# Close server socket
tcpSerSock.close()
