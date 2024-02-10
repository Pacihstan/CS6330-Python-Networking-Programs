from socket import *

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('',8888))
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

    #extract filename
    try: 
        print(message.split()[1])
        filename = str(message.split()[1]).replace('http://','')
        print('successfully split message')
    except:
        print('#Failed to split message')
        filename = ''
    print('Filename:'+filename)
    filetouse = "/" + filename
    print(filetouse)
    c = socket(AF_INET, SOCK_STREAM)
    hostn = filename.replace("www.","",1)
    print('Hostname: ' + hostn)
    c.connect((hostn,80))
    #fix here so that transport endpoint is open




    fileobj = c.makefile('wrb', None)
    fileobj.write(b"GET  "+b"http://"+filename.encode()+b"HTTP/1.0\n\n")
    buffer = fileobj.readlines()


    response_file = open(b'./'+filename.encode(), 'w+b')
    for line in buffer:
        response_file.write(line)
        tcpCliSock.send(bytes(line, "utf-8"))

tcpCliSock.close()
tcpSerSock.close()
c.close()
