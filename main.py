import tkinter as tk
from tkinter import ttk
import sv_ttk as sv
from fenetre_jeu import ouvrir_fenetre_jeu
from utils import effet_fondu, afficher_texte, ouvrir_lien_mit, afficher_message_bloquant
from constants import BACKGROUND_COLOR, FOREGROUND_COLOR, TITRE, DESCRIPTION
from styles import configurer_styles

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Jeu EMC")
centrage_de_fenetre(fenetre, 500, 400)
fenetre.configure(bg=BACKGROUND_COLOR)
fenetre.resizable(False, False)
sv.set_theme("dark")

# Configuration des styles
configurer_styles()

# Effet de fondu pour le titre
titre = ttk.Label(
    fenetre,
    text=TITRE,
    justify="center",
    font=("Arial", 18, "bold"),
    background=BACKGROUND_COLOR,
    foreground=FOREGROUND_COLOR
)
titre.pack(pady=20)
effet_fondu(titre)

# Affichage progressif du texte d'introduction
texte_intro = ttk.Label(
    fenetre,
    text="",
    font=("Arial", 10, "bold"),
    background=BACKGROUND_COLOR,
    foreground=FOREGROUND_COLOR
)
texte_intro.pack(pady=6)
afficher_texte(texte_intro, DESCRIPTION)

# Cadre pour les boutons
cadre_boutons = ttk.Frame(fenetre)
cadre_boutons.place(relx=0.5, rely=0.55, anchor="center")

# Bouton "Jouer"
btn_jouer = ttk.Button(
    cadre_boutons,
    style="Large.Accent.TButton",
    text="Jouer",
    command=lambda: ouvrir_fenetre_jeu(fenetre)
)
# Bouton "Quitter"
btn_quitter = ttk.Button(
    cadre_boutons,
    style="Large.Accent.TButton",
    text="Quitter",
    command=fenetre.destroy
)

# Affichage des boutons après un délai
fenetre.after(1500, lambda: (btn_jouer.pack(pady=15), btn_quitter.pack(pady=15)))

# Mentions légales
mention_license = ttk.Label(
    fenetre,
    text="Projet d'EMC sous licence ",
    font=("Arial", 8),
    background=BACKGROUND_COLOR,
    foreground=FOREGROUND_COLOR
)
mention_license.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-30)

# Lien vers la licence MIT
lien_mit = tk.Label(
    fenetre,
    text="MIT",
    fg=FOREGROUND_COLOR,
    bg=BACKGROUND_COLOR,
    font=("Arial", 8, "underline"),
    cursor="hand2"
)
lien_mit.place(relx=0.0, rely=1.0, anchor="sw", x=134, y=-28)
lien_mit.bind("<Button-1>", lambda e: ouvrir_lien_mit())

# Mention de copyright
mention_copyright = ttk.Label(
    fenetre,
    text="Copyright © Doisne Lilou, Dubus Yanis, Cordier Ryan, Bloise Alban",
    font=("Arial", 8),
    background=BACKGROUND_COLOR,
    foreground=FOREGROUND_COLOR
)
mention_copyright.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

# Lancement de la boucle principale
fenetre.mainloop()
