from socket import * 
import os 
import sys 
import struct 
import time 
import select 
import binascii   
 
ICMP_ECHO_REQUEST = 8 


# my section !

def myChecksumFxn(header, data):
    print('\n\nbeginning of myChecksumFxn')
    print('#received header and data:')
    print(header.hex())
    print(data.hex())
    
    #for loop that iterates through 16 bits at a time
    # convert hex to integer to binary to integer to hex
    print('\npacket concat test')
    packet = header + data
    packet_hex = packet.hex()
    packet_int = int(packet.hex(), 16)
    print(hex(packet_int))

    print('\nbinary conversion test')
    packet_bin = bin(packet_int)
    print(packet_bin)

    print('\nget packet length')
    print('length:' + str(len(packet.hex())))


    sum = 0
    for i in range(0, len(packet), 2):
        # create bytes string with current bytes to add to sum
        byte_list = [packet[i], packet[i+1]] # add bytes to list
        current = bytearray(byte_list) # create byte array using list
        int_current = int(current.hex(), 16) # convert byte array to integer
        sum += int_current # add converted byte value to sum
        #check value of sum a bits to see if len > 16
        #if it is truncate and +1
        print(current.hex())
        print(int_current)
        #print(len(packet))
        print(sum)

        print("\n")




    print('end of myChecksumFxn\n\n')
# end my section

def checksum(string):  
    csum = 0 
    countTo = (len(string) // 2) * 2   
    count = 0 
	

    while count < countTo: 
        thisVal = ord(string[count+1]) * 256 + ord(string[count])   	 	
        csum = csum + thisVal   	 	
        csum = csum & 0xffffffff    	 	
        count = count + 2 
 	 
    if countTo < len(string): 
        csum = csum + ord(string[len(string) - 1])  	 	
        csum = csum & 0xffffffff  
 	 
    csum = (csum >> 16) + (csum & 0xffff)  	
    csum = csum + (csum >> 16)  	
    answer = ~csum   	
    answer = answer & 0xffff  
    answer = answer >> 8 | (answer << 8 & 0xff00) 
    return answer 
def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout 
 	 
    while 1:  
        startedSelect = time.time()  	 	
        whatReady = select.select([mySocket], [], [], timeLeft) 
        howLongInSelect = (time.time() - startedSelect)  	 	
        if whatReady[0] == []: # Timeout  	 	 	
            return "Request timed out." 
        timeReceived = time.time()   	 	
        recPacket, addr = mySocket.recvfrom(1024) 
        
        #Fill in start 
     
        #Fetch the ICMP header from the IP packet 
        print("print after receive")
    
        #Fill in end  	 	
        timeLeft = timeLeft - howLongInSelect  	 	
        if timeLeft <= 0: 
            return "Request timed out." 
 	 
def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16) 
        
    myChecksum = 0 
    # Make a demme header with a 0 checksum 
    # struct -- Interpret strings as packed binary data 
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1) 
    data = struct.pack("d", time.time()) 
 	# Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(str(header + data))
    #test code section
    myChecksumFxn(header, data)
    print('pre-system check checksum:')
    print(hex(myChecksum))
 	 
 	# Get the right checksum, and put in the header  	
    if sys.platform == 'darwin':
      # Convert 16-bit integers from host to network  byte order  	 	
      myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    print('post-system check checksum:')
    print(hex(myChecksum).encode())
 	 	 
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)  	
    packet = header + data 
    #print('#print out packet as hex:')
    #print(header.hex())
   # print(data.hex())
    #print('end datagram')

    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str 
 	# Both LISTS and TUPLES consist of a number of objects 
 	# which can be referenced by their position number within the object. 
 	 
def doOnePing(destAddr, timeout):   	
    icmp = getprotobyname("icmp") 
 	# SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process i  	
    sendOnePing(mySocket, destAddr, myID)  	
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)  
    mySocket.close() 
    return delay 
 	 
def ping(host, timeout=1):
 	# timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost  	
    dest = gethostbyname(host)  	
    #print("Pinging " + dest + " using Python:")
    #print("") 
 	# Send ping requests to a server separated by approximately one second
    while 1 :
        delay = doOnePing(dest, timeout) 
        print(delay) 
        time.sleep(1)# one second  	
        return delay 

ping("google.com")





