# 2023-Beun-Lanco
The best LAN party in the world would not be complete without some fire hazards. In the past 5 editions of the TesLAN, the tinkering masters of the LANCo have crafted and accumulated things that light up and add to the ambience of the LAN, expertly referred to as "beundingen" (beunthings). 

In 2023, beun consists of three beunding categories and software:

1. Signposts (seinpalen)
2. LEDbeams Crew-area
3. Logo Crew-area 
4. SyncStream (software)

# 1. Signposts
The seinpalen are large PVC pipes with an addressable LED-string at the top. Typically there is one seinpaal for each group of tables at the LAN. These Seinpalen can be used to assign each group of tables to a color. They can also be used to highlight a group of tables, for example to tell that group of people that they can go and get food. 

The seinpalen are constructed of two pieces of 70 mm PVC pipe, coupled by a 70-70mm PVC extender (coupler piece). The top piece is about 40 cm in length, while the bottom piece is 2 meters long. (The bottom 2 meter long part is not always 70 mm, will report on this once on the LAN). Around the top pipe, 5 meters of 60 leds/m WS2812b leds are wrapped (300 leds total). The input of the LED strip is at the top, so index 0 is LED closes to the ceiling and index 299 is the LED that is closes to the ground. Each LEDstrip has a JST-SM 3 pin female connector which powers the LEDstrip from the top. There is also a speaker wire attached at the bottom of the LEDstrip which powers the LEDstrip from the bottom. It is needed to have 2 power injection points, as the voltage drops quickly on the conductors in the LED-strips, because of their relatively high resistance. Please wire the seinpaal as follows:

![image](https://user-images.githubusercontent.com/99472685/225277334-c6208dba-fee9-407c-9db2-920bfa4313dd.png)

The Seinpalen are controlled by either an Arduino Nano (Seinpaal 1-4) or Arduino pro mini (5V 16Mhz) (Seinpaal 5-8).  The microcontroller is mounted on a custom PCB. The custom PCB has pads that can be soldered to "select" either Nano or Pro mini pinouts. The microcontroller is interconnected to a WizNet W5500 LAN module via SPI. The PCB also acts as a passthrough for all the LED wiring as shown above. For all microcontroller programming, remove the microcontroller from the custom PCB as otherwise the LED-strip will try to power from your USB port. Another tip: for the Arduino pro mini's, use a proper FTDI programmer because if somehow the ground gets disconnected during programming, a short will be created through the data pins and that may fry your pro-mini.

For powersupply, a 5V >7A powersupply should be used. I recommend to use the high current ATX powersupplies for the seinpalen as they have long wires (i.e. current losses) and many LEDs. Strictly, the LEDstrip can pull up to 18A! However in reality, I found that the maximum current is lower due to the losses in the wires. High current causes high voltage drop across the wires, which in turn lowers the voltage that the LEDs receive. At some point, the voltage drop is so high that the LEDs no longer pass through data.

The code for the seinpaal controllers is placed in the folder Arduino_esp_code/. The config can be found in devices.h, which includes MAC/IP settings for all devices. If at least one device has USING_ESP8266 defined, then you need to supply the wifi credentials in wifi_credentials.h (see wifi_credentials_example.h). 

When booting a microcontroller with this code, there is a simple LED debug indicator visible (1st 14 LEDS, on seinpalen this looks like a ring). 

| Ring color | Status                                                                                                           |
|------------|------------------------------------------------------------------------------------------------------------------|
| Blue       | Init error: WizNET/Wifi chip cannot be found. Check connections between Wiznet and microcontroller               |
| Red        | Init complete, but no connection: Can be because IP conflicts, network cable disconnected, incorrect credentials |
| Green      | All good: Device has IP and is ready to receive packets                                                          |

## ATX powersupplies:
We have 6 ATX PSU's that have been wired to just output 5V. On these PSUs, the green wire (PSU-ON) is wired to ground such that the power supplies are always on. Each power supply has at least 3 conductors going from the 5V rail to a WAGO clip. The WAGO clips are supposed to be permanently attached to the PSUs, as it can be a pain to squeeze the wires in the WAGO clips. All other wires are tucked to the inside of the powersupplies and isolated per rail with isolation tape. 


# 2. LEDbeams Crew-area
The crew-area is usually a U-shaped group of tables that is seperated from the rest of the LAN. This area hosts the most valuable people at the LAN, soooo we gotta accentuate that with some LEDs of course! To achieve this, the LANCo owns 10 beams of 1.8 meters that have 60 leds/m WS2812b LED strips attatched. There are 106 LEDs per beam (although this is slightly different for some damaged LEDbeams). Each LEDbeam has a 3-pin JST-female connector at the input and a 3pin JST-male connector at the output (at I hope to solder this like this this year). We highly recommend to NOT chain more than 2 LEDbeams per PSU due to current losses in the LEDstrips. 

![image](https://github.com/EloySchultz/2023-Beun-LANCo/assets/99472685/4ca987e2-1cc2-42c6-80d7-1bf7fa666d44)

The idea is that the powersupply is in the center of two beams, thus creating minimal in-strip resistive losses. For controllers, we simply use ESP8266 nodeMCU V3 boards with a JST-SM male connector attached to it. This controller hangs on the input side of the beams, and will receive power through the rails of the ledstrip. 


On the ESP8266, the same code in the folder Arduino_esp_code/ is used. Make sure to switch to the correct device in the arduino IDE before uploading.


# 3. Logo

In previous years, there was a large TesLAN logo on the wall behind the crew-area. This was first achieved by building the logo out of cardboard, and from the 4th edition a large PVC logo was built that was lit up using EL-Wire. However, this logo was a pain to set up and the EL-wire PSU broke at the 5th edition of the TesLAN. Hence, a new solution was needed.

For this year, we will rent a laser projector and FB3 interface from T-organisations. The laser can project shapes by quickly rotating mirrors (scanners), such that the laser point moves quickly and to our pesky human eyes it looks like solid lines. In order to create animations/graphics for the laser, we have set up the following pipeline: 

## 3.1 Figure creation
Use either Adobe Illustrator for still images, or Adobe Animate to generate animations. Make sure that all figures in the image only have a border/outline and don't have a fill. In case of an animation, it is imperative that the first frame of the animation contains all colors for that animation. I.e. you cannot introduce a new color halfway through the animation, if it was not also present in the first frame of the animation. Another limitation: we currently do not support mask tags, meaning that you cannot use masks in Adobe Animate. Export your frame/animation as an SVG file/sequence. 

## 3.2 SVG Processing
This is where the magic happens. We have SVG image(s) that consist of vectors, but we need a sequence of points that our laser point needs to jump to. Furthermore, the laser needs to know for each move if the laser should be enabled and what color the laser should be during the movement. 

I have taken an SVG2ILD script from OpenLase and I have modified it to support xlink tags, transforms, and color (both CSS style header and in-tag stroke). The script reads an SVG file, and then using SAX XML parser and alot of magic we extract a list of points, the color and whether the laser should be on/off during the movement. The color table is generated based on the first frame on an animation, and is put in a seperate ILDA section (see docs/ILDA_IDTF14_rev011.pdf for complete ILDA transfer specification that we use). Furthermore, we sort the points such that a semi-optimal path is found to connect all the points. I recommend you check the script yourself to understand what is going on!

To convert .svg files, go to Logo/SVG2ILD/run.py and put in the files there and then simply run it using python. There is a seperate section for single frames and for video SVG sequences. The main magic is happening in Logo/SVG2ILD/core.py. The script will output the .ild (ILDA) files in Logo\SVG2ILD\ILDA.

These IDLA files can then be loaded into a laser program of choice. For this year, we will use pangolin quickshow as we have a pangolin FB3 interface for our laser. In quickshow, we simply import the .ild files as figures, and then we use the quickshow features to create a lasershow consisting of various animations. In quickshow, we can also adjust the laser for non-normal projection (keystone correction, video: https://www.youtube.com/watch?v=BOX0U0b0qSE). 

During the LAN, we will tune the settings in Logo/SVG2ILD/core.py so that our ILDA files are optimized for the laser that we get. The dwell settings and speed can influence how many points have to be drawn by the laser, so these settings can influence flickering in the final image.  


# 4. SyncStream
Heavily based on: https://github.com/MaxWinsemius/SyncStream/ 
Yeah so SyncStream is pretty cool. SyncStream has two parts: one program that runs on the beun devices (that you can find in /Arduino_esp_code) and the other that runs on a computer that acts as a server (find this in /SyncStream). This year, I wrote a GUI for syncstream that allows for easy managing of all beun devices in the hall. You run it by running /SyncStream/Multi_device_GUI/main.py. It allows for beun devices to be grouped, or nested in virtual devices such that a group of devices acts as one large device. [TODO ELoy add some images/tutorial here]




