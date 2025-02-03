import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sv_ttk as sv
import webbrowser  # Module pour ouvrir des liens dans le navigateur

# Liste pour stocker les pseudos ajoutés
pseudos = []

# Fonction liée au bouton "Jouer"
def bouton_action_1():
    # Création de la fenêtre suivante (seconde page)
    fenetre_jeu = tk.Toplevel()  # Utilisation de Toplevel au lieu de Tk
    fenetre_jeu.title("Ajout de Pseudos")
    fenetre_jeu.geometry("500x500")  # Dimension de la fenêtre
    fenetre_jeu.configure(bg="#1c1c1c")  # Arrière-plan sombre

    # Fonction pour ajouter un pseudo dans la liste
    def ajouter_pseudo():
        pseudo = pseudo_entry.get()
        if pseudo:  # Si le pseudo n'est pas vide
            pseudos.append(pseudo)  # Ajouter le pseudo à la liste
            listbox_pseudos.insert(tk.END, pseudo)  # Ajouter le pseudo dans la listbox
            pseudo_entry.delete(0, tk.END)  # Effacer le champ de texte après ajout
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un pseudo.")

    # Titre de la nouvelle page
    titre_jeu = ttk.Label(fenetre_jeu, text="Ajoutez vos pseudos", font=("Arial", 18, "bold"), background="#1c1c1c", foreground="white")
    titre_jeu.pack(pady=20, fill=tk.X)

    # Champ de texte pour le pseudo
    pseudo_entry = ttk.Entry(fenetre_jeu, font=("Arial", 16))
    pseudo_entry.pack(pady=20, fill=tk.X, padx=20)

    # Bouton pour ajouter le pseudo
    btn_ajouter_pseudo = ttk.Button(fenetre_jeu, text="Ajouter Pseudo", command=ajouter_pseudo, style="Accent.TButton")
    btn_ajouter_pseudo.pack(pady=10, fill=tk.X, padx=20)

    # Listbox pour afficher les pseudos ajoutés
    listbox_pseudos = tk.Listbox(fenetre_jeu, font=("Arial", 14), height=5)
    listbox_pseudos.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)

    # Bouton pour quitter la page (retour à la page principale)
    btn_quitter_jeu = ttk.Button(fenetre_jeu, text="Retour à l'accueil", command=fenetre_jeu.destroy, style="Large.Accent.TButton")
    btn_quitter_jeu.pack(pady=20, fill=tk.X, padx=20)

def bouton_action_2():
    messagebox.showinfo("Quitter", "Action pour le bouton 2")

# Fonction pour ouvrir le lien MIT
def ouvrir_lien_mit():
    webbrowser.open("https://github.com/Exorcism0666/projet-emc/blob/main/LICENSE")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Jeu EMC")
fenetre.geometry("500x400")  # Taille de la fenêtre
fenetre.configure(bg="#1c1c1c")  # Assurer une couleur de fond cohérente

# Application du thème sv-ttk
sv.set_theme("dark")  # Appliquer le thème sombre

# Création du style personnalisé pour les boutons
style = ttk.Style()
style.configure("Large.Accent.TButton", padding=(20, 10), font=("Arial", 14))
style.map(
    "Large.Accent.TButton",
    foreground=[("pressed", "white"), ("active", "#E0E0E0")],
    background=[("pressed", "#444"), ("active", "#666")]
)

# Ajout d'un titre
titre = ttk.Label(fenetre, text="La démocratie han", font=("Arial", 18, "bold"), anchor="center", background="#1c1c1c", foreground="white")
titre.pack(pady=20, fill=tk.X)

# Création d'un cadre pour les boutons
cadre_boutons = ttk.Frame(fenetre)
cadre_boutons.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Ajout des boutons "Jouer" et "Quitter"
btn_1 = ttk.Button(cadre_boutons, text="Jouer", command=bouton_action_1, style="Large.Accent.TButton")
btn_1.pack(pady=15, fill=tk.X)

btn_2 = ttk.Button(cadre_boutons, text="Quitter", command=fenetre.destroy, style="Large.Accent.TButton")
btn_2.pack(pady=15, fill=tk.X)

# Mentions légales en bas à gauche
mention_license = ttk.Label(fenetre, text="Projet d'EMC sous licence ", font=("Arial", 8), background="#1c1c1c", foreground="white")
mention_license.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-30)

# Créer un label cliquable pour "MIT"
lien_mit = tk.Label(
    fenetre,
    text="MIT",
    fg="white",
    bg=fenetre["background"],  # Utiliser la couleur de fond de la fenêtre
    font=("Arial", 8, "underline"),
    cursor="hand2"
)
lien_mit.place(relx=0.0, rely=1.0, anchor="sw", x=134, y=-28)
lien_mit.bind("<Button-1>", lambda e: ouvrir_lien_mit())

# Mention des auteurs
mention_copyright = ttk.Label(
    fenetre,
    text="Copyright © Doisne Lilou, Dubus Yanis, Ryan Cordier, Alban Bloise",
    font=("Arial", 8),
    background="#1c1c1c",
    foreground="white"
)
mention_copyright.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

# Boucle principale de l'application
fenetre.mainloop()
