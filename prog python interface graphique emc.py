import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sv_ttk
import webbrowser  # Module pour ouvrir des liens dans le navigateur
import pyglet, os # Pour la police d'écriture

pyglet.font.add_file('undertale.ttf')  # Your TTF file name here

# Fonction liée aux boutons
def bouton_action_1():
    messagebox.showinfo("Bouton 1", "Action pour le bouton 1")

def bouton_action_2():
    messagebox.showinfo("Bouton 2", "Action pour le bouton 2")

# Fonction pour ouvrir le lien MIT
def ouvrir_lien_mit():
    webbrowser.open("https://github.com/Exorcism0666/projet-emc/blob/main/LICENSE")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Jeu emc")
fenetre.geometry("500x400")  # Taille de la fenêtre

# Application du thème sv-ttk
sv_ttk.set_theme("dark")  # Vous pouvez changer en "light" pour un thème clair

# Création du style personnalisé pour les boutons
style = ttk.Style()
style.configure("Large.Accent.TButton", padding=(20, 10), font=("undertale", 14), background="#007BFF", foreground="black")
style.map(
    "Large.Blue.TButton",
    background=[("active", "#0056b3"), ("pressed", "#004494")]
)

# Style pour le texte en bas à gauche
style.configure("Small.White.TLabel", foreground="white", font=("Arial", 8))  # Texte plus petit

# Ajout d'un titre
titre = ttk.Label(fenetre, text="La démocratie han", font=("undertale", 18, "bold"), anchor="center")
titre.pack(pady=20)  # Espacement au-dessus et au-dessous du titre

# Création d'un cadre pour les boutons
cadre_boutons = ttk.Frame(fenetre)  # Utilisation de ttk pour compatibilité avec sv-ttk
cadre_boutons.place(relx=0.5, rely=0.5, anchor="center")  # Centrer le cadre

# Ajout des boutons au cadre avec le style "Large.Accent.TButton"
btn_1 = ttk.Button(cadre_boutons, text="Bouton 1", command=bouton_action_1, style="Large.Accent.TButton")
btn_1.pack(pady=15)  # Espacement vertical

btn_2 = ttk.Button(cadre_boutons, text="Bouton 2", command=bouton_action_2, style="Large.Accent.TButton")
btn_2.pack(pady=15)

# Mentions légales en bas à gauche
mention_license = ttk.Label(
    fenetre,
    text="Projet d'EMC sous licence ",
    style="Small.White.TLabel"
)
mention_license.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-30)  # Positionnement en bas à gauche

# Créer un label cliquable pour "MIT"
lien_mit = tk.Label(
    fenetre,
    text="MIT",
    fg="white",  # Couleur du texte
    bg="#1c1c1c",  # Couleur de fond (ajustez-la pour correspondre au thème sombre)
    font=("Arial", 8, "underline"),  # Police soulignée pour indiquer un lien
    cursor="hand2"  # Curseur en forme de main pour indiquer un lien cliquable
)
# Positionnement précis pour aligner "MIT" avec la phrase
lien_mit.place(relx=0.0, rely=1.0, anchor="sw", x=134, y=-28)  # Ajustez la valeur de x pour aligner correctement
lien_mit.bind("<Button-1>", lambda e: ouvrir_lien_mit())  # Lier le clic à la fonction

mention_copyright = ttk.Label(
    fenetre,
    text="Copyright © Doisne Lilou, Dubus Yanis, Ryan Cordier, Alban Bloise",  # Remplacez par les prénoms
    style="Small.White.TLabel"
)
mention_copyright.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

# Boucle principale de l'application
fenetre.mainloop()
