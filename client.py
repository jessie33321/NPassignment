import socket

#create socket
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
clientSocket.bind(('0.0.0.0',68))

#Discover
OP = b'\x01'
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
Options = b'\x35\x01\x01\x32\x04\xc0\xa8\x01\x64'
end = b'\xff'
msg = OP+HTYPE+HLEN+HOPS+XID+SECS+FLAGS+CIADDR+YIADDR+SIADDR+GIADDR+CHADDR+padding+Magic_Cookie+Options+end

clientSocket.sendto(msg,('255.255.255.255', 67))

#Receive Offer 
clientSocket.recvfrom(2048)
print('Offer...')

#Request
OP = b'\x01'
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
Options = b'\x35\x01\x03\x32\x04\xc0\xa8\x01\x64\x36\x04\xc0\xa8\x01\x01'
end = b'\xff'
msg = OP+HTYPE+HLEN+HOPS+XID+SECS+FLAGS+CIADDR+YIADDR+SIADDR+GIADDR+CHADDR+padding+Magic_Cookie+Options+end

clientSocket.sendto(msg,('255.255.255.255', 67))

#Receive Ack
ack = clientSocket.recvfrom(2048)
print('Ack...')

print('\n----------configuration result-----------')
print('subnet mask: '+str(ack[0][245])+'.'+str(ack[0][246])+'.'+str(ack[0][247])+'.'+str(ack[0][248]))
print('router: '+str(ack[0][251])+'.'+str(ack[0][252])+'.'+str(ack[0][253])+'.'+str(ack[0][254]))

ltime = ack[0][257]*16*16 + ack[0][258]
ltime = ltime*16*16 + ack[0][259]
ltime = ltime*16*16 + ack[0][260]
print('IP lease time: ' + str(ltime) + ' secs')

print('DHCP server: '+str(ack[0][263])+'.'+str(ack[0][264])+'.'+str(ack[0][265])+'.'+str(ack[0][266]))
