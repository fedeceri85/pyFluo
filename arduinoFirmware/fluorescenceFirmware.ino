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

  http://www.arduino.cc/en/Tutorial/Blink
*/
#define INTERRUPT_INPUT 2
#define LED365 7
#define LED385 8
#define CAMTRIG 9
volatile byte current;
volatile byte state = LOW;
volatile byte LED = HIGH;
unsigned long previous; //How much time since previous interrupt
// the setup function runs once when you press reset or power the board
int exp365 = 100;
int exp385 = 12;
int intDelay = 20;
int ifi = 100; // interFrameinterval
int ifiDelay = ifi-exp365-exp385-intDelay;
int state2 = 0;
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  Serial.begin(9600);
  Serial.setTimeout(100); 
  pinMode(LED385, OUTPUT);
  pinMode(LED365, OUTPUT);
  pinMode(CAMTRIG, OUTPUT);
  digitalWrite(LED365, LOW);
  digitalWrite(LED385, LOW);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_INPUT), blink, CHANGE);
}

// the loop function runs over and over again forever
void loop() {

   if (state2 ==1){
      LED = HIGH;
      digitalWrite(CAMTRIG, HIGH);// turn the LED on (HIGH is the voltage level)
      delay(exp365);                       // wait for a second
      digitalWrite(CAMTRIG, LOW); 
      delay(intDelay);  
      LED = LOW;  
      digitalWrite(CAMTRIG, HIGH);// turn the LED on (HIGH is the voltage level)
      delay(exp385);                       // wait for a secon
      digitalWrite(CAMTRIG, LOW); 
      delay(ifiDelay);
  }
  
}


void blink(){
  // Function that change the state of the LEDs every time an interrupt is reached
  //TODO RESET LED AND STATE IF TIMEOUT REACHED
  state =  digitalRead(INTERRUPT_INPUT); //!state;
 // RESET LED AND STATE IF TIMEOUT REACHED
//  if (millis()-previous>5000){ 
 //   LED = HIGH;
///    state = LOW;
//  }
  //previous = millis();
  // Switch the correct LED on or off.
  if (state2 ==1){
    if (LED){
  
          digitalWrite(LED365, state);
     
  
    }
    else{
  
          digitalWrite(LED385, state);
  
    }
  }
}


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    int state3 = Serial.parseInt(); //1: off, 2: alternate,3: 365 on, 4: 385 on
    int exp365_2 = Serial.parseInt();
    int exp385_2 = Serial.parseInt();
    int intDelay_2 = Serial.parseInt();
    int ifi_2 = Serial.parseInt();
    //
    
    Serial.print(state3);
    Serial.print(' ');
    Serial.print(exp365_2);
    Serial.print(' ');
    Serial.print(exp385_2);
    Serial.print(' ');
    Serial.print(intDelay_2);
    Serial.print(' ');
    Serial.print(ifi_2 );
    Serial.println(' ');
    switch (state3){
      case 1:
          digitalWrite(LED365, LOW);
          digitalWrite(LED385, LOW);
          LED = HIGH;
          state = LOW;
          state2 = 0;
          break;
        
      case 2:
          exp365 = exp365_2;
          exp385 = exp385_2;
          intDelay = intDelay_2;
          ifi = ifi_2;
          ifiDelay = ifi-exp365-exp385-intDelay;
          state2 = 1;
          break;
     case 3:
          current = digitalRead(LED365);
          digitalWrite(LED365, !current);
          LED = HIGH;
          state = LOW;
          state2 = 0;
          break;
     case 4:
          current = digitalRead(LED385);
          digitalWrite(LED385, !current);
          LED = HIGH;
          state = LOW;
          state2 = 0;
          break;
    }

  }
}
