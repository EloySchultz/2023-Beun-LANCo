# 2023-Beun-Lanco
2023 Beun Lanco

The best LAN party in the world would not be complete without some fire hazards. In the past 5 editions of the TESLAN, LANCo members have crafted and accumulated many items, expertly referred to as beundingen (beunthings), which light up and add to the ambience of the LAN. 

In 2023, beun consists of three beunding categories and software:

1. Signposts (seinpalen)
2. LEDbeams Crew-area
3. Logo Crew-area 
4. SyncStream (software)

# 1. Signposts
The seinpalen are large PVC pipes with an addressable LED-string at the top. Typically there is one seinpaal for each group of tables at the LAN. These Seinpalen can be used to assign each group of tables to a color. They can also be used to highlight a group of tables, for example to tell that group of people that they can go and get food. 

The seinpalen are constructed of two pieces of PVC pipe. The dimensions are....[x]
Around the top PVC pipe part, 5 meters of 60 leds/m WS2812b leds are wrapped (300 leds total). Index 0 is LED closes to the ceiling and index 299 is the LED that is closes to the ground. Each LEDstrip has a JST-SM 3 pin female connector which powers the LEDstrip from the top. There is also a speaker wire attached at the bottom of the LEDstrip which powers the LEDstrip from the bottom. Please wire the seinpaal as follows:

{image here}

The Seinpalen are controlled by either an Arduino Nano (Seinpaal 1-4) or Arduino mini (Seinpaal 5-8). The microcontroller is mounted on a custom PCB, and interconnected to a WizNet W5500 LAN module via SPI. The PCB also acts as a passthrough for all the LED wiring as shown above. For all microcontroller programming, remove the microcontroller from the custom PCB as otherwise the LED-strip will try to power from your USB port. 

PSU?


# 2. LEDbeams Crew-area
The crew-area is usually a U-shaped group of tables that is seperated from the rest of the LAN. We gotta accentuate that with some LEDs ofcourse! So, the LANCo owns 10 beams of 1.8 meters that have 60 leds/m WS2812b LED strips attatched. There are 106 LEDs per beam (although this is slightly different for some damaged LEDbeams). Each LEDbeam has a 3-pin JST-female connector at the input and a 3pin JST-male connector at the output. We highly recommend to NOT chain more than 2 LEDbeams per PSU due to current losses in the LEDstrips. 

Controller

PSu?




# 3. Logo



# 4. SyncStream
https://github.com/MaxWinsemius/SyncStream/ 



