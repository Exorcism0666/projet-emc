#include <LiquidCrystal.h>

// Initialisation de l'écran LCD
LiquidCrystal lcd_1(12, 11, 5, 4, 3, 2);

// Définition des constantes et variables
const int buttonPin = 7;
bool isAnimating = false;
bool isWaitingForButton = false; // on attendra l'ordre depuis Python
unsigned long previousMillis = 0;
unsigned long animationStartTime = 0;
const unsigned long animationDuration = 5000;
int result = 0;

void setup() {
  lcd_1.begin(16, 2);
  lcd_1.print("En attente des");
  lcd_1.setCursor(0, 1);
  lcd_1.print("joueurs...");

  randomSeed(analogRead(0));
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600); // Démarrage de la communication série
}

void loop() {
  unsigned long currentMillis = millis();

  // Vérifier si un signal vient du PC pour autoriser un lancer
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    if (input == "start") {
      isWaitingForButton = true;
      lcd_1.clear();
      lcd_1.print("Lancement du de!");
      lcd_1.setCursor(0, 1);
      lcd_1.print("Appuyer bouton!");
    }
  }

  // Attente de l'appui du bouton
  if (isWaitingForButton && digitalRead(buttonPin) == LOW) {
    delay(300);
    while (digitalRead(buttonPin) == LOW);
    isWaitingForButton = false;
    isAnimating = true;
    animationStartTime = currentMillis;
    previousMillis = currentMillis;
    
    lcd_1.clear();
    lcd_1.print("Lancement du de!");
  }

  // Animation du lancer
  if (isAnimating) {
    if (currentMillis - previousMillis >= 75) {
      previousMillis = currentMillis;
      lcd_1.setCursor(0, 1);
      for (int i = 0; i < 16; i++) {
        lcd_1.print(random(1, 7));
      }
    }

    if (currentMillis - animationStartTime >= animationDuration) {
      isAnimating = false;
      result = random(1, 7);
      Serial.println(result);
      lcd_1.clear();
      lcd_1.setCursor(0, 0);
      lcd_1.print("Resultat: ");
      lcd_1.print(result);
      delay(5000);
      lcd_1.clear();
      lcd_1.print("En attente des");
      lcd_1.setCursor(0, 1);
      lcd_1.print("joueurs...");
    }
  }
}
