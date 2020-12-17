#include <Wire.h>
void setup()
{
  Wire.begin();
  Serial.begin(9600);
}

void loop()
{
  Serial.println("Begin");
  Wire.beginTransmission(0x3F);
  Serial.println("write");
  Wire.write(0x05);
  Wire.endTransmission();
  Serial.println("request");
  Wire.requestFrom(0x06, 1);
  Serial.println("waiting...");
  while (Wire.available() == 0) {
  }
  int c = Wire.read();
  Serial.println("Done");
  Serial.println(c);
}

/*
 * sensor: 0x3F
   write 1 to 0x05
   wait 100ms
   Read 0x06
*/
