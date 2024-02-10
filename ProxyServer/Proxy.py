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
    try:
        print(message.split()[1])
        filename = str(message.split()[1].replace(':443',''))
        print('successfully split messsage')
    except:
        print('#Failed to split message')
        filename = ''
    print('Filename:' +filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
        tcpCliSock.send(b"Content-Type:text/html\r\n")
        # Fill in start.
        
        #print('outputdata ' + outputdata)


        # Fill in end.
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        print('#entered except')
        if fileExist == "false":
            print('#entered if')
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            print('#created socket')
            hostn = filename.replace("www.","",1)
            print('Hostname: ' + hostn)
            try:
                print('#entering main try')
                # Connect to the socket to port 80
                c.connect((hostn.encode(),80))
                print('#connected on port 80')
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('wrb', None)
                print('write = ' + str(b"GET   "+b"http://"+filename.encode()+b"HTTP/1.0\n\n").decode())
                fileobj.write(b"GET  "+b"http://"+filename.encode()+b"HTTP/1.0\n\n")
                print('#created temporary file')
                # Read the response into buffer
                buffer = fileobj.readlines()
                print('#read response into buffer')

                # Create a new file in the cache for the requested file.
                #start
                response_file = open(b'./'+filename.encode(), 'w+b') #might have to change this to actually create a file
                print('#response file created')
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                for line in buffer:
                    response_file.write(line)
                    tcpCliSock.send(bytes(line, "utf-8"))
                print('#populated response file and sent')
                # Fill in start.
                # Fill in end.
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            print(placeholder)
            # Fill in start.
            # Fill in end.
    # Close the client and the server sockets
    #c.close()
        c.close()
tcpCliSock.close()
tcpSerSock.close()
    # Fill in start.
    # Fill in end
