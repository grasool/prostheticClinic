/*************************************************** 
  This is an example for our Adafruit 16-channel PWM & Servo driver
  Servo test - this will drive 8 servos, one after the other on the
  first 8 pins of the PCA9685

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/products/815
  
  These drivers use I2C to communicate, 2 pins are required to  
  interface.

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
// you can also call it with a different address and I2C interface
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(&Wire, 0x40);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define OPEN 150 // this is the 'minimum' pulse length count (out of 4096)
#define CLOSED 400 //550 // this sis the 'maximum' pulse length count (out of 4096)//550
#define REST 275

//pinky = servo 4
//ring = servo 3
//middle = servo 2
//pointer = servo 1
//thumb = servo 0

// our servo # counter
uint8_t servonum = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("8 channel Servo test!");

  pwm.begin();
  
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  delay(10);
}

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000000;  // convert to us
  pulse /= pulselength;
  Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}
int s = 0;
void loop() {
  // Drive each servo one at a time
  //Serial.println(servonum);
  if(Serial.available()){
    s = (int)Serial.read();
    Serial.println(s);
    switch(s){
      case 48://1
        allOpen();
        break;
      case 49://2
        allClosed();
        break;
      case 50:
        allRest();
        break;
      case 51:
        initialize();
        break;
      case 52://4
        //middleFinger();
        pinkyOut();
        break;
      case 53://5
        cycleFingers();
        break;
      case 54:
        pointFinger();
        break;
      case 55:
        rockOut();
        break;
      case 56://8
        testEachFinger(1000);
        break;
      case 57: 
        thumb(CLOSED);
        break;
      case 98:
        thumb(OPEN);
        break;
    }
      
    
  }
}

void allClosed(){
 int thumbClose = CLOSED;
  allFingers(thumbClose);
}

void allOpen(){
  allFingers(OPEN);
}

void allRest(){
  allFingers(REST);
}

void allFingers(int pos){
  pinky(pos);
  middle(pos);
  ring(pos);
  pointer(pos);
  thumb(pos);
}

void pinky(int pos){
  Serial.println("Pinky");
  pwm.setPWM(4,0,pos);
  
}

void ring(int pos){
  pwm.setPWM(3,0,pos);
}

void middle(int pos){
  pwm.setPWM(2,0,pos);
}

void pointer(int pos){
  pwm.setPWM(1,0,pos);
}

void thumb(int pos){
  pwm.setPWM(0,0,pos);
}

void initialize(){
  allOpen();
  delay(2000);
  allClosed();
  delay(2000);
  testEachFinger(500);
  delay(1000);
  pointFinger();
  delay(1000);
  rockOut();
  delay(1000);
  allOpen();
 
}

void cycle(int t,int dir){
  thumb(dir);
  delay(t);
  pointer(dir);
  delay(t);
  middle(dir);
  delay(t);
  ring(dir);
  delay(t);
  pinky(dir);
  delay(t);
  
}

void cycleFingers(){
  cycle(400,CLOSED);
  cycle(400,OPEN);
}



void testEachFinger(int t){
  thumb(CLOSED);
  delay(t);
  thumb(OPEN);
  delay(t);
  pointer(CLOSED);
  delay(t);
  pointer(OPEN);
  delay(t);
  middle(CLOSED);
  delay(t);
  middle(OPEN);
  delay(t);
  ring(CLOSED);
  delay(t);
  ring(OPEN);
  delay(t);
  pinky(CLOSED);
  delay(t);
  pinky(OPEN);
  delay(t);
}

void pointFinger(){
  thumb(OPEN);
  pointer(OPEN);
  middle(CLOSED);
  pinky(CLOSED);
  ring(CLOSED);
}

void pinkyOut(){
  allClosed();
  pinky(OPEN);
}

void rockOut(){
  thumb(OPEN);
  pointer(OPEN);
  pinky(OPEN);
  ring(CLOSED);
  middle(CLOSED);
}

void middleFinger(){
  allClosed();
  middle(OPEN);
}





