
#include <Wire.h>
#include <Adafruit_AMG88xx.h>
#include<cvzone.h>

SerialData serialData(2, 1);

Adafruit_AMG88xx amg;

float pixels[AMG88xx_PIXEL_ARRAY_SIZE];
int action[2];
int flash = 7;
int buzzer = 8;

void setup() {
  serialData.begin(9600);

  bool status;
  pinMode(buzzer, OUTPUT);
  pinMode(flash, OUTPUT);

  status = amg.begin();
  if (!status) {
    Serial.println("Could not find a valid AMG88xx sensor, check wiring!");
    while (1);
  }

  Serial.println();
  digitalWrite(flash, HIGH);

  delay(100);
}


void loop() {
  serialData.Get(action);

  amg.readPixels(pixels);

  Serial.print("[");
  for (int i = 1; i <= AMG88xx_PIXEL_ARRAY_SIZE; i++) {
    Serial.print(pixels[i - 1]);
    Serial.print(", ");
    if ( i % 8 == 0 ) Serial.println();
  }
  Serial.println("]");

  digitalWrite(action[0], action[1]);

  delay(500);
}
