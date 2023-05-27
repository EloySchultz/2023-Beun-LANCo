// CONSTANTS FOR ALL DEVICES //
#define LED_PACKET_BUFFER 320
unsigned int localPort = 8888;
byte gateway[] = { 10, 20, 30, 1} ;
byte subnet[] = { 255, 255, 255, 0} ;


//DEVICE SPECIFIC CONSTANTS
#if defined(SEINPAAL_1)
  #define USING_WIZNET 1;
	byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x07};
	byte ip[] = { 10, 20, 30, 2};
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_2)
  #define USING_WIZNET 1;
	byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x08};
	byte ip[] = {  10, 20, 30, 3};
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif


#if defined(SEINPAAL_3)
  #define USING_WIZNET 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x09};
  byte ip[] = {  10, 20, 30, 4 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_4)
  #define USING_WIZNET 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0A};
  byte ip[] = {  10, 20, 30, 5 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_5)
  #define USING_WIZNET 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0B};
  byte ip[] = {  10, 20, 30, 6 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_6)
  #define USING_WIZNET 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0C};
  byte ip[] = {  10, 20, 30, 7 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_7)
  #define USING_WIZNET 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0D};
  byte ip[] = {  10, 20, 30, 8 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_8)
  #define USING_WIZNET 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0E};
  byte ip[] = {  10, 20, 30, 9};
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif


#if defined(LEDBEAM_1) //AKA LB 1+2
  #define USING_ESP8266 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0F};
  byte ip[] = {  10, 20, 30, 10 };
  #define DATA_PIN 0 //On ESP we use D3 as data out (GPIO0)
  #define NUM_LEDS 212 //Ledbeam has 106 LEDs, so 212 for two ledbeams
#endif

#if defined(LEDBEAM_2) //AKA LB 3+4
  #define USING_ESP8266 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x10};
  byte ip[] = {  10, 20, 30, 11 };
  #define DATA_PIN 0 //On ESP we use D3 as data out (GPIO0)
  #define NUM_LEDS 212 //Ledbeam has 106 LEDs, so 212 for two ledbeams
#endif

#if defined(LEDBEAM_3) //AKA LB 5+6
  #define USING_ESP8266 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x11};
  byte ip[] = {  10, 20, 30, 12 };
  #define DATA_PIN 0 //On ESP we use D3 as data out (GPIO0)
  #define NUM_LEDS 212 //Ledbeam has 106 LEDs, so 212 for two ledbeams
#endif

#if defined(LEDBEAM_4) //AKA LB 7+8
  #define USING_ESP8266 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x12};
  byte ip[] = {  10, 20, 30, 13 };
  #define DATA_PIN 0 //On ESP we use D3 as data out (GPIO0)
  #define NUM_LEDS 212 //Ledbeam has 106 LEDs, so 212 for two ledbeams
#endif

#if defined(LEDBEAM_5) //AKA LB 9+10
  #define USING_ESP8266 1;
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x13};
  byte ip[] = {10, 20, 30, 14};
  #define DATA_PIN 0 //On ESP we use D3 as data out (GPIO0)
  #define NUM_LEDS 212 //Ledbeam has 106 LEDs, so 212 for two ledbeams
#endif
