import tkinter as tk
from tkinter import ttk
import sv_ttk as sv
from utils import afficher_message_bloquant

# Liste pour stocker les pseudos
pseudos = []

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

def supprimer_pseudo(listbox_pseudos):
    selection = listbox_pseudos.curselection()
    if selection:
        index = selection[0]
        listbox_pseudos.delete(index)
        pseudos.pop(index)
    else:
        afficher_message_bloquant("Erreur", "Veuillez sélectionner un pseudo à supprimer.")

def ouvrir_fenetre_jeu(fenetre_principale):
    fenetre_principale.withdraw()
    fenetre_jeu = tk.Toplevel(fenetre_principale)
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
        fenetre_principale.deiconify()

    def on_close():
        fenetre_principale.deiconify()
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

    listbox_pseudos = tk.Listbox(fenetre_jeu, font=("Courier", 14), height=4, width=20, justify="center")
    listbox_pseudos.pack(pady=10)

    ttk.Button(fenetre_jeu, text="Ajouter un pseudo", style="Accent.TButton", command=lambda: ajouter_pseudo(pseudo_entry, listbox_pseudos)).pack(pady=10)
    ttk.Button(fenetre_jeu, text="Supprimer un pseudo", style="Accent.TButton", command=lambda: supprimer_pseudo(listbox_pseudos)).pack(pady=10)

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