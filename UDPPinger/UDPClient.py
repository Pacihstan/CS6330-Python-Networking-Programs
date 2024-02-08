from socket import *
import time

server_nameport = ('127.0.0.1', 12000)
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(5)
sequence_number = 0
while sequence_number < 10:
    time_sent = time.time()
    sequence_number = sequence_number + 1
    message = "Ping " + str(sequence_number) + ' ' + str(time_sent)
    print(message)
    client_socket.sendto(message.encode(), server_nameport)
    try:
        return_message, server_address = client_socket.recvfrom(2048)
        time_received = time.time()
    except:
        print("Request Timed Out")
        continue
    RTT = str(time_received - time_sent)
    #print(return_message.decode() + ' received')
    print('RTT:' + RTT)
