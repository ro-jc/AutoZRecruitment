#include <Adafruit_LiquidCrystal.h>
#include <Keypad.h>

#define BUTTON_PIN 2

Adafruit_LiquidCrystal lcd(0);

char keys[4][4] = {
  {'1','2','3', 'A'},
  {'4','5','6', 'B'},
  {'7','8','9', 'C'},
  {'E','0','F', 'D'}
};

byte pin_rows[4] = {10, 9, 8, 7};
byte pin_column[4] = {6, 5, 4, 3};

Keypad keypad = Keypad(makeKeymap(keys), pin_rows, pin_column, 4, 4);

String hex_phrase = "0x";

void setup(){
  lcd.begin(16, 2);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop(){
  char key = keypad.getKey();
  if (key){
    hex_phrase += key;
  }

  if (digitalRead(BUTTON_PIN)==0) {
    lcd.clear();
    lcd.print(hex_phrase);
    hex_phrase = "0x";
    delay(50);
  }
}
