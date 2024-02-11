# version of Proxy designed to find errors and test proxy without cache, but saves files
from socket import socket, AF_INET, SOCK_STREAM, gethostbyname

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', 8888))
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
    
    # handling of filename extraction cases
    if len(message) != 0:
        if ("http://" in message):
            filename = message.split()[1].split("/")[2]
        elif ("https://" in message):
            filename = message.split()[1].split("/")[2]
        elif "/" in message:
            filename = message.split()[1].split("/")[0]
        else:
            filename = message.split()[1]
    else:
        continue

    #this is a test, remove later
    if ":" in filename:
        port = filename.split(":")[1]
        print("Port:"+port)
        filename = filename.split(":")[0]


    print('Filename:' + filename)
    port = int(port)


    c = socket(AF_INET, SOCK_STREAM)
    hostn = filename.replace("www.", "", 1)
    print('Hostname:' + hostn)
    print("Host resolved IP:" + gethostbyname(hostn))


    #connect to site and send get request
    c.connect((gethostbyname(hostn),443))
    c.send(b"GET  "+b"https://"+filename.encode()+b" HTTP/1.0\n\n")

    # Receive and process HTTP response
    c.settimeout(3)
    response = b""
    while True:
        try:
            data = c.recv(1024)
            if not data:
                break
            tcpCliSock.send(data)
            response += data
        except:
            print('Timeout occurred...')
            break

    #print response
    print('Response message:' + response.decode())

    # Write response to file
    with open(filename, 'wb') as f:
        f.write(response)

    # Close client socket
    tcpCliSock.close()

# Close server socket
tcpSerSock.close()
