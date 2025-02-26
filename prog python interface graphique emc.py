import tkinter as tk
from tkinter import messagebox, ttk
import sv_ttk as sv
import webbrowser

# Liste pour stocker les pseudos
pseudos = []

# Fonction pour ouvrir un lien
def ouvrir_lien_mit():
    webbrowser.open("https://github.com/Exorcism0666/projet-emc/blob/main/LICENSE")

# Fonction pour afficher un message bloquant
def afficher_message_bloquant(titre, message):
    popup = tk.Toplevel(fenetre)
    popup.title(titre)
    popup.configure(bg="#1c1c1c")
    popup.resizable(False, False)
    popup.grab_set()

    label = ttk.Label(popup, text=message, font=("Arial", 12), background="#1c1c1c", foreground="white", wraplength=280)
    label.pack(pady=20, padx=20)
    ttk.Button(popup, text="OK", command=popup.destroy).pack()

    popup.update_idletasks()
    largeur = popup.winfo_width()
    hauteur = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (largeur // 2)
    y = (popup.winfo_screenheight() // 2) - (hauteur // 2)
    popup.geometry(f"{largeur}x{hauteur}+{x}+{y}")

# Fonction pour ajouter un pseudo
def ajouter_pseudo(pseudo_entry, listbox_pseudos):
    if len(pseudos) >= 4:
        afficher_message_bloquant("Erreur", "Vous ne pouvez pas ajouter plus de 4 pseudos.")
        return
    pseudo = pseudo_entry.get()
    if pseudo:
        pseudo = pseudo.center(20)  # Formatage pour 20 caractères centrés
        if pseudo in pseudos:
            afficher_message_bloquant("Erreur", "Ce pseudonyme est déjà utilisé par un autre joueur.")
            return
        pseudos.append(pseudo)
        listbox_pseudos.insert(tk.END, pseudo)
        pseudo_entry.delete(0, tk.END)
    else:
        afficher_message_bloquant("Erreur", "Veuillez entrer un pseudo.")

# Fonction pour supprimer un pseudo
def supprimer_pseudo():
    selection = listbox_pseudos.curselection()
    if selection:
        index = selection[0]
        listbox_pseudos.delete(index)
        pseudos.pop(index)
    else:
        afficher_message_bloquant("Erreur", "Veuillez sélectionner un pseudo à supprimer.")

# Fonction pour afficher la fenêtre de jeu
def ouvrir_fenetre_jeu():
    fenetre.withdraw()
    fenetre_jeu = tk.Toplevel(fenetre)
    fenetre_jeu.title("Inscriptions des joueurs")
    fenetre_jeu.geometry("400x550")
    fenetre_jeu.configure(bg="#1c1c1c")
    fenetre_jeu.resizable(False, False)
    sv.set_theme("dark")

    # Configuration du style vert
    style = ttk.Style()
    style.configure("Green.TButton",
                    background="#4CAF50",  # Couleur verte
                    foreground="white",   # Texte blanc
                    font=("Arial", 14),  # Police
                    padding=(20, 10))    # Padding

    def retour_accueil():
        fenetre_jeu.destroy()
        fenetre.deiconify()
        effet_fondu(0)

    def on_close():
        fenetre.deiconify()
        effet_fondu(0)
        fenetre_jeu.destroy()

    fenetre_jeu.protocol("WM_DELETE_WINDOW", on_close)

    ttk.Label(fenetre_jeu, text="Inscriptions des joueurs!", font=("Arial", 18, "bold"), background="#1c1c1c", foreground="white").pack(pady=10)
    ttk.Label(fenetre_jeu, text="Limite de 4 joueurs !", font=("Arial", 10, "bold italic"), background="#1c1c1c", foreground="white").pack(pady=20)

    # Fonction de validation pour limiter les caractères à 16
    def valider_texte(P):
        return len(P) <= 16

    validate_command = fenetre_jeu.register(valider_texte)

    pseudo_entry = ttk.Entry(fenetre_jeu, font=("Arial", 16), validate="key", validatecommand=(validate_command, "%P"), justify="center")
    pseudo_entry.pack(pady=3)
    ttk.Label(fenetre_jeu, text="(limite de 16 caractères)", font=("Arial", 10, "italic"), background="#1c1c1c", foreground="white").pack(pady=10)

    global listbox_pseudos
    listbox_pseudos = tk.Listbox(fenetre_jeu, font=("Courier", 14), height=4, width=20, justify="center")
    listbox_pseudos.pack(pady=10)

    ttk.Button(fenetre_jeu, text="Ajouter un pseudo", style="Accent.TButton", command=lambda: ajouter_pseudo(pseudo_entry, listbox_pseudos)).pack(pady=10)
    ttk.Button(fenetre_jeu, text="Supprimer un pseudo", style="Accent.TButton", command=supprimer_pseudo).pack(pady=10)

    # Bouton "Commencer la partie"
    btn_commencer = ttk.Button(
        fenetre_jeu,
        text="Commencer la partie",
        style="Green.TButton"
    )
    btn_commencer.pack(pady=10)

    # Bouton "Retour à l'accueil"
    btn_retour = ttk.Button(fenetre_jeu, text="Retour à l'accueil", command=retour_accueil)
    btn_retour.pack(pady=10)

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Jeu EMC")
fenetre.geometry("500x400")
fenetre.configure(bg="#1c1c1c")
fenetre.resizable(False, False)
sv.set_theme("dark")

style = ttk.Style()
style.configure("Large.Accent.TButton", padding=(20, 10), font=("Arial", 14))

# Effet de fondu pour le titre
def effet_fondu(opacity=0):
    if opacity <= 1.0:
        couleur = f"#{int(opacity * 255):02x}{int(opacity * 255):02x}{int(opacity * 255):02x}"
        titre.config(foreground=couleur)
        fenetre.after(50, effet_fondu, opacity + 0.05)

description = "Un jeu où la démocratie règne… enfin, jusqu'à ce que quelqu’un triche !"
def afficher_texte(index=0):
    if index < len(description):
        texte_intro.config(text=description[:index+1])
        fenetre.after(50, afficher_texte, index+1)

titre = ttk.Label(fenetre, text="🎭 DémocraTroll\nÀ vous de jouer (ou de manipuler !)", justify="center", font=("Arial", 18, "bold"), background="#1c1c1c", foreground="white")
titre.pack(pady=20)
effet_fondu()

texte_intro = ttk.Label(fenetre, text="", font=("Arial", 10, "bold"), background="#1c1c1c", foreground="white")
texte_intro.pack(pady=6)
afficher_texte()

cadre_boutons = ttk.Frame(fenetre)
cadre_boutons.place(relx=0.5, rely=0.55, anchor="center")

btn_jouer = ttk.Button(cadre_boutons, style="Large.Accent.TButton", text="Jouer", command=ouvrir_fenetre_jeu)
btn_quitter = ttk.Button(cadre_boutons, style="Large.Accent.TButton", text="Quitter", command=fenetre.destroy)
fenetre.after(1500, lambda: (btn_jouer.pack(pady=15), btn_quitter.pack(pady=15)))

# Mentions légales
mention_license = ttk.Label(fenetre, text="Projet d'EMC sous licence ", font=("Arial", 8), background="#1c1c1c", foreground="white")
mention_license.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-30)

lien_mit = tk.Label(fenetre, text="MIT", fg="white", bg="#1c1c1c", font=("Arial", 8, "underline"), cursor="hand2")
lien_mit.place(relx=0.0, rely=1.0, anchor="sw", x=134, y=-28)
lien_mit.bind("<Button-1>", lambda e: ouvrir_lien_mit())

mention_copyright = ttk.Label(fenetre, text="Copyright © Doisne Lilou, Dubus Yanis, Ryan Cordier, Alban Bloise", font=("Arial", 8), background="#1c1c1c", foreground="white")
mention_copyright.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

fenetre.mainloop()
