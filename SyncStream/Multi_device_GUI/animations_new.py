import colorsys
from time import sleep
from math import sin, pi, sqrt
import random
import numpy as np
import operator
import time
#%% Helpers
hsv2rgb = lambda h,s,v: tuple(int(x * 15) for x in colorsys.hsv_to_rgb(h,s,v))

class c_animations():
    def __init__(self):
        self.font = {
            'T': [[1, 0, 0, 0, 0], [1, 1, 1, 1, 1], [1, 0, 0, 0, 0]],
            'E': [[1, 1, 1, 1, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1]],
            'S': [[1, 1, 1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 1, 1, 1]],
            'L': [[1, 1, 1, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1]],
            'A': [[1, 1, 1, 1, 1], [1, 0, 1, 0, 0], [1, 1, 1, 1, 1]],
            'N': [[1, 1, 1, 1, 1], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [1, 1, 1, 1, 1]],
            ' ': [[0, 0, 0, 0, 0]],
            'W': [[1, 1, 1, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1], [1, 1, 1, 1, 0]],
            'C': [[0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1]],
            'O': [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]],
            'M': [[0, 1, 1, 1, 1], [1, 0, 0, 0, 0], [0, 1, 1, 0, 0], [1, 0, 0, 0, 0], [1, 1, 1, 1, 0]],
            'H': [[1, 1, 1, 1, 1], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1]],
            '!': [[1, 1, 1, 0, 1]],
            'F': [[1, 1, 1, 1, 1], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0]],
            'Y': [[1, 1, 1, 0, 1], [0, 0, 1, 0, 1], [1, 1, 1, 1, 0]],
            'I': [[1, 0, 0, 0, 1], [1, 1, 1, 1, 1], [1, 0, 0, 0, 1]],
            'K': [[1, 1, 1, 1, 1], [0, 0, 1, 0, 0], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1]],
            'V': [[1, 1, 1, 1, 0], [0, 0, 0, 0, 1], [1, 1, 1, 1, 0]],
            'U': [[1, 1, 1, 1, 1], [0, 0, 0, 0, 1], [1, 1, 1, 1, 1]]}
        pass
        

    def cycle(self,arr, s=1):
        def _cycle0(arr): return [*arr[1:], arr[0]]
        def _cycle1(arr): return [arr[-1], *arr[:-1]]
        for _ in range(abs(s)): 
            if s>0: arr = _cycle0(arr)
            else:   arr = _cycle1(arr)
        return arr

    #%% Animations
    # def regenboog(beunding, N, speed=1, dt=0.02,brightness = 0.1, duration=3):
        # t0 = time.time()
        # Nsteps = 9999999999999 #int(duration//dt) inf steps cuz sleep is inaccurate AF

        # buffer = [(x*1.0/N, 1, 1) for x in range(N)]

        # for _ in range(Nsteps):
            # for i, val in enumerate(buffer):
                # beunding.setLed(i, (int(brightness*x) for x in hsv2rgb(*val)))
            # beunding.send()
            # buffer = cycle(buffer, speed)
            # time.sleep(dt)
            # if time.time()-t0>duration:
                # return
                
    def show_1(self,beunding, N, speed=1, dt=0.02,brightness = 0.25, duration=30):
        for i in range(5):
            self.regenboog(beunding, 300, speed=1,duration=5, brightness=0.3)
            self.show_text(beunding, 300,string="WELCOME TO THE TESLAN!",duration=1, dt=0.1,colour=(2,0,2))
            self.red_flame(beunding, 300, duration=5, dt=0.02)
                
    def regenboog(self,beunding, N, speed=1, dt=0.02,brightness = 0.3, duration=30):
        Nsteps = int(duration//dt)

        buffer = [(x*1.0/N, 1, 1) for x in range(N)]

        for _ in range(Nsteps):
            for i, val in enumerate(buffer):
                beunding.setLed(i, (int(brightness*x) for x in hsv2rgb(*val)))
            beunding.send()

            buffer = self.cycle(buffer, speed)

            sleep(dt)
            
    def linerider_fill(self,beunding, N, speed=10, dt=0.02, duration=30, colour = (1,1,1)):
        Nsteps = int(duration//(dt))
        z=0;
        a = 1;
        for _ in range(Nsteps):
            for i in range(0,N,speed):
                if i == z:
                    if a>0:
                        for j in range(speed):
                            beunding.setLed(i+j,colour)
                    else:
                        for j in range(speed):
                            beunding.setLed(i+j,(0,0,0))
                    #print(z);
                #else:
                    #beunding.setLed(i,(0,0,0))
            beunding.send()
            z+=a*speed;
            if z>N or z<0:
                z=z-a*speed;
                a=-a;
            sleep(dt)
                    

    def sinus(self,beunding, N, speed=1, dt=0.02, duration=30, colour=(3,3,3)):
        Nsteps = int(duration//dt)

        period = []
        for i in range(32):
            val = [c*sin(pi*i/32) for c in colour]
            val = [int(abs(c)) for c in val]
            period.append(val)

        for _ in range(Nsteps//len(period)):
            for col in period:
                for i in range(N):
                    beunding.setLed(i, col)
                beunding.send()
                
                sleep(dt)

    def set_colour(self,beunding, N, speed=1, dt=0.02, duration=30, colour=(0,0,0)):
        for i in range(N):
            beunding.setLed(i, colour)
        beunding.send()

    def blank(self,beunding, N, speed=1, dt=0.02, duration=30):
        self.set_colour(beunding, N, colour=(0,0,0))
            
            
    def red_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour2 = (2,0,0), colour=(3,1,0)):
        #Dit kan efficienter, bla bla bla
        Nsteps = int(duration//dt)
        colors = [(0,0,0),colour2,colour]
        written = np.zeros(N);
        #q=0;
        #for i in range(int(N/4*3),N):
        #    written[i]=1;
        for q in range(Nsteps):
            t=140#random.randint(150,200); #Above this number: only flares.
            for i in range(N):
                if q%round(3*(350-i)/300+1)==0: #Dus dit zorgt ervoor dat ledjes onderaan snel updaten, en ledjes bovenaan langzaam updaten
                    if i>280: #core
                        written[i]=2;
                        if q%2 == 0:
                            written[i-13] = 2;
                    elif i>t: #between core and air
                        if written[i]>0:
                                if written[i]==2:
                                    if random.randint(0,10)>6:  #This number >x defines the height of the flames.
                                        written[i] -=1;
                                    if random.randint(100,300)<i:
                                        r=(random.randint(0,10)>5)*1
                                        written[max(0,i-13-r)]=2#-1*(random.randint(0,10)>5))] =2
                                        #written[max(0,i-13-1-r)]=1#*(random.randint(0,10)>5))] =2
                                        #written[max(0,i-13+1-r)]=1#*(random.randint(0,10)>5))] =2
                                elif written[i]==1:
                                    if random.randint(0,10)>3:
                                        written[i] -=1;
                                if written[i]==0:# and random.randint(0,10)>1:
                                    written[max(0,i-13-1*(random.randint(0,10)>5))] =1
                                    
                               
                                    
                    else:
                        ##flares
                        if written[i]>0:
                                written[i] -=1;
                                if written[i]==0 and random.randint(0,10)>1: #1/10 chance of disappearing
                                    written[max(0,i-13-1*(random.randint(0,10)>5))] =1
                                    
                  
                                    
                                    
                                    
            written[0] = 0;
            #for i in range(t-10,t+10):
            #    beunding.setLed(i,(1,0,1))
            for i in range(N):
                beunding.setLed(i, colors[int(written[i])])
            beunding.send()
            sleep(dt)
            
            
    def red_flame_old(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (1,0,0), colour2=(2,1,0)):
        #Dit kan efficienter, bla bla bla
        Nsteps = int(duration//dt)
        colors = [(0,0,0),colour2,colour]
        written = np.zeros(N);
        #q=0;
        #for i in range(int(N/4*3),N):
        #    written[i]=1;
        for q in range(Nsteps):
            t=random.randint(150,200);
            for i in range(N):
                if i>t and random.randint(0,N*3)<i: #and random.randint(0,N)<i:
                    if i>280: 
                        written[i] = 2;
                    else:
                        written[i] = random.randint(1,2);
                else:
                    if i>t: #core
                        if written[i]>0 and random.randint(0,N)>1.2*i:
                            if random.randint(0,2)>1:
                                written[i] -=1;
                            
                            if written[i]==0:# and random.randint(0,10)>1:
                                written[max(0,i-13-1*(random.randint(0,10)>5))] =1
                    else: #flares
                        if written[i]>0:
                            if q%3==0:
                            #if random.randint(0,10)>3: #slow decay, nice for flares
                                written[i] -=1;
                                if written[i]==0 and random.randint(0,10)>1: #1/10 chance of disappearing
                                    written[max(0,i-13-1*(random.randint(0,10)>5))] =1
                                    
                                    
                                    
            written[0] = 0;
            for i in range(N):
                beunding.setLed(i, colors[int(written[i])])
            beunding.send()
            sleep(dt)
            
    def blue_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (0,0,1), colour2=(1,2,2)):
        self.red_flame(beunding, N, speed, dt, duration, colour, colour2)

    def green_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (0,1,0), colour2=(2,2,0)):
        self.red_flame(beunding, N, speed, dt, duration, colour, colour2)
        
    def pink_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (1,0,1), colour2=(3,1,1)):
        self.red_flame(beunding, N, speed, dt, duration, colour, colour2)
        
    def yellow_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (2,1,0), colour2=(3,2,0)):
        self.red_flame(beunding, N, speed, dt, duration, colour, colour2)
        
    def white_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (1,1,1), colour2=(2,2,1)):
        self.red_flame(beunding, N, speed, dt, duration, colour, colour2)

        
    def vertical_rainbow(self,beunding, N, speed=1, dt = 0.02, duration = 30, brightness=0.2):
        Nsteps = int(duration//dt)
        offset=0;
        hsv2rgb = lambda h,s,v: tuple(int(x * 15) for x in colorsys.hsv_to_rgb(h,s,v))
        for offset in range(Nsteps):
            for i in range(N):
                colour = ()
                beunding.setLed(i, (int(brightness*x) for x in hsv2rgb((offset/26*speed+i/13)%13,1,1)))
            beunding.send()
            sleep(dt)
            

    def show_text(self,beunding, N, string="WELCOME TO THE TESLAN!", dt = 0.1, duration = 30, colour = (1,1,1)):
        #duration = how many times to repeat
        repeated=0
        font=self.font
        Nsteps = 1000000#int(duration//dt)
        offset=0
        colors=[(0,0,0),colour]
        min_index=10000000
        ls=0;
        for character in string: #find string length in LEDS
            ls += len(self.font[character]) + 1
        initial_offset = ls*14
        
        for _ in range(Nsteps):
            offset+=1;
            written = np.zeros(N);
            z=0
            max_index=0
            for character in string[::-1]:
                l=len(font[character])
                for i in range(l): # breedte
                    for j in range(5): #hoogte
                        #print(max_index)
                        max_index = max(max_index,N-(j+i)*13-(i)-(offset+(z))*14+initial_offset*2+14*10+7)
                        written=self.try_set_written(written,N,N-(j+i)*13-(i)-(offset+(z))*14+initial_offset, font[character][l-1-i][4-j])
                        written=self.try_set_written(written,N,N-(j+i)*13-(i)-(offset+(z))*14+initial_offset*2+14*10+7, font[character][l-1-i][4-j])
                        #beunding.setLed()
                z+=l+1;
            if max_index==0:
                offset=0;
                repeated+=1;
                if repeated==duration:
                    return;
            for i in range(N):
                beunding.setLed(i, colors[int(written[i])])
            beunding.send()
            
            beunding.send()
            sleep(dt)
        #print(font['A']);
    def try_set_written(self,written,N,i,val):
        if i<N and i>-1:
            written[i]=val
        return written