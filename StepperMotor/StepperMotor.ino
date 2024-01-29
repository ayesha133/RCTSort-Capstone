void setup() {
  // put your setup code here, to run once:
  Serial.begin()
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available > 0){
    char data = Serial.read();

    if(data == '0'){
      Serial.print('Recycling');
    }
    else if (data == '1'){
      Serial.print('Garbage');
    }
    else{
      Serial.print('Compost');
    }
  }
}
