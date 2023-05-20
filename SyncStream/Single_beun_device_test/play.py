from UDPStreamer import beunding
from time import sleep
from animations import regenboog, sinus, set_colour, linerider, red_flame, blue_flame, green_flame, pink_flame, yellow_flame,white_flame, vertical_rainbow, red_flame_old, show_text
paal = beunding("192.168.2.157", 8888, 320, 4095)


#Seinpaal has 300 LEDs
#Ledbeam has 106 LEDS

#sinus(paal, 300, duration=1, colour=(4,1,4), dt=0.02)
#regenboog(paal, 300, speed=3,duration=300, brightness=0.2)
#linerider(paal, 300, 1, dt=0.02, colour = (1,2,1))
# for i in range(9,16):
   # col = (i,i,i)
   # print(col)     
   # set_colour(paal, 300,colour=col)
   # sleep(5)
    
# set_colour(paal, 300,colour=(0,0,0))
#sleep(100)
#red_flame(paal, 300, duration=30, dt=0.02)
#vertical_rainbow(paal, 300, duration=300, dt=0.02, brightness=0.1)
while(1):
    set_colour(paal, 106, colour = (0,0,0))
    #regenboog(paal, 106, speed=1,duration=5, brightness=0.3)
    #show_text(paal, 300,string="WELCOME TO THE TESLAN!",duration=1, dt=0.1,colour=(2,0,2))
    #red_flame(paal, 300, duration=5, dt=0.02)
    #linerider(paal, 300, 3,duration=5, dt=0.02, colour = (3,0,1))
    #vertical_rainbow(paal, 300, duration=5, dt=0.02, brightness=0.3, speed=1)
    #
    #white_flame(paal, 300, duration=5, dt=0.02)
    #yellow_flame(paal, 300, duration=5, dt=0.02)
    # green_flame(paal, 300, duration=5, dt=0.02)
    # pink_flame(paal, 300, duration=5, dt=0.02)
    # blue_flame(paal, 300, duration=5, dt=0.02)
    
    
    # linerider(paal, 300, 3,duration=3, dt=0.02, colour = (1,1,2))
