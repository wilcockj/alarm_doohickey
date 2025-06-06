/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink
*/
#define ALARM_POW_PIN 13
// the setup function runs once when you press reset or power the board


void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(ALARM_POW_PIN, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600); 
  setCpuFrequencyMhz(10); // or even 40 if you're not doing much
}
int incomingByte = 0;

// the loop function runs over and over again forever
void loop() {

  if (Serial.available() > 0) {

      // read the incoming byte:
      char buf[20];
      int read_num = Serial.readBytesUntil('\n',buf,20);
      buf[read_num] = '\0';
      if(strcmp(buf,"True")==0){
        digitalWrite(ALARM_POW_PIN, HIGH);
        digitalWrite(LED_BUILTIN, HIGH);
      }
      else if(strcmp(buf,"False")==0){
        digitalWrite(ALARM_POW_PIN, LOW);
        digitalWrite(LED_BUILTIN, LOW);
      }
  }
  delay(10);
}
