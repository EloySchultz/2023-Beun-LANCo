import animations_new
import time
import math
import socket


animation_class = animations_new.c_animations()
class beunding_streamer:
    def __init__(self,N,invert,IP, PORT, MAX_INDEX, BITMULT, PACKET_LENGTH):
        self.N =N
        self.invert=int(invert)
        self.IP = IP
        self.PORT = PORT
        self.PACKET_LENGTH = PACKET_LENGTH
        self.MAX_INDEX = MAX_INDEX
        self.BITMULT = BITMULT
        self.command = bytes()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def setLed(self, index, *a):
        # Creates a 3-byte bytestring that specifies one led

        if self.invert==1:
            index = self.N - index -1
        if len(a) == 1:
            r, g, b = a[0]
        else:
            r, g, b = a
        r=int(r)
        g=int(g)
        b=int(b)

        if index > self.MAX_INDEX:
            raise ValueError
        else:
            ir, il = index % self.BITMULT, index // self.BITMULT
        # print(il)
        # print(ir)
        # print(r)
        # print(g)
        # print(b)
        b = bytes([il,
                   ir * self.BITMULT + r,
                   g * self.BITMULT + b])
        self.command += b

    def send(self):
        # Splits command buffer into segments that fit a UDP packet
        maxbytes = self.PACKET_LENGTH - self.PACKET_LENGTH % 3

        if len(self.command) < self.PACKET_LENGTH:
            self.sock.sendto(self.command, (self.IP, self.PORT))
        else:
            for i in range(math.ceil(len(self.command) / maxbytes) - 1):
                self.sock.sendto(self.command[i * maxbytes:(i + 1) * maxbytes], (self.IP, self.PORT))
            self.sock.sendto(self.command[(i + 1) * maxbytes:], (self.IP, self.PORT))
        self.command = bytes()


class parallel_streamer:
    def __init__(self, child_ips,child_ports,child_leds,child_inverts,MAX_INDEX, BITMULT, PACKET_LENGTH):
        print("Parallel")
        self.PACKET_LENGTH = PACKET_LENGTH
        self.MAX_INDEX = MAX_INDEX
        self.BITMULT = BITMULT
        self.child_inverts = child_inverts
        self.child_ips=child_ips
        self.child_ports=child_ports
        self.child_leds=child_leds
        self.N = min(self.child_leds)
        self.command=bytes()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.fb={}

    def setLed(self, index, a):
        self.fb[index] = tuple(a)

    def setLed_for_real(self, index,invert,N,*a):
        # Creates a 3-byte bytestring that specifies one led
        if len(a) == 1:
            r, g, b = a[0]
        else:
            r, g, b = a
        r = int(r)
        g = int(g)
        b = int(b)
        if invert==1:
            index = N - index -1

        if index > self.MAX_INDEX:
            raise ValueError
        else:
            ir, il = index % self.BITMULT, index // self.BITMULT

        b = bytes([il,
                   ir * self.BITMULT + r,
                   g * self.BITMULT + b])
        self.command += b

    def send(self):
        curr_index = 0;
        #print(self.N)
        for q in range(0,len(self.child_ips)):
            self.IP = self.child_ips[q]
            self.PORT=self.child_ports[q]
            #self.N = self.child_leds[q]
            invert=int(self.child_inverts[q])
            self.command = bytes()
            maxbytes = self.PACKET_LENGTH - self.PACKET_LENGTH % 3
            for i in range(self.N):
                if i in self.fb.keys():
                    self.setLed_for_real(i, invert, self.N, self.fb[i])
            if len(self.command) < self.PACKET_LENGTH:
                self.sock.sendto(self.command, (self.IP, self.PORT))
            else:
                for i in range(math.ceil(len(self.command) / maxbytes) - 1):
                    self.sock.sendto(self.command[i * maxbytes:(i + 1) * maxbytes], (self.IP, self.PORT))
                self.sock.sendto(self.command[(i + 1) * maxbytes:], (self.IP, self.PORT))
            self.command = bytes()

        self.fb={}
    pass





class vdev_streamer:
    def __init__(self, child_ips,child_ports,child_leds,child_inverts,MAX_INDEX, BITMULT, PACKET_LENGTH):
        print("Sequentiel")
        self.PACKET_LENGTH = PACKET_LENGTH
        self.MAX_INDEX = MAX_INDEX
        self.BITMULT = BITMULT
        self.child_inverts = child_inverts
        self.child_ips=child_ips
        self.child_ports=child_ports
        self.child_leds=child_leds
        self.command=bytes()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.fb={}
    def setLed(self, index, a):
        try:
            self.fb[index] = tuple(a)
        except:
            print("an exception has occured")
    def setLed_for_real(self, index,invert,N,*a):
        # Creates a 3-byte bytestring that specifies one led
        if len(a) == 1:
            r, g, b = a[0]
        else:
            r, g, b = a
        r = int(r)
        g = int(g)
        b = int(b)
        if invert==1:
            index = N - index -1

        if index > self.MAX_INDEX:
            raise ValueError
        else:
            ir, il = index % self.BITMULT, index // self.BITMULT

        b = bytes([il,
                   ir * self.BITMULT + r,
                   g * self.BITMULT + b])
        self.command += b

    def send(self):
        curr_index = 0;
        for q in range(0,len(self.child_ips)):
            IP = self.child_ips[q]
            PORT=self.child_ports[q]
            N = self.child_leds[q]
            invert=int(self.child_inverts[q])
            self.command = bytes()
            for i in range(0, N):
                if curr_index + i in self.fb.keys():
                    self.setLed_for_real(i,invert,N, self.fb[curr_index + i])
            maxbytes = self.PACKET_LENGTH - self.PACKET_LENGTH % 3
            if len(self.command) < self.PACKET_LENGTH:
                self.sock.sendto(self.command, (IP, PORT))
            else:
                for i in range(math.ceil(len(self.command) / maxbytes) - 1):
                    self.sock.sendto(self.command[i * maxbytes:(i + 1) * maxbytes], (IP, PORT))
                self.sock.sendto(self.command[(i + 1) * maxbytes:], (IP, PORT))
            self.command = bytes()
            curr_index+=N

        self.fb={}
    pass
def single_stream(N, animation_name,color,invert,IP, PORT, MAX_INDEX, BITMULT, PACKET_LENGTH):
    #global obj_list
    N = int(N)
    beunding = beunding_streamer(N,invert,IP, PORT, MAX_INDEX, BITMULT, PACKET_LENGTH)
    enabled=1
    while(enabled):  #Hier moet iets komen zodat je animaties wel/niet kan loopen
        #animation_name = beunding.properties['Animation']
        if hasattr(animation_class, animation_name):
            animation = getattr(animation_class, animation_name)
        else:
            raise ValueError("Animation " + str(animation_name) + " does not exist")
        animation(beunding, N, duration = 200000, colour=color) #American to bri'ish converter
        enabled=0 #dit meot voor blank

def vdev_stream(sequential, N, animation_name,color, child_ips,child_ports,child_leds,child_inverts,MAX_INDEX, BITMULT, PACKET_LENGTH):
    #global obj_list
    print(sequential)
    if sequential=="1":
        N = int(N)
        beunding = vdev_streamer(child_ips,child_ports,child_leds,child_inverts,MAX_INDEX, BITMULT, PACKET_LENGTH)
        enabled=1
        while(enabled):  #Hier moet iets komen zodat je animaties wel/niet kan loopen
            #animation_name = beunding.properties['Animation']
            animation = getattr(animation_class, animation_name)
            animation(beunding, N, duration = 200000, colour=color)  #American to bri'ish converter
            enabled=0
    else:
        N = int(N)
        beunding = parallel_streamer(child_ips, child_ports, child_leds, child_inverts, MAX_INDEX, BITMULT, PACKET_LENGTH)
        enabled = 1
        while (enabled):  # Hier moet iets komen zodat je animaties wel/niet kan loopen
            # animation_name = beunding.properties['Animation']
            animation = getattr(animation_class, animation_name)
            animation(beunding, min(child_leds), duration=200000, colour=color)  # American to bri'ish converter
            enabled = 0