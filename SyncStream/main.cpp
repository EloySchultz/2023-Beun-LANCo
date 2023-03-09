/*   Includes   */
#include <SPI.h>    
#include <FastLED.h>
#include "network_hardware.h"

#if defined(USING_WIZNET)
  #include <Ethernet.h>
  #include <EthernetUdp.h>
#elif defined(USING_ESP8266)
  #include <ESP8266WiFi.h>
  #include <WiFiUdp.h>
#elif defined(USING_ENC)
  #include <EthernetENC.h>
  #include <EthernetUdp.h>
#endif

/*   Init   */

#define LED_PACKET_BUFFER 320
#define NUM_LEDS 250
unsigned int localPort = 8888;
byte mac[] = {0xBE, 0xEF, 0x13, 0x37, 0xBE, 0x07};

#if defined(USING_WIZNET) || defined(USING_ENC)
  EthernetUDP Udp;
  #define UDP_TX_PACKET_MAX_SIZE LED_PACKET_BUFFER //24 bytes by default on Atmega. Very large on ESP
  #define DATA_PIN 3
#elif defined(USING_ESP8266)
  #define FASTLED_ESP8266_RAW_PIN_ORDER
  #define DATA_PIN 0
  #define WIFI_SSID "ssid"
  #define WIFI_PASS "pass"
  WiFiUDP Udp;
#endif

char packetBuffer[LED_PACKET_BUFFER];
CRGB leds[NUM_LEDS];

/*   Functions   */

void setup() {
#if defined(USING_WIZNET) || defined(USING_ENC)
  Ethernet.begin(mac);
#elif defined(USING_ESP8266)
  wifi_set_macaddr(0, const_cast<uint8*>(mac));
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(100);
#endif

  Udp.begin(localPort);
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
}

void parsePacket(int num){
  unsigned int iled;
  for (int i = 0; i<num; i++){
    iled = ((int)packetBuffer[i*3]<<4) + (((int)packetBuffer[i*3 + 1]&0b11110000)>>4); //first 1.5 bytes are led index
    leds[iled].r = (packetBuffer[i*3 + 1]&0b00001111)<<4;                   //4th half byte
    leds[iled].g =  packetBuffer[i*3 + 2]&0b11110000;                       //5th half byte
    leds[iled].b = (packetBuffer[i*3 + 2]&0b00001111)<<4;                   //6th=last half byte
  }
}

void loop() {
  int packetSize = Udp.parsePacket();
  if(packetSize) {
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE); //read to buffer
    parsePacket(packetSize/3);
    FastLED.show();
  }
}
