#include <LiquidCrystal.h>

// Déclaration de l'objet LiquidCrystal
LiquidCrystal lcd_1(12, 11, 5, 4, 3, 2);

// Variables globales
unsigned long previousMillis = 0; // Pour gérer le timing de l'animation
unsigned long animationDuration = 5000; // Durée de l'animation en millisecondes
bool isAnimating = false; // Indique si l'animation est en cours
int result = 0; // Résultat final du dé
const int buttonPin = 7; // Broche où le bouton est connecté
bool isWaitingForButton = true; // Indique si le programme attend l'appui du bouton

void setup()
{
  lcd_1.begin(16, 2); // Configure les colonnes et les lignes de l'écran LCD
  lcd_1.print("Lancement du de!");
  lcd_1.setCursor(0,1);
  lcd_1.print("Appuyer bouton!");
  randomSeed(analogRead(0)); // Initialise le générateur de nombres aléatoires
  pinMode(buttonPin, INPUT_PULLUP); // Configure la broche du bouton en entrée avec résistance de tirage interne
}

void loop()
{
  unsigned long currentMillis = millis(); // Récupère le temps écoulé depuis le démarrage

  if (isWaitingForButton)
  {
    // Attend que l'utilisateur appuie sur le bouton pour démarrer
    if (digitalRead(buttonPin) == LOW) // Si le bouton est pressé
    {
      delay(300); // Délai pour éviter les rebonds
      isWaitingForButton = false; // Arrête d'attendre l'appui du bouton
      isAnimating = true; // Démarre l'animation
      previousMillis = currentMillis; // Réinitialise le temps
      animationDuration = currentMillis + 5000; // Définit la durée de l'animation
    }
  }
  else if (isAnimating)
  {
    // Affiche une animation rapide de plusieurs chiffres
    if (currentMillis - previousMillis >= 75) // Change les chiffres toutes les 75 ms
    {
      previousMillis = currentMillis;

      // Génère des chiffres aléatoires pour chaque position
      int randomNumber1 = random(1, 9); // Chiffre 1
      int randomNumber2 = random(1, 9); // Chiffre 2
      int randomNumber3 = random(1, 9); // Chiffre 3
      int randomNumber4 = random(1, 9); // Chiffre 4
      int randomNumber5 = random(1, 9); // Chiffre 5
      int randomNumber6 = random(1, 9); // Chiffre 6
      int randomNumber7 = random(1, 9); // Chiffre 7
      int randomNumber8 = random(1, 9); // Chiffre 8
      int randomNumber9 = random(1, 9); // Chiffre 9
      int randomNumber10 = random(1, 9); // Chiffre 10
      int randomNumber11 = random(1, 9); // Chiffre 11
      int randomNumber12 = random(1, 9); // Chiffre 12
      int randomNumber13 = random(1, 9); // Chiffre 13
      int randomNumber14 = random(1, 9); // Chiffre 14
      int randomNumber15 = random(1, 9); // Chiffre 15
      int randomNumber16 = random(1, 9); // Chiffre 16

      // Affiche les chiffres sur l'écran LCD
      lcd_1.setCursor(0, 1); // Place le curseur sur la deuxième ligne
      lcd_1.print(randomNumber1);
      lcd_1.print(randomNumber2);
      lcd_1.print(randomNumber3);
      lcd_1.print(randomNumber4);
      lcd_1.print(randomNumber5);
      lcd_1.print(randomNumber6);
      lcd_1.print(randomNumber7);
      lcd_1.print(randomNumber8);
      lcd_1.print(randomNumber9);
      lcd_1.print(randomNumber10);
      lcd_1.print(randomNumber11);
      lcd_1.print(randomNumber12);
      lcd_1.print(randomNumber13);
      lcd_1.print(randomNumber14);
      lcd_1.print(randomNumber15);
      lcd_1.print(randomNumber16);
    }

    // Arrête l'animation après la durée spécifiée
    if (currentMillis >= animationDuration)
    {
      isAnimating = false;
      result = random(1, 7); // Génère le résultat final
      lcd_1.setCursor(0, 1); // Place le curseur sur la deuxième ligne
      lcd_1.print("Resultat: ");
      lcd_1.print("          "); // Efface les chiffres précédents
      lcd_1.setCursor(9, 1); // Positionne le curseur pour afficher le résultat
      lcd_1.print(result);
      delay(10000);
      lcd_1.setCursor(0, 1);
      lcd_1.print("Appuyer Bouton! ");
    }
  }
  else
  {
    // Vérifie si le bouton est pressé pour relancer le dé
    if (digitalRead(buttonPin) == LOW) // Si le bouton est pressé
    {
      delay(300); // Délai pour éviter les rebonds
      isAnimating = true; // Relance l'animation
      previousMillis = currentMillis; // Réinitialise le temps
      animationDuration = currentMillis + 5000; // Définit la durée de l'animation
    }
  }
}
