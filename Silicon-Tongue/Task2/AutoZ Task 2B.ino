// Scaling Factor
const float scale = 0.249266862;

// Potentiometer reading
int potVal;

// Motor connections
int e12 = 9;
int i1 = 8;
int i2 = 7;

// LED connections
int e34 = 3;
int i3 = 5;
int i4 = 4;


void setup() {
	// Declare control pins as outputs
	pinMode(e12, OUTPUT);
	pinMode(i1, OUTPUT);
	pinMode(i2, OUTPUT);
	pinMode(e34, OUTPUT);
	pinMode(i3, OUTPUT);
	pinMode(i4, OUTPUT);
  	
	// Set combinations required to move motor and turn on LED
	digitalWrite(i1, HIGH);
	digitalWrite(i2, LOW);
	digitalWrite(i3, HIGH);
	digitalWrite(i4, LOW);
}


void loop() {
  	// Read potentiometer input
  	potVal = analogRead(A5);
    
    // Write using PWM after scaling value down to 255 
    analogWrite(e12, potVal*scale);
    analogWrite(e34, abs(1023-potVal)*scale);
}