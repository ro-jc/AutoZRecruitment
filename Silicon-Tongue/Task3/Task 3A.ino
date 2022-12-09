#include <Adafruit_LiquidCrystal.h>
#include <Keypad.h>

Adafruit_LiquidCrystal lcd(0);

char keys[4][4] = {
  {'1','2','3', 'A'},
  {'4','5','6', 'B'},
  {'7','8','9', 'C'},
  {'*','0','#', 'D'}
};

byte pin_rows[4] = {10, 9, 8, 7};
byte pin_column[4] = {6, 5, 4, 3};

Keypad keypad = Keypad(makeKeymap(keys), pin_rows, pin_column, 4, 4);

String decimal_string = "";
char hex[14];

void setup(){
  lcd.begin(16, 2);
}

bool clear = false;
void loop(){
  char key = keypad.getKey();
  if (key) {
    if (key!='#' and decimal_string.length()!=16) {
      decimal_string += key;
      
      if (clear) {
      	clear_line(0);
        clear = false;
      }
      lcd.print(key);
    } else {
      sprintf(hex, "%X", decimal_string.toInt());
      
      clear_line(1);
      lcd.print("0x");
      lcd.print(hex);
      
      clear = true;
      decimal_string = "";
    }
  }
}

void clear_line(int line) {
  lcd.setCursor(0,line);
  lcd.print("                ");
  lcd.setCursor(0,line);
}
