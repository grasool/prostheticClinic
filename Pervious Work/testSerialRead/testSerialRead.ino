

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
}
int s = -1;
void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    s = (int)Serial.read();
    //Serial.println(s);
    if(s == 49){
      digitalWrite(LED_BUILTIN,HIGH);
      //Serial.print("ON");
      delay(10);
    }
    if(s == 48){
      digitalWrite(LED_BUILTIN,LOW);
      //Serial.print("OFF");
      delay(10);
    }
  }
}
