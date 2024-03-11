#define DIR_PIN 2
#define STEP_PIN 3
#define STEPS_PER_REVOLUTION 400 // Assuming 1/2 microstepping (200 * 2)


void setup() {
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0){
    String incomingData = Serial.readString();
    Serial.print("Arduino received: ");
    Serial.println(incomingData);

    if(incomingData == "0"){
      //Blink
    }
    else if (incomingData == "1"){
      rotateToAngle(120);
    }
    else if (incomingData == "2"){
      rotateToAngle(240);
    }
  }
}

void rotateToAngle(int targetAngle){
  if(targetAngle == 120){
    rotateBackAndForth(STEPS_PER_REVOLUTION/3);
  }
  else if(targetAngle == 240){
    rotateBackAndForth((STEPS_PER_REVOLUTION/3) * 2);
  }
}

void rotateBackAndForth(int steps){
  digitalWrite(DIR_PIN, HIGH); // Set direction
  for(int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(500); // Adjust speed by changing delay
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(500); // Adjust speed by changing delay
  }
  delay(5000); // Wait before reversing direction
  
  // Rotate counterclockwise
  digitalWrite(DIR_PIN, LOW); // Set direction
  for(int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(500); // Adjust speed by changing delay
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(500); // Adjust speed by changing delay
  }
  delay(5000); 
}
