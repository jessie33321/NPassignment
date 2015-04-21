import socket

#create socket
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
serverSocket.bind(('', 67))

#Receive Discover
serverSocket.recvfrom(2048)
print('Discover...')

#Offer
OP = b'\x02'
HTYPE = b'\x01'
HLEN = b'\x06'
HOPS = b'\x00'
XID = b'\x39\x03\xF3\x26'
SECS = b'\x00\x00'
FLAGS = b'\x00\x00'
CIADDR = b'\x00\x00\x00\x00'
YIADDR = b'\x00\x00\x00\x00'
SIADDR = b'\x00\x00\x00\x00'
GIADDR = b'\x00\x00\x00\x00'
CHADDR = b'\x00\x05\x3C\x04\x8D\x59'
padding = b'\x00' * (10+192)
Magic_Cookie = b'\x63\x82\x53\x63' 
Options = b'\x35\x01\x02\x01\x04\xff\xff\xff\x00\x03\x04\xc0\xa8\x01\x01\x33\x04\x00\x01\x51\x80\x36\x04\xc0\xa8\x01\x01'
end = b'\xff'
msg = OP+HTYPE+HLEN+HOPS+XID+SECS+FLAGS+CIADDR+YIADDR+SIADDR+GIADDR+CHADDR+padding+Magic_Cookie+Options+end

serverSocket.sendto(msg,('255.255.255.255',68))

#Receive Request
serverSocket.recvfrom(2048)
print('Request...')

#Ack
OP = b'\x02'
HTYPE = b'\x01'
HLEN = b'\x06'
HOPS = b'\x00'
XID = b'\x39\x03\xF3\x26'
SECS = b'\x00\x00'
FLAGS = b'\x00\x00'
CIADDR = b'\x00\x00\x00\x00'
YIADDR = b'\x00\x00\x00\x00'
SIADDR = b'\x00\x00\x00\x00'
GIADDR = b'\x00\x00\x00\x00'
CHADDR = b'\x00\x05\x3C\x04\x8D\x59'
padding = b'\x00' * (10+192)
Magic_Cookie = b'\x63\x82\x53\x63' 
Options = b'\x35\x01\x05\x01\x04\xff\xff\xff\x00\x03\x04\xc0\xa8\x01\x01\x33\x04\x00\x01\x51\x80\x36\x04\xc0\xa8\x01\x01'
end = b'\xff'
msg = OP+HTYPE+HLEN+HOPS+XID+SECS+FLAGS+CIADDR+YIADDR+SIADDR+GIADDR+CHADDR+padding+Magic_Cookie+Options+end

serverSocket.sendto(msg,('255.255.255.255',68))