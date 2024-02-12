from socket import *
import sys
if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('',8888))
tcpSerSock.listen(5)
while True:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    # start
    try:
        message = tcpCliSock.recv(1024).decode() 
        print(message)
    except:
        print('#failed to decode message')
        continue
    # Extract the filename from the given message
    if len(message) != 0:
        if("http://" in message):
            filename = message.split()[1].split("/")[2]
        elif "/" in message:
            filename = message.split()[1].split("/")[0]
        else:
            filename = message.split[1]
    else:
        continue

    # Extract the port from the given message
    port = 80
    if ':' in filename:
        port = filename.split(':')[1]
        filename = filename.split(":")[0]
    # Continue if port is not 80
    if port != 80:
        print('Not using port 80. Skipping...')
        continue

    print('Filename:' +filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:], "rb")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
        tcpCliSock.send(b"Content-Type:text/html\r\n")
        # Fill in start.
        # iterate throught 
        for line in outputdata:
            tcpCliSock.send(line)

        # Fill in end.
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.","",1)
            print('Hostname:' + hostn)
            try:
                # Connect to the socket to port 80
                c.connect((gethostbyname(hostn),port))
            
                # Send traffic to target host
                c.sendall(message.encode())

                # Receive HTTP response
                c.settimeout(10)
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

                # Create a new file in the cache for the requested file.
                with open(b'./'+filename.encode(), 'w+b') as f:
                    f.write(response)
                print('Response: ' + response.decode())

            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            # Fill in start.
            tcpCliSock.send(b"HTTP/1.0 404 Not Found\r\n") 
            tcpCliSock.send(b"Content-Type:text/html\r\n")  
            tcpCliSock.send(b"\r\n")  
            tcpCliSock.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n") 
    # Close the client and the server sockets
tcpCliSock.close()
tcpSerSock.close()
