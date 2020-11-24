#include <LiquidCrystal.h>
#include <DHT.h>

// delay between readings (ms)
int delayTime = 5000;

// vars for LCD
int Contrast = 50;
LiquidCrystal lcd(9, 8, 5, 4, 3, 2);

// sensor
DHT dht(A1, DHT11);

void setup()
{
  Serial.begin(9600);

  // initialize the sensor
  dht.begin();

  // LCD setup
  analogWrite(6, Contrast);
  lcd.begin(16, 2);
}

void loop()
{

  // read humidity
  float humi = dht.readHumidity();
  // read temperature (C)
  float temp = dht.readTemperature();

  // check if any reads failed
  if (isnan(humi) || isnan(temp))
  {
    Serial.println("Failed to read from DHT sensor!");
  }
  else
  {
    // print to serial. This will be read by the rpi
    Serial.print("Humidity: ");
    Serial.print(humi);
    Serial.print(" %");
    Serial.print("  |  ");
    Serial.print("Temperature: ");
    Serial.print(temp);
    Serial.print(" °C");

    // print to LCD
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.setCursor(6, 0);
    lcd.print(temp, 1);
    lcd.setCursor(11, 0);
    lcd.print("C");
    lcd.setCursor(0, 1);
    lcd.print("RH: ");
    lcd.setCursor(6, 1);
    lcd.print(humi, 1);
    lcd.setCursor(11, 1);
    lcd.print("%");

    // delay between readings
    delay(delayTime);
  }
}
