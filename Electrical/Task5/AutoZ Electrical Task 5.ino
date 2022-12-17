// Motor connections
#define direction_pin 2
#define speed_pin 5

// Scaling Factor
const float scale = 2.55;


void setup() {
  // Declare control pins as outputs
  pinMode(direction_pin, OUTPUT);
  pinMode(speed_pin, OUTPUT);
  
  // Begin Serial communication
  Serial.begin(9600);
}

int speed = 0;
void loop() {
  if (Serial.available()) {
    // Read speed
  	speed = Serial.parseInt();
    Serial.println(speed);
    
    // Set motor direction based on speed
    if (speed>=0) {
      digitalWrite(direction_pin, LOW);
    } else {
      digitalWrite(direction_pin, HIGH);;
    }
    
    // Run motor
  	analogWrite(speed_pin, abs(speed)*scale);
  }
}