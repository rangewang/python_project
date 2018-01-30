import socket
import struct
from uuid import getnode as get_mac
from random import randint

def getMacInBytes():
    mac = str(hex(get_mac()))
    mac = mac[2:]
    while len(mac) < 12 :
        mac = '0' + mac
    macb = b''
    for i in range(0, 12, 2) :
        m = int(mac[i:i + 2], 16)
        macb += struct.pack('!B', m)
    return macb

class DHCPOfferPack:
    def __init__(self):
        self.transactionID = b''
        for i in range(4):
            t = randint(0, 255)
            self.transactionID += struct.pack('!B', t) 

    def buildPacket(self):
        macb = getMacInBytes()
        #DHCPREQUEST message
        packet = b''
        packet += b'\x02'   #OP
        packet += b'\x01'   #HTYPE
        packet += b'\x06'   #HLEN
        packet += b'\x00'   #HOPS 
        packet += b'\x39\x03\xF3\x26'       #XID
        packet += b'\x00\x00'    #SECS
        packet += b'\x80\x00'   #FLAGS
        packet += b'\x00\x00\x00\x00'   #CIADDR (Client IP address)
        packet += b'\xC0\xA8\x01\x64'   #YIADDR (Your IP address)
        packet += b'\xC0\xA8\x01\x01'   #SIADDR (Server IP address)
        packet += b'\x00\x00\x00\x00'   #GIADDR (Gateway IP address)
        packet += macb #CHADDR (Client hardware address)
        packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
        packet += b'\x00' * 67
        packet += b'\x00' * 125 
        packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
        packet += b'\x35\x01\x02'   #Option: DHCP Discover
        packet += b'\x3d\x06' + macb
        packet += b'\x37\x03\x03\x01\x06'   #DHCP Options 53
        packet += b'\xff'   #End Option
        return packet



class DHCPAck:
    def __init__(self):
        transID=0

    def buildPacket(self):
        macb = getMacInBytes()
        packet = b''
        packet += b'\x02'
        packet += b'\x01'
        packet += b'\x06'  
        packet += b'\x00'   
        packet += b'\x39\x03\xF3\x26'      
        packet += b'\x00\x00'    
        packet += b'\x80\x00'   
        packet += b'\x00\x00\x00\x00'   
        packet += b'\xC0\xA8\x01\x64'   
        packet += b'\xC0\xA8\x01\x01'   
        packet += b'\x00\x00\x00\x00'   
        packet += macb
        packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        packet += b'\x00' * 67  
        packet += b'\x00' * 125 
        packet += b'\x63\x82\x53\x63'   
        packet += b'\x35\x01\x05'   
        #packet += b'\x3d\x06' + macb
        #packet += b'\x32\x04\xC0\xA8\x1E\x0A'   #Option: DHCP option 50: 192.168.30.10 requested
        packet += b'\xff'   #End Option
        return packet


if __name__ == '__main__':
    input('Make sure you have started WireShark and press any key to continue~~')
   
    dhcps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dhcps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)    
#========================================================================
    try:
        dhcps.bind(('', 67))
    except Exception as e:
        dhcps.close()
        input('Error : port 1067 is be used and Program will quit!!')
        exit()
#==========================================================================
    print('DHCP Server Start')
    dhcps.settimeout(5)
    try:
        while True:
            data = dhcps.recv(1024)
            if data == '': 
              print('bye~')
              break
            else:
              break
    except socket.timeout as e:
        print('')

    offerPacket = DHCPOfferPack()
    dhcps.sendto(offerPacket.buildPacket(), ('<broadcast>', 68))
    try:
        while True:
            data = dhcps.recv(1024)
            if data == '':
              print('bye~')
              break
            else:
              break
    except socket.timeout as e:
        print('')
 
    offerAck = DHCPAck()
    dhcps.sendto(offerAck.buildPacket(), ('<broadcast>', 68))
    dhcps.close()
      
#============================================================================
    print('網路程式設計 HW1\n')
    print('學生：王梵維\n')
    print('學號：603410024\n')
    input('Press any key to exit and go to see the WireShark result.')
    exit()
    #my github link: https://github.com/rangewang/103-2_hw1/
