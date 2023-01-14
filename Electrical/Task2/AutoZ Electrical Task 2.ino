void setup()
{
  Serial.begin(9600);
}

void loop()
{
  // Scale down to 30 by multiplying with (30/1023)
  Serial.println(analogRead(A1)*0.029325513);
}