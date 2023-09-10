#include <dht.h>

dht DHT;

#define DHT11_PIN 2

void setup() {
  pinMode(DHT11_PIN, INPUT);
  
  Serial.begin(9600);

}

void loop() {
  int chk = DHT.read11(DHT11_PIN);
  float room_farenheit = DHT.temperature * 9.0/5.0 + 32.0;
  float room_humidity = DHT.humidity;
  Serial.println((String)room_farenheit + "," + room_humidity);
  delay(1000);
}