from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerSock.bind((sys.argv[1], 8888))  # Assuming port 8888 for the proxy server
tcpSerSock.listen(5)  # Listen for incoming connections, up to 5 queued connections
# Fill in end.

while True:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()  # Fill in start. Receive data from client socket
    # Fill in end.
    print(message)

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)

    try:
        # Check whether the file exists in the cache
        f = open(filetouse[1:], "rb")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
        tcpCliSock.send(b"Content-Type:text/html\r\n")
        tcpCliSock.send(b"\r\n")
        for i in range(len(outputdata)):
            tcpCliSock.send(outputdata[i])
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            print(hostn)
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                fileobj.write("GET /HTTP/1.0\n\n".encode())  # Ensure to encode the string to bytes
                # Read the response into buffer
                buff = fileobj.readlines()
                # Create a new file in the cache for the requested file.
                tmpFile = open("./" + filename, "wb")
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                for line in buff:
                    tcpCliSock.send(line)
                    tmpFile.write(line)
                print('Requested file sent')
            except Exception as e:
                print("Illegal request:", e)
        else:
            # HTTP response message for file not found
            tcpCliSock.send(b"HTTP/1.0 404 Not Found\r\n")
            tcpCliSock.send(b"Content-Type:text/html\r\n")
            tcpCliSock.send(b"\r\n")
            tcpCliSock.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")

    # Close the client and the server sockets
    tcpCliSock.close()

# Close the server socket
tcpSerSock.close()

