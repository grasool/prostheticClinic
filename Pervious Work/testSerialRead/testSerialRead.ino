

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
}
int s = 0;
void loop() {
  // put your main code here, to run repeatedly:
  Serial.print(Serial.available());
  if(Serial.available()){
    s += 1; //(int)Serial.read();
    //Serial.println(s);
    if(s%2 == 0){
      digitalWrite(LED_BUILTIN,HIGH);
      Serial.print("ON");
      delay(100);
    }
    if(s%2 == 1){
      digitalWrite(LED_BUILTIN,LOW);
      Serial.print("OFF");
      delay(100);
    }
  }
}
