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
            self.regenboog(beunding, N, speed=1,duration=10, brightness=0.7)
            self.knightrider(beunding, N, speed=10, duration=10)
            self.moving_stripes(beunding, N, speed=1, duration=10)
            self.dots(beunding, N, speed=1, duration=10)
            self.snake(beunding, N, speed=1, duration=10)
            self.idle(beunding, N, speed=1, duration=10)
            self.wiper(beunding, N, speed=1, duration=10)
            self.wiper(beunding, N, speed=0.5, duration=10, colour=(10,0,8))
            self.wiper(beunding, N, speed=0.5, duration=10, colour=(2,3,7))
    def regenboog(self,beunding, N, speed=1, dt=0.02,brightness = 0.7, duration=30):
        Nsteps = int(duration//dt)

        buffer = [(x*1.0/N, 1, 1) for x in range(N)]

        for _ in range(Nsteps):
            for i, val in enumerate(buffer):
                beunding.setLed(i, (int(brightness*x) for x in hsv2rgb(*val)))
            beunding.send()

            buffer = self.cycle(buffer, speed)

            sleep(dt)

    def knightrider(self,beunding, N, speed=3, dt=0.02, duration=30, colour = (5,2,0)):
        buffer = []
        for i in range(N):
            buffer.append((0,0,0))
        Nsteps = int(duration//(dt))
        z=0;
        a = 1;
        for _ in range(Nsteps):
            for i in range(0,N,speed):
                if i == z:
                    if a:
                        for j in range(speed):
                            if (i+j<N):
                                buffer[i+j] = colour
                                #beunding.setLed(i+j,colour)
                        for j in range(speed):
                            if a>0:
                                if (i-1-j)>=0:
                                    buffer[i-1-j] = (0,0,0)
                            else:
                                if (i+speed+j<N):
                                    buffer[i+speed+j] = (0,0,0)

                    #print(z);
                #else:
                    #beunding.setLed(i,(0,0,0))
            self.send_buffer(beunding,buffer)
            z+=a*speed;
            if z>N or z<0:
                z=z-a*speed;
                a=-a;
            sleep(dt)

    def knightrider_fill(self,beunding, N, speed=10, dt=0.02, duration=30, colour = (1,1,1)):
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

    def send_buffer(self,beunding,buffer):
        for i in range(len(buffer)):
            beunding.setLed(i,buffer[i])
        beunding.send()

    def moving_stripes(self,beunding, N, speed=1, dt=0.06, duration=30, colour=(15,0,15)):

        portal = 1;
        portal1_N=50
        portal2_N=60
        if colour == (0,0,0):
            rgb=1;
        else:
            rgb=0
        Nsteps = int(duration // (dt))
        buffer = []
        for i in range(N):
            buffer.append((0,0,0))
        # main loop
        offset = 0;
        for t in range(Nsteps):
            if rgb==1:
                colour = (15 * (1 / 2 + 1 / 2 * sin(2 * pi * t * dt / 20)),
                          15 * (1 / 2 + 1 / 2 * sin(2 * pi * t * dt / 20 + 2 / 3 * pi)),
                          15 * (1 / 2 + 1 / 2 * sin(2 * pi * t * dt / 20 + 4 / 3 * pi)))
            for i in range(N):
                buffer[i] = tuple([max(0, (-0.2 + sin((i + t) / 50 * 2 * pi))) * x for x in colour])
            if portal == 1:
                for i in range(portal1_N,portal2_N):
                    buffer[i] = (0,0,0)
                for i in range(3):
                    buffer[i+portal1_N] = (15,3,0)

                    buffer[i + portal2_N] = (0, 3, 15)


            self.send_buffer(beunding, buffer)
            sleep(dt)
    def dots(self,beunding, N, speed=1, dt=0.06, duration=30, colour=(15,0,0)):
        Nsteps = int(duration // dt)
        buffer = []
        for i in range(N):
            buffer.append((0, 0, 0))
        buffer2 = []
        for i in range(N):
            buffer2.append((0, 0, 0))
        k=0
        colour = (10, 0, 0)
        for t in range(Nsteps):
            if t*dt-k*dt>3:
                colour = (colour[1],colour[2],colour[0])
                k=t
            for i in range(N):
                buffer[N-i-1] = tuple(x*((t+i)%3>1) for x in colour)

            if random.randint(0,100)>85:
                j = random.randint(0,N-1)
                buffer2 = self.try_set_written(buffer2, N, j, (15, 15, 15))
                for i in range(5):
                    buffer2=self.try_set_written(buffer2,N,i+j, tuple(0.8**i*x for x in (10,10,10)))
                    buffer2 = self.try_set_written(buffer2, N, j-i, tuple(0.8**i*x for x in (10, 10, 10)))
            for i in range(N):
                buffer2[i] = tuple(0.93*x for x in buffer2[i])
            #print(buffer2)
            #buffer=buffer2
            for i in range(N):
                buffer[i] = tuple(max(x) for x in zip(buffer[i],buffer2[i]))
            self.send_buffer(beunding, buffer)
            sleep(dt)
    def wiper(self,beunding,N,speed=1, dt=0.02, duration=30, colour=(1,6,3)):
        dt = dt*speed
        buffer=[]
        for i in range(N):
            buffer.append((0,0,0))

        for i in range(int(N/2)):
            buffer[i]=colour
            buffer[N-i-1]=colour
            self.send_buffer(beunding,buffer)
            time.sleep(dt)
        for i in range(int(N / 2)):
            buffer[int(N/2)-i] = (0,0,0)
            buffer[int(N/2)+i] = (0,0,0)
            self.send_buffer(beunding, buffer)
            time.sleep(dt)
        buffer[0] = (0, 0, 0)
        buffer[N-1] = (0,0,0)
        self.send_buffer(beunding, buffer)
        time.sleep(2*dt)

    def wipe_and_fade(self,beunding,N,speed=1, dt=0.02, duration=30, colour=(1,6,3)):
        buffer=[]
        for i in range(N):
            buffer.append((0,0,0))

        for i in range(int(N/2)):
            buffer[i]=colour
            buffer[N-i-1]=colour
            self.send_buffer(beunding,buffer)
            time.sleep(dt)

        for k in range(0,1000,100):
            #print(k)
            for i in range(N):
                buffer[i] = tuple(x*(1000-k)/1000 for x in colour)
            self.send_buffer(beunding, buffer)
            time.sleep(dt)

    def color_cycle(self,beunding,N,speed=1, dt=0.02, duration=30, colour=(1,6,3)):
        Nsteps = int(duration // dt)
        for t in range(Nsteps):
            hsv2rgb = lambda h, s, v: tuple(int(x * 15) for x in colorsys.hsv_to_rgb(h, s, v))
            colour = hsv2rgb(t*dt/60,1,0.5)
            for i in range(N):
                beunding.setLed(i,colour)
            beunding.send()
            time.sleep(dt)
    def snake(self,beunding, N, speed=1, dt=0.001, duration=30, colour=(1,6,3)):
        t1 = time.time()
        snake_index=0;
        direction = 1;
        snake_len = 4;
        buffer = []

        apple_index = random.randint(0,N-1)
        for i in range(N):
            buffer.append((0,0,0))
        for t in range(10000000):
            for i in range(N):
                buffer[i] = (0, 0, 0)
            if snake_index+direction < 0 or snake_index+snake_len+direction>N:
                direction=direction*-1
            snake_index=snake_index + direction

            if apple_index>=snake_index and apple_index<=snake_index+snake_len:
                while(apple_index>=snake_index and apple_index<=snake_index+snake_len):
                    apple_index = random.randint(0,N-1)
                snake_len+=1
                if snake_index+snake_len>N:
                    snake_index-=1

            #render snake
            for i in range(snake_len):
                buffer[snake_index+i] = (0,15,0)

            #render apple
            buffer[apple_index] = (15,0,0)

            self.send_buffer(beunding,buffer)

            sleep(dt)
            if time.time()-t1 > duration:
                return
            if snake_len>N-30:
                b=[]
                for i in range(N):
                    b.append((0,0,0))
                for _ in range(3):
                    self.send_buffer(beunding, b)
                    time.sleep(0.5)
                    self.send_buffer(beunding, buffer)
                    time.sleep(0.5)
                self.send_buffer(beunding, b)
                time.sleep(1)
                snake_len=1

    def sinus(self, beunding, N, speed=1, dt=0.02, duration=30, colour=(0, 0, 0)):
        if colour == (0, 0, 0):
            rgb = 1
        else:
            rgb = 0

        Nsteps = int(duration // dt)
        #
        # period = []
        # for i in range(32):
        #     #val =
        #     #val = [int(abs(c)) for c in val]
        #     period.append(val)
        hsv2rgb = lambda h, s, v: tuple(int(x * 15) for x in colorsys.hsv_to_rgb(h, s, v))
        for q in range(Nsteps):

            if rgb == 1:
                colour = hsv2rgb(q * dt / 60, 1, 0.8)

            col = [int(round((1 / 2 + 1 / 2 * sin(pi * q /64)) * c)) for c in colour]
            for i in range(N):
                beunding.setLed(i, col)
            beunding.send()

            sleep(dt)

    def idle(self,beunding, N, speed=1, dt=0.02, duration=30, colour=(0,0,0)):
        hsv2rgb = lambda h, s, v: tuple(int(x * 15) for x in colorsys.hsv_to_rgb(h, s, v))
        if colour == (0,0,0):
            rgb=1
        else:
            rgb=0
        if rgb == 1:
            colour = hsv2rgb(0 * dt / 60, 1, 1)
            mcol = tuple(0.5*x for x in colour)

        self.wipe_and_fade(beunding, N, speed=1, dt=0.02, duration=30, colour=colour)



        #self.wiper(beunding, N, speed=1, dt=0.02, duration=30, colour=mcol)
        Nsteps = int(duration//dt)
        #
        # period = []
        # for i in range(32):
        #     #val =
        #     #val = [int(abs(c)) for c in val]
        #     period.append(val)
        centroids=[20,50]
        speeds=[1,-0.52]
        magnitude=0
        m2 = 0
        buffer=[]
        buffer2=[]
        for i in range(N):
            buffer.append((0,0,0))
            buffer2.append((0, 0, 0))

        for q in range(Nsteps):
            magnitude = min(1,q*dt/12)
            m2 = min(1, q * dt / 1)
            if rgb == 1:
                colour = hsv2rgb(q * dt /240, 1, 1)
            #col = tuple(0.5*x for x in colour)
            col = [int(round(c*0.5*m2)) for c in colour] #sinus (1 / 2 + 1 / 2 * sin(pi * q / 128)) *
            for i in range(N):
                buffer[i] = col
                buffer2[i] = (0,0,0) #if you remove this you get pastal colours which is still cool!
            k=0
            for x in centroids:
                centroids[k] +=speeds[k]
                if centroids[k] > N:
                    centroids[k]=0
                if centroids[k]<0:
                    centroids[k]=N
                k+=1
                x=round(x)
                buffer2 = self.try_set_written(buffer2, N, x, tuple(magnitude * x for x in (15, 15, 15)))
                for i in range(5):
                    buffer2 = self.try_set_written(buffer2, N, i + x, tuple(magnitude*0.6 ** i * x for x in (10, 10, 10)))
                    buffer2 = self.try_set_written(buffer2, N, x - i, tuple(magnitude*0.6 ** i * x for x in (10, 10, 10)))
            for i in range(N):
                buffer[i] = tuple(max(x) for x in zip(buffer[i],buffer2[i]))
            self.send_buffer(beunding,buffer)
            sleep(dt)
    def green(self,beunding, N, speed=1, dt=0.02, duration=30, colour=(0,1,0)):
        self.set_colour(beunding, N, speed, dt, duration, colour=colour)
    def set_colour(self,beunding, N, speed=1, dt=0.02, duration=30, colour=(0,0,0)):
        for i in range(N):
            beunding.setLed(i, colour)
        beunding.send()

    def blank(self,beunding, N, speed=1, dt=0.02, duration=30, colour=(0,0,0)):
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
            
            
    #
    # def blue_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (0,0,1), colour2=(1,2,2)):
    #     self.red_flame(beunding, N, speed, dt, duration, colour, colour2)
    #
    # def green_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (0,1,0), colour2=(2,2,0)):
    #     self.red_flame(beunding, N, speed, dt, duration, colour, colour2)
    #
    # def pink_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (1,0,1), colour2=(3,1,1)):
    #     self.red_flame(beunding, N, speed, dt, duration, colour, colour2)
    #
    # def yellow_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (2,1,0), colour2=(3,2,0)):
    #     self.red_flame(beunding, N, speed, dt, duration, colour, colour2)
    #
    # def white_flame(self,beunding, N, speed=1, dt = 0.02, duration = 30, colour = (1,1,1), colour2=(2,2,1)):
    #     self.red_flame(beunding, N, speed, dt, duration, colour, colour2)

        
    def vertical_rainbow(self,beunding, N, speed=1, dt = 0.02, duration = 30, brightness=0.6):
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