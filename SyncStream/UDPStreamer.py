import socket
from math import ceil

class beunding():
    def __init__(self, IP, PORT, PACKET_LENGTH, MAX_INDEX=4095, BIT_SHIFT=4):
        self.IP = IP
        self.PORT = PORT
        self.PACKET_LENGTH = PACKET_LENGTH
        self.MAX_INDEX = MAX_INDEX
        self.BITMULT = int(2**BIT_SHIFT)
        self.command = bytes()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def setLed(self, index, *a):
        #Creates a 3-byte bytestring that specifies one led
        if len(a) == 1: r,g,b=a[0]
        else: r,g,b = a

        if index > self.MAX_INDEX: raise ValueError
        else: ir, il = index%self.BITMULT, index//self.BITMULT
        
        b =  bytes([il, 
                    ir*self.BITMULT + r, 
                    g*self.BITMULT + b])
        self.command += b

    def send(self):
        #Splits command buffer into segments that fit a UDP packet
        maxbytes = self.PACKET_LENGTH - self.PACKET_LENGTH%3

        if len(self.command) < self.PACKET_LENGTH:
            self.sock.sendto(self.command, (self.IP, self.PORT))
        else:
            for i in range(ceil(len(self.command)/maxbytes)-1):
                self.sock.sendto(self.command[i*maxbytes:(i+1)*maxbytes], (self.IP, self.PORT))
            self.sock.sendto(self.command[(i+1)*maxbytes:], (self.IP, self.PORT))
        
        self.command = bytes()
