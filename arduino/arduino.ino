#include <LiquidCrystal.h>
#include "DHT.h"

#define DHTPIN A1 // define hardware
#define DHTTYPE DHT11

// temp/humi probe
DHT dht(DHTPIN, DHTTYPE);

int delayTime = 5000;

// vars for LCD
int Contrast = 50;
LiquidCrystal lcd(9, 8, 5, 4, 3, 2); 

void setup() {
  Serial.begin(9600);

  dht.begin(); // initialize the sensor
  
  analogWrite(6,Contrast); // LCD setup
  lcd.begin(16, 2);

}

void loop() {
  
  // read humidity
  float humi  = dht.readHumidity();
  // read temperature as Celsius
  float tempC = dht.readTemperature();
  // read temperature as Fahrenheit
  float tempF = dht.readTemperature(true);

  // check if any reads failed
  if (isnan(humi) || isnan(tempC) || isnan(tempF)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print("Humidity: ");
    Serial.print(humi);
    Serial.print(" %");
    Serial.print("  |  "); 
    Serial.print("Temperature: ");
    Serial.print(tempC);
    Serial.print(" °C ~ ");
    Serial.print(tempF);
    Serial.println(" °F");

    // print to LCD
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.setCursor(6,0);
    lcd.print(tempC,1);
    lcd.setCursor(11,0);
    lcd.print("C");
    lcd.setCursor(0, 1);
    lcd.print("RH: ");
    lcd.setCursor(6,1);
    lcd.print(humi,1);
    lcd.setCursor(11,1);
    lcd.print("%");

    // wait a few seconds between measurements.
    delay(delayTime);
  }
}
