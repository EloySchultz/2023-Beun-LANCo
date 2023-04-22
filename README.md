# 2023-Beun-Lanco
The best LAN party in the world would not be complete without some fire hazards. In the past 5 editions of the TESLAN, LANCo members have crafted and accumulated many items, expertly referred to as "beundingen" (beunthings), which light up and add to the ambience of the LAN. 

In 2023, beun consists of three beunding categories and software:

1. Signposts (seinpalen)
2. LEDbeams Crew-area
3. Logo Crew-area 
4. SyncStream (software)

# 1. Signposts
The seinpalen are large PVC pipes with an addressable LED-string at the top. Typically there is one seinpaal for each group of tables at the LAN. These Seinpalen can be used to assign each group of tables to a color. They can also be used to highlight a group of tables, for example to tell that group of people that they can go and get food. 

The seinpalen are constructed of two pieces of 70 mm PVC pipe, coupled by a 70-70mm PVC extender (coupler piece). The top piece is about 40 cm in length, while the bottom piece is 2 meters long. Around the top piece, 5 meters of 60 leds/m WS2812b leds are wrapped (300 leds total). Index 0 is LED closes to the ceiling and index 299 is the LED that is closes to the ground. Each LEDstrip has a JST-SM 3 pin female connector which powers the LEDstrip from the top. There is also a speaker wire attached at the bottom of the LEDstrip which powers the LEDstrip from the bottom. Please wire the seinpaal as follows:

![image](https://user-images.githubusercontent.com/99472685/225277334-c6208dba-fee9-407c-9db2-920bfa4313dd.png)

The Seinpalen are controlled by either an Arduino Nano (Seinpaal 1-4) or Arduino pro mini (5V 16Mhz) (Seinpaal 5-8).  The microcontroller is mounted on a custom PCB. The custom PCB has pads that can be soldered to "select" either Nano or Pro mini pinouts. The microcontroller is interconnected to a WizNet W5500 LAN module via SPI. The PCB also acts as a passthrough for all the LED wiring as shown above. For all microcontroller programming, remove the microcontroller from the custom PCB as otherwise the LED-strip will try to power from your USB port. Another tip: for the Arduino pro mini's, use a proper FTDI programmer because if somehow the ground gets disconnected during programming, a short will be created through the data pins and that may fry your pro-mini.

For powersupply, a 5V >7A powersupply should be used. Strictly, the LEDstrip can pull up to 18A. However in reality, I found that the maximum current is lower due to the losses in the wires. High current causes high voltage drop across the wires, which in turn lowers the voltage that the LEDs receive. At some point, the voltage drop is so high that the LEDs no longer pass through data. 


# 2. LEDbeams Crew-area
The crew-area is usually a U-shaped group of tables that is seperated from the rest of the LAN. This area hosts the most valuable people at the LAN, soooo we gotta accentuate that with some LEDs of course! To achieve this, the LANCo owns 10 beams of 1.8 meters that have 60 leds/m WS2812b LED strips attatched. There are 106 LEDs per beam (although this is slightly different for some damaged LEDbeams). Each LEDbeam has a 3-pin JST-female connector at the input and a 3pin JST-male connector at the output. We highly recommend to NOT chain more than 2 LEDbeams per PSU due to current losses in the LEDstrips. 

Controller

PSu?




# 3. Logo

Laser go BRRRT.

Yes so new in the 6th edition of the TesLAN is laser graphics logo! The idea is that, instead of building a phyisical logo out of PVC pipe and el-wire to put on the wall, we instead use a laser to project graphics and animations on the wall. I worked on a script to convert .SVG files to .ild (ILDA) files. I even made it so that a color table is automatically generated per ILDA file! (I hope this is how it is supposed to be).


# 4. SyncStream
https://github.com/MaxWinsemius/SyncStream/ 






#5. Continuation of the cycle
When I started doing beun for LANCo in early 2023 there was little to no documentation on what goes where and how it all works together. That is the reason why I started this repo. Please, for our postertity, document the things that you do during your year(s) of beun at the LANCo, such that new LANCo members can easily pick up the task for the next edition of the TESLAN. I recommend you to host your own copy of this repo while you work on beun (or do a fork if you so desire).


