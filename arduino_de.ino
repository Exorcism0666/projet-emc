#include <LiquidCrystal.h>

// Initialisation de l'écran LCD
LiquidCrystal lcd_1(12, 11, 5, 4, 3, 2);

// Définition des constantes et variables
const int buttonPin = 7; // Broche du bouton
bool isAnimating = false; // Indique si l'animation est en cours
bool isWaitingForButton = true; // Indique si l'on attend un appui sur le bouton
unsigned long previousMillis = 0; // Stocke le temps pour le timing
unsigned long animationStartTime = 0; // Stocke le début de l'animation
const unsigned long animationDuration = 5000; // Durée de l'animation (5s)
int result = 0; // Résultat final du dé

void setup() {
  lcd_1.begin(16, 2);
  lcd_1.print("Lancement du de!");
  lcd_1.setCursor(0, 1);
  lcd_1.print("Appuyer bouton!");
  
  randomSeed(analogRead(0)); // Initialisation du générateur aléatoire
  pinMode(buttonPin, INPUT_PULLUP); // Activation du pull-up interne
}

void loop() {
  unsigned long currentMillis = millis(); // Temps actuel

  // Attente de l'appui du bouton
  if (isWaitingForButton && digitalRead(buttonPin) == LOW) {
    delay(300); // Anti-rebond
    while (digitalRead(buttonPin) == LOW); // Attendre le relâchement
    isWaitingForButton = false;
    isAnimating = true;
    animationStartTime = currentMillis;
    previousMillis = currentMillis;
    
    lcd_1.clear();
    lcd_1.print("Lancement du de!");
  }

  // Animation du lancer de dé
  if (isAnimating) {
    if (currentMillis - previousMillis >= 75) {
      previousMillis = currentMillis;
      lcd_1.setCursor(0, 1);
      
      for (int i = 0; i < 16; i++) {
        lcd_1.print(random(1, 9)); // Affichage de chiffres aléatoires
      }
    }

    // Arrêt de l'animation après le temps défini
    if (currentMillis - animationStartTime >= animationDuration) {
      isAnimating = false;
      result = random(1, 7); // Résultat final (1 à 6)
      lcd_1.clear();
      lcd_1.setCursor(0, 0);
      lcd_1.print("Resultat: ");
      lcd_1.print(result);
      delay(7500); // Affichage du résultat pendant 5s
      lcd_1.clear();
      lcd_1.print("Lancement du de!");
      lcd_1.setCursor(0, 1);
      lcd_1.print("Appuyer bouton!");
      isWaitingForButton = true;
    }
  }
}
