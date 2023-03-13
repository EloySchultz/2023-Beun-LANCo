//SEINPAAL SPECIFIC CONSTANTS
#if defined(SEINPAAL_1)
	byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x07};
	byte ip[] = { 192, 168, 2, 150 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_2)
	byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x08};
	byte ip[] = { 192, 168, 2, 151 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(ESP_SEINPAAL_2)
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x08};
  byte ip[] = { 192, 168, 2, 151 };
  #define DATA_PIN 5 //On ESP we use D1 (GPIO5) as output.
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_3)
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x09};
  byte ip[] = { 192, 168, 2, 152 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_4)
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0A};
  byte ip[] = { 192, 168, 2, 153 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_5)
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0B};
  byte ip[] = { 192, 168, 2, 154 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_6)
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0C};
  byte ip[] = { 192, 168, 2, 155 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_7)
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0D};
  byte ip[] = { 192, 168, 2, 156 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif

#if defined(SEINPAAL_8)
  byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x0E};
  byte ip[] = { 192, 168, 2, 157 };
  #define DATA_PIN 3 //On Arduino we use D3 as data out
  #define NUM_LEDS 300 //Seinpaal has 300 LEDs
#endif
