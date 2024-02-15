from socket import * 
import os 
import sys 
import struct 
import time 
import select 
import binascii   
 
ICMP_ECHO_REQUEST = 8 

def myChecksumFxn(header, data):
    packet = header + data
    sum = 0
    for i in range(0, len(packet), 2):
        # create bytes string with current bytes to add to sum
        byte_list = [packet[i], packet[i+1]] # add bytes to list
        current = bytearray(byte_list) # create byte array using list
        int_current = int(current.hex(), 16) # convert byte array to integer 
        sum+= int_current#add to sum
        binary_sum = bin(sum)#convert sum to binary
        #check value of sum bits to see if len > 16
        binary_sum_string = str(binary_sum).replace('0b','')
        if len(binary_sum_string) > 16:#if it is truncate and +1
            #truncate string
            binary_sum_string = binary_sum_string[1:]
            #convert back to int and add 1
            sum = int(binary_sum_string, 2) + 1
 
    #pad sum with zeroes if len < 16
    binary_sum_string = str(bin(sum)).replace('0b','')
    if len(binary_sum_string) < 16:
        binary_sum_string = binary_sum_string.zfill(16)
    #create checksum
    #for loop that creates an inverted string version of the final sum and convert back to binary and then to hex
    #create string to represent checksum
    checksum_string = ''
    for k in range(len(binary_sum_string)):
        if binary_sum_string[k] == '0':
            checksum_string+='1'
        elif binary_sum_string[k] == '1':
            checksum_string+='0'
        else:
            print('Invalid value in sum...')
            continue
    #convert to hex
    checksum_hex = ''
    for i in range(0,len(checksum_string), 4):
        current = ''
        for k in range(4):
            current+=checksum_string[i+k]
        nibble_int = int(current,2)
        checksum_hex += str(hex(nibble_int)).replace('0x','')
    checksum_byte_array = bytearray([int(checksum_hex[0],16), int(checksum_hex[1],16), int(checksum_hex[2],16), int(checksum_hex[3], 16)])
    checksum_final = int(checksum_hex, 16)
    return(checksum_final)


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
        ICMP_type = recPacket[20]
        ICMP_code = recPacket[21]
        ICMP_checksum = recPacket[22:24].hex()
        ICMP_identifier = int(recPacket[24:26].hex(), 16)
        ICMP_seq = int(recPacket[26:28].hex(), 16)
        ttl = recPacket[8] 
        

        print('reply from ' + str(addr[0]) + ': icmp_seq=' + str(ICMP_seq) + ' ttl=' + str(ttl),end='')
        #ICMP starts at index 20
        #for k in range(0,len(recPacket),1):
            #print(str(k) + ':' + str(hex(recPacket[k])))

    
        #Fill in end  	 	
        timeLeft = timeLeft - howLongInSelect  	 	
        if timeLeft <= 0: 
            return "Request timed out." 
        else: return howLongInSelect
 	 
def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16) 
        
    myChecksum = 0 
    # Make a demme header with a 0 checksum 
    # struct -- Interpret strings as packed binary data 
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1) 
    data = struct.pack("d", time.time()) 
 	# Calculate the checksum on the data and the dummy header.
    myChecksum = myChecksumFxn(header, data)
     	 
 	# Get the right checksum, and put in the header  	
    if sys.platform == 'darwin':
      # Convert 16-bit integers from host to network  byte order  	 	
      myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
     	 	 
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)  	
    packet = header + data 

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
    print("Pinging " + dest + " using Python:")
    print("") 
 	# Send ping requests to a server separated by approximately one second
    while 1 :
        delay = doOnePing(dest, timeout) 
        print(' time=' + str(delay*1000)+ ' ms') 
        time.sleep(1)# one second  	
        #return delay 

ping(sys.argv[1])





