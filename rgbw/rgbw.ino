//#define FASTLED_FORCE_SOFTWARE_PINS
//#define FASTLED_ESP8266_NODEMCU_PIN_ORDER
//#define FASTLED_ALLOW_INTERRUPTS 0
#include "FastLED.h"
#include "FastLED_RGBW.h"
#define BAUD_RATE 115200
#define DATA_PIN 2
#define HASH_LENGTH 6

char i_msg[] = {'N', 'e', 'b', 'u', 'l', 'a', '\0'};
char f_msg[] = {'F', 'r', 'a', 'm', 'e', 's', '\0'};
bool found_app = false;
bool set_config = false;
int init_pos = 0;
byte num_led = 100;
CRGBW leds[100];
CRGB *ledsRGB = (CRGB *) &leds[0];
int brightness = 80;

void setup() {
  Serial.begin(BAUD_RATE);
  FastLED.addLeds<WS2812B, DATA_PIN, RGB>(ledsRGB, getRGBWsize(num_led));
  FastLED.setBrightness(brightness);
  memset(leds, 0, num_led * sizeof(struct CRGB));
  disconnected();
}

void loop() {
  if (!found_app) {
    while (!Serial.available()) {
      Serial.write("A");
      delay(300);
    }
    if (checksum(i_msg)) {
      found_app = true;
      Serial.write('C');
    }
  }
  else if(!set_config){
    Serial.write('T');
    while (Serial.available()) {
      Serial.write('H');
      num_led = Serial.read();
      set_config = true;
      Serial.write(num_led);
    }
  }
  else {
    if (checksum(f_msg)) {
      show_rgb();
    }
  }
}

bool checksum(char *msg) {
  while (Serial.available()) {
    char message = Serial.read();
    if(message == 'D'){
        found_app = false;
        break;
    }
    if (message != '\n' && msg[init_pos] == message) {
      init_pos++;
      if (init_pos == HASH_LENGTH) {
        init_pos = 0;
        return true;
      }
    } else {
      init_pos = 0;
    }
  }
  return false;
}

void show_rgb() {
  for (uint8_t i = 0; i < num_led; i++) {
    byte r, g, b;
    while (!Serial.available()) ; ;
    r = Serial.read();
    while (!Serial.available()) ; ;
    g = Serial.read();
    while (!Serial.available()) ; ;
    b = Serial.read();
    leds[i].r = r;
    leds[i].g = g;
    leds[i].b = b;
  }
  FastLED.show();
}

void disconnected() {
  for (uint8_t i = 0; i < num_led; i++) {
    leds[i].r = 0;
    leds[i].g = 1;
    leds[i].b = 0;
  }
  FastLED.show();
}
