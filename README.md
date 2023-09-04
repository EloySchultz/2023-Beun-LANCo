# 2023-Beun-LANCo | TesLAN 6th Edition 

![image](https://github.com/EloySchultz/2023-Beun-LANCo/assets/99472685/4e1e5fa1-0133-4f9e-8dd2-f09942c62a99)

The best LAN party in the world would not be complete without some fire hazards. In the past 5 editions of the TesLAN, the tinkering masters of the LANCo have crafted and accumulated things that light up and add to the ambience of the LAN, expertly referred to as "beundingen" (beunthings). 

For TesLAN 6, beun consisted of the following items:

1. Signposts (seinpalen)
2. LEDbeams Crew-area
3. Logo Crew-area 
4. SyncStream (software)
5. Beamer assembly
6. Switch beams

# 1. Signposts
![image](https://github.com/EloySchultz/2023-Beun-LANCo/assets/99472685/53bb3fde-d291-4a63-9da1-c227e7efac15)

The seinpalen are large PVC pipes with an addressable LED-string at the top. Typically there is one seinpaal for each group of tables at the LAN. These Seinpalen can be used to assign each group of tables to a color. They can also be used to highlight a group of tables, for example to tell that group of people that they can go and get food. 

Most of the seinpalen are constructed of two pieces of 70 mm PVC pipe, coupled by a 70-70mm PVC extender (coupler piece). However, with some seinpalen the bottom piece is more than 70 mm in diameter, hence some tape is needed to attach the 70mm head to the >70mm bottom piece. The top piece is about 40 cm in length, while the bottom piece is 2 meters long. Around the top pipe, 5 meters of 60 leds/m WS2812b leds are wrapped (300 leds total). The input of the LED strip is at the top, so index 0 is LED closes to the ceiling and index 299 is the LED that is closes to the ground. Each LEDstrip has a JST-SM 3 pin female connector which powers the LEDstrip from the top. There is also a speaker wire attached at the bottom of the LEDstrip which powers the LEDstrip from the bottom. It is needed to have 2 power injection points, as the voltage drops quickly on the conductors in the LED-strips, because of their relatively high resistance. Please wire the seinpaal as follows:

![image](https://user-images.githubusercontent.com/99472685/225277334-c6208dba-fee9-407c-9db2-920bfa4313dd.png)

The Seinpalen are controlled by either an Arduino Nano (Seinpaal 1-4) or Arduino pro mini (5V 16Mhz) (Seinpaal 5-8).  The microcontroller is mounted on a custom PCB. The custom PCB has pads that can be soldered to "select" either Nano or Pro mini pinouts. The microcontroller is interconnected to a WizNet W5500 LAN module via SPI. The PCB also acts as a passthrough for all the LED wiring as shown above. For all microcontroller programming, remove the microcontroller from the custom PCB as otherwise the LED-strip will try to power from your USB port. Another tip: for the Arduino pro mini's, use a proper FTDI programmer because if somehow the ground gets disconnected during programming, a short will be created through the data pins and that may fry your pro-mini.

For powersupply, a 5V >7A powersupply should be used. I recommend to use the high current ATX powersupplies for the seinpalen as they have long wires (i.e. current losses) and many LEDs. Strictly, the LEDstrip can pull up to 18A! However in reality, I found that the maximum current is lower due to the losses in the wires. High current causes high voltage drop across the wires, which in turn lowers the voltage that the LEDs receive. At some point, the voltage drop is so high that the LEDs no longer pass through data.

https://youtu.be/9BhRjhOlgGc

The code for the seinpaal controllers is placed in the folder Arduino_esp_code/. The config can be found in devices.h, which includes MAC/IP settings for all devices. If at least one device has USING_ESP8266 defined, then you need to supply the wifi credentials in wifi_credentials.h (see wifi_credentials_example.h). 

When booting a microcontroller with this code, there is a simple LED debug indicator visible (1st 14 LEDS, on seinpalen this looks like a ring). 

| Ring color | Status                                                                                                           |
|------------|------------------------------------------------------------------------------------------------------------------|
| Blue       | Init error: WizNET/Wifi chip cannot be found. Check connections between Wiznet and microcontroller               |
| Red        | Init complete, but no connection: Can be because IP conflicts, network cable disconnected, incorrect credentials |
| Green      | All good: Device has IP and is ready to receive packets                                                          |


If a beundevice ring color is flickering between green and red, this is either because of 
- a voltage spike on the PSU. This is a common issue with ATX powersupplies right after you connect them to mains voltage. Let it sit for 30 seconds, it should stabilize.
- a UDP package that is received that addresses memory that is not reserved. This usually happens when the number of LEDs in the Arduino code is smaller than the number of LEDs you are sending in SyncStream. It can also happen if you have a mismatch in packet length (320 should be good for this).
- something weird is going on between switch and beunding. We had this happen a bunch of times during the build-up of TesLAN 6. If the beunding is constantly requesting an IP from the switches, the beunding might manage to get an address for a very short bit, but it will lose this again shortly which causes a red-green loop. This was eventually solved by simply rebooting the microcontroller a couple of times. 
- If your ring is purple, this is a combination of blue and red. This only happened once so far, and the problem went away after re-flashing the microcontroller. 


## Something that needs fixing:
For next edition, please make a strain relief or mount for the PCBs of the seinpalen. Currently the weight of the PCB and of all network cable/power wire is just hanging on the connectors/wires that are connected to the PCB. This is not right, and if a connection breaks due to prolonged strain it will be a pain to repair (and also, it may cause shorting or other problems). So, I recommend to think of and implement something that holds the PCBs and wires in-place without straining the JST-SM connectors or their wires. 

## ATX powersupplies:
We have 6 ATX PSU's that have been wired to just output 5V. On these PSUs, the green wire (PSU-ON) is wired to ground such that the power supplies are always on. Each power supply has at least 3 conductors going from the 5V rail to a WAGO clip. The WAGO clips are supposed to be permanently attached to the PSUs, as it can be a pain to squeeze the wires in the WAGO clips. All other wires are tucked to the inside of the power supplies and isolated per rail with isolation tape. 


# 2. LEDbeams Crew-area
![image](https://github.com/EloySchultz/2023-Beun-LANCo/assets/99472685/9b6a3c87-4586-4185-a5b0-46bf1939bf2a)

The crew-area is usually a U- or L-shaped group of tables that is separated from the rest of the LAN. This area hosts the most valuable people at the LAN, soooo we gotta accentuate that with some LEDs of course! To achieve this, the LANCo owns 10 beams of ~1.8 meters that have 60 leds/m WS2812b LED strips attached. There are 106 LEDs per beam (although this is slightly different for some damaged LED beams). The beams are placed at the front-side of the tables, and 10 diffuser panels are placed in front of it. The diffuser panels consists of a plastic frame and fabric that is squished into the frames with rubbers (much like a hor, the fabric is squished in with this stuff (https://www.praxis.nl/badkamer-keuken-wonen/horren/accessoires/bruynzeel-pees-en-rollerset/5609465)). The diffuser panels are attached to the ledbeams with small wooden beams and some screws. 

I highly recommend to NOT chain more than 2 LEDbeams per PSU due to current losses in the LEDstrips.  
## How we did it at TesLAN 6

https://youtu.be/yT-bN0SuYpE
For TesLAN 6, we used the following wiring. Please note that I do not recommend to use this wiring for future editions. 
![image](https://github.com/EloySchultz/2023-Beun-LANCo/assets/99472685/4ca987e2-1cc2-42c6-80d7-1bf7fa666d44)
The idea is that the powersupply is in the center of two beams, thus creating minimal in-strip resistive losses. For controllers, we simply use ESP8266 nodeMCU V3 boards with a JST-SM male connector attached to it. This controller hangs on the input side of the beams, and will receive power through the rails of the led strip. 

On the ESP8266, the same code in the folder Arduino_esp_code/ is used. Make sure to switch to the correct device in the Arduino IDE before uploading.
## How we recommend doing it on TesLAN 7+
The above setup had some problems. The JST connectors are very prone to break during transport if they are not glued down. This meant that during the LAN, we had to manually re-solder these connections. That is not fun in the dark. Aside from this, the 5V and GND conductors are not thick enough for the amount of current that is required, hence you need to parallel-wire thick speaker wire to each led beam anyway, essentially making two of the three conductors in the JST-SM connector redundant. 

Another problem occurred with the Wi-Fi. During the LAN, it is apparently very busy on the 2.4GHz band; Many people are using either Wi-Fi, Bluetooth or both. So much so, that putting beun devices that need a constant, uninterrupted stream of packets on Wi-Fi turned out to be a really bad idea. Devices were barely receiving any packets during busy times, sometimes reaching up to >3 seconds per update. Many packets were dropped or delayed, so much so that it was at times not possible to have the led beams act in sync, nor to blank the led beams.  
For future editions, I recommend a setup like this:
![image](https://github.com/EloySchultz/2023-Beun-LANCo/assets/99472685/ddb42aaf-e751-4464-bd36-5344b5948b58)
So still 2 ledbeams per PSU and PSU in the middle, but instead we use LAN-based controllers, and we only connect the grounds and data wires together. Aside from this, we use only 2 instead of 5 controllers, further negating sync issues. 

# 3. Logo
![image](https://github.com/EloySchultz/2023-Beun-LANCo/assets/99472685/356c56bc-a6a1-4140-884d-d32d3ec43b53)

In previous years, there was a large TesLAN logo on the wall behind the crew-area. This was first achieved by building the logo out of cardboard, and from the 4th edition a large PVC logo was built that was lit up using EL-Wire. However, this logo was a pain to set up and the EL-wire PSU broke at the 5th edition of the TesLAN. Hence, a new solution was needed.

For TesLAN 6, we rented a laser projector and FB3 interface from T-organisations. The laser can project shapes by quickly rotating mirrors (scanners), such that the laser point moves quickly and to our pesky human eyes it looks like solid lines. The physical setup looks like this:

https://youtube.com/shorts/J3oQPthkkY8

There is a small PC in the truss that has quickshow on it and that is connected with an FB3 interface to the laser through ILDA. The computer is remote controlled using nomachine. 

In order to create animations/graphics for the laser, we have set up the following pipeline: 

## 3.1 Figure creation
Use either Adobe Illustrator for still images, or Adobe Animate to generate animations. Make sure that all figures in the image only have a border/outline and don't have a fill. In case of an animation, it is imperative that the first frame of the animation contains all colors for that animation. I.e. you cannot introduce a new color halfway through the animation, if it was not also present in the first frame of the animation. Another limitation: we currently do not support mask tags, meaning that you cannot use masks in Adobe Animate. Export your frame/animation as an SVG file/sequence. 

## 3.2 SVG Processing (this is very beun, find a better alternative please)
This is where the magic happens. We have SVG image(s) that consist of vectors, but we need a sequence of points that our laser point needs to jump to. Furthermore, the laser needs to know for each move if the laser should be enabled and what color the laser should be during the movement. 

I have taken an SVG2ILD script from OpenLase(https://github.com/marcan/openlase) and I have modified it to support xlink tags, transforms, and color (both CSS style header and in-tag stroke). The script reads an SVG file, and then using SAX XML parser and alot of magic we extract a list of points, the color and whether the laser should be on/off during the movement. The color table is generated based on the first frame on an animation, and is put in a seperate ILDA section (see docs/ILDA_IDTF14_rev011.pdf for complete ILDA transfer specification that we use). The points are then sorted in the same way that OpenLase sorts them.. I recommend you check the script yourself to understand what is going on!

To convert .svg files, go to Logo/SVG2ILD/run.py and put in the files there and then simply run it using python. There is a seperate section for single frames and for video SVG sequences. The main magic is happening in Logo/SVG2ILD/core.py. The script will output the .ild (ILDA) files in Logo\SVG2ILD\ILDA.

These IDLA files can then be loaded into a laser program of choice. For this year, we will use pangolin quickshow as we have a pangolin FB3 interface for our laser. In quickshow, we simply import the .ild files as figures, and then we use the quickshow features to create a lasershow consisting of various animations. In quickshow, we can also adjust the laser for non-normal projection (keystone correction, video: https://www.youtube.com/watch?v=BOX0U0b0qSE). 

During the LAN, you can tune the settings in Logo/SVG2ILD/core.py so that the ILDA files are optimized for the laser. The dwell settings and speed can influence how many points have to be drawn by the laser, so these settings can influence flickering in the final image.  

Something to note: The sorting algorithm that is adopted from OpenLase is bad. It sucks. This algorithm should be revised. Joris and I have an algorithm laying around for this (send Joris or me (Eloy) a message if you need this), but please be aware that it will probably cost quite some time and effort to implement this into the OpenLase script. Therefore, I recommend that you search for a different way to convert images to ILDA for the future.

# 4. SyncStream
![image](https://github.com/EloySchultz/2023-Beun-LANCo/assets/99472685/46f08c7a-a550-4cea-8a8a-0216f8bc6819)

SyncStream is a protocol for streaming rgb data directly to microcontrollers with LEDs in real-time over (W)LAN. The idea is simple: LEDs on a device retain their state unless the microcontroller receives an update for that LED. An update consists of a UDP packet that consists of groups of 3 bytes. The first 12 bits encode the LED index (0-4095), after which 3 sections of 4 bits each encode the value for red, green and blue respectively (0,15).   
SyncStream has two parts: one program that runs on the beun devices (that you can find in /Arduino_esp_code) and the other that runs on a computer that acts as a server (find this in /SyncStream). Mathijs and Max did a great job writing SyncStream in the past, which is why for this year I felt like it was a great idea to mostly ignore their work and instead beun together a GUI that can act as a server (TesLAN Beun Manager). TBM allows for allows for easy managing of all beun devices in the hall. You run it by running /SyncStream/Multi_device_GUI/main.py. Essentially, TBM spawns a process for each beun device and provides an overview and controls over all child processes. Aside from this, TBM allows for beun devices to be grouped, or nested in virtual devices such that a group of devices acts as one large device. Groups can also be activated in a wave-like pattern, such that it looks like a wave is going through the hall, which is achieved by spawning processes with a delay based on the location of the devices in the hall.

Want a tutorial? Here is sleep-deprived me at 1 AM on the 2nd night of TesLAN 6 trying to explain it:

https://www.youtube.com/watch?v=qlxQvPsAu7o

BTW, the code for TBM is pretty horrible cuz I beuned it together in a rush and I don't care about unclear and vague variable assignments lol. If you do the wrong thing, you can make it crash. Someone should probably have a good look at it and make it nice and proper. 



# 5. Beamer stuff
![image](https://github.com/EloySchultz/2023-Beun-LANCo/assets/99472685/76ddfb7c-26c7-416a-9104-b10df8178eb8)

So the beamer needs to hang of the Truss, and we never had a proper solution for this. For TesLAN 6, I revived the old beamer platform that was built previously. The design consists of two wooden rectangles with a platform in the middle for the beamer to sit on. I improved the design by completing the loops (adding a beam underneath the platform) and by slightly reinforcing the corners. Howerver, in the future, some cross beams should be added so that we can stop the beamer assembly from wiggling around as much. 


# 6 Switch stuff
The switches hang between the tables on two wooden beams. These beams are in a bag that is separated from the crew-area beams. They are approx 25 cm in length and have a hole where a 3.5 mm 30mm screw goes. One screw per rack ear is enough. Perhaps in next years we want slightly thinner screws (like 3mm), because I recall one of the network guys saying that the big screws may damage the racke ears a bit. Make sure to check this with the network guys.

---

# Misc. notes for TesLAN 7+
Some notes:
- Check ledbeam 4. It was not working properly during the 6th TesLAN and I don't know why. I think that the data line might be shorted to ground or to VCC, but I did not manage to fix this during the TesLAN 6.
- Remove labels from seinpalen and put them higher up the seinpaal. They are currently at the bottom of each sein, but this area will get covered with tape during assembly. 
- Seinpaal 8 has a new pro-mini that has a reversed serial interface! This means that you need to connect the arduino to the FTDI programmer upside down!
- If seinpaal uses mains cable for power:  blue is GND and brown is VCC. Most of them have a label on them that specifies this.
- In TBM, I made it so that packets are spammed, but you may not want this. SyncStream was made to only send a packet whenever an LED needs to be updated. However, for TesLAN 6 we were running our crew-area panels on WiFi (this sucked). I noticed that by spamming many more packets (i.e., send over the entire frame buffer every time), it was more likely that packets came through. However, since in the future you should absolutely refrain from using WiFi at all, you can probably revert this back to how it was before (sending only the updates). Note that for some animations such as the flames, you will still need to send over almost the entire framebuffer.

---

# General tips for doing beun at the TesLAN:
Below, some general tips and tricks for doing beun at the TesLAN. 

1. Go to storage often to index what you have and what you need to buy. Please remember that things regularly break and despawn in storage.
Please test all beun long BEFORE the TesLAN. That usually entails taking stuff home, building a test setup and testing if it actually works. I know this can be quite alot, so keep track of the status of each beun device in an excelsheet (like I did in `Ouwe beun meuk voor Teslan 6.xlsx` on mjolnir, please note that this document is outdated but it may give you an idea on how to keep track of what is broken). It is quite important that you test stuff at home so that you can make an accurate budget. Don't just assume that things will be working when they come out of storage. They. Wont. 

2. Consider to bring the following tools to the LAN:
- Both torx bit screwdrivers and phillips bit screwdrivers (we have both types of screws, there is no coherence)
- Battery powered drill 
- Also smaller screwdrivers for things like kroonsteentjes (altough I have done my very best to replace all kroonsteentjes with WAGO clips)
- Adjustable LAB bench powersupply with OCP (please, test things before you connect them with a regular PSU)
- Multimeter
- Soldering iron (bonus points if it is wireless, since especially for the crew area panels you will be running around alot), tin, desolder wick
- Strippers (not the human kind), clippers, tweezers
- Isolation tape, zipties, etc.
- Small head lamp

3. Put the following items on the beun budget if we do not have them in storage:
- Screws (3.5x30mm and 3.5x40mm) --> This was unforeseen on TesLAN 6
- CR2032 batteries --> This was unforeseen on TesLAN 6, were needed for LASER PC. 
- Speaker wire --> this is always handy to have, especially when bodging together the crew area panels.

4. Communicate beforehand with the network wizards what your MAC adresses are and what IP adresses they will have on the LAN. This simplifies your life. They should put all beundevices on a separate VLAN, such that not everyone at the LAN can access the beun devices. If you have a list of IP adresses, I recommend programming this list in devices.h.
Also, for the seinpalen specifically, many of our cables have one and where the clip is broken. The end where the clip is not broken goes into the seinpaal, as otherwise the cable falls out. The other (broken) end goes into the switch. This means that sometimes, a seinpaal might stop working because the cable somehow wiggled it's way out of the switch. That's life! Just reseat the cable and power cycle the seinpaal. 
5. Be in time with your beun budget. It can take 3 weeks or more before your budget is fully approved, so please submit your budget in-time with some margin. You can check Mjolnir for the format of the beun budget. 
6. Keep track of what people buy (also unforeseen) and put this in the beun financial result. Make sure that you do this fairly!  

That's it. Remember to also have fun lmao!

 > Beun is beun. Beun is goei. Beun is an experiment. Beun is fun. Do beun.



