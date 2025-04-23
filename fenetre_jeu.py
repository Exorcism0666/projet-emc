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

import tkinter as tk
from tkinter import ttk
import sv_ttk

def afficher_reglement(fenetre_jeu):
    reglement_window = tk.Toplevel(fenetre_jeu)
    reglement_window.title("Règlement du jeu")
    reglement_window.geometry("600x400")
    reglement_window.configure(bg="#1c1c1c")
    reglement_window.resizable(False, False)
    sv_ttk.set_theme("dark")

    pages = [
        {
            "titre": "Objectif du jeu 🕮",
            "contenu": "Le but du jeu va être de répondre correctement aux questions posées par le programme, sachant qu'il y a un compte à rebours."
        },
        {
            "titre": "Déroulement ⏳",
            "contenu": "Chaque joueur, à tour de rôle, aura une question avec 4 choix différents. L'une d'entre elles sera bonne, les autres fausses. Si le joueur trouve la bonne réponse, il pourra alors lancer le dé et avancer."
        },
        {
            "titre": "Règles spéciales ✨",
            "contenu": "1. À définir selon les variantes du jeu.\n2. Par exemple : si un joueur répond 3 bonnes réponses d'affilée, il avance de 2 cases supplémentaires."
        }
    ]

    current_page = tk.IntVar(value=0)

    # Frame principale centrée
    main_frame = ttk.Frame(reglement_window)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Titre
    lbl_titre = ttk.Label(
        main_frame,
        font=("Arial", 16, "bold"),
        foreground="white",
        background="#1c1c1c",
        justify="center",
        wraplength=500
    )
    lbl_titre.pack(pady=(0, 10))

    # Contenu
    lbl_contenu = ttk.Label(
        main_frame,
        font=("Arial", 12),
        wraplength=500,
        foreground="white",
        background="#1c1c1c",
        justify="center"
    )
    lbl_contenu.pack(pady=(0, 20))

    # Contrôles de navigation
    controls_frame = ttk.Frame(main_frame)
    controls_frame.pack()

    btn_prev = ttk.Button(
        controls_frame,
        text="← Précédent",
        command=lambda: changer_page(-1)
    )
    btn_prev.pack(side="left", padx=10)

    btn_next = ttk.Button(
        controls_frame,
        text="Suivant →",
        command=lambda: changer_page(1)
    )
    btn_next.pack(side="right", padx=10)

    # Met à jour l'affichage de la page
    def afficher_page():
        index = current_page.get()
        page = pages[index]
        lbl_titre.config(text=page["titre"])
        lbl_contenu.config(text=page["contenu"])

        # Gère l'état des boutons
        btn_prev["state"] = "normal" if index > 0 else "disabled"
        btn_next["state"] = "normal" if index < len(pages) - 1 else "disabled"

    # Change la page (avance ou recule)
    def changer_page(delta):
        new_index = current_page.get() + delta
        if 0 <= new_index < len(pages):
            current_page.set(new_index)
            afficher_page()

    afficher_page()

    def update_page(*args):
        page_index = current_page.get()
        btn_prev.state(["!disabled" if page_index > 0 else "disabled"])

        if page_index >= len(pages) - 1:
            btn_next.config(text="Commencer !")
            btn_next.config(command=reglement_window.destroy)
        else:
            btn_next.config(text="Suivant →")
            btn_next.config(command=lambda: current_page.set(current_page.get() + 1))

        lbl_titre.config(text=pages[page_index]["titre"])
        lbl_contenu.config(text=pages[page_index]["contenu"])

    current_page.trace_add("write", update_page)
    update_page()

    # Centrer la fenêtre
    reglement_window.update_idletasks()
    width = reglement_window.winfo_width()
    height = reglement_window.winfo_height()
    x = (reglement_window.winfo_screenwidth() // 2) - (width // 2)
    y = (reglement_window.winfo_screenheight() // 2) - (height // 2)
    reglement_window.geometry(f"+{x}+{y}")

    reglement_window.grab_set()

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
    pseudo_entry.bind("<Return>", lambda event: ajouter_pseudo(pseudo_entry, listbox_pseudos))
    ttk.Label(fenetre_jeu, text="(limite de 16 caractères)", font=("Arial", 10, "italic"), background="#1c1c1c", foreground="white").pack(pady=10)

    listbox_pseudos = tk.Listbox(fenetre_jeu, font=("Courier", 14), height=4, width=20, justify="center")
    listbox_pseudos.pack(pady=10)

    ttk.Button(fenetre_jeu, text="Ajouter un pseudo", style="Accent.TButton", command=lambda: ajouter_pseudo(pseudo_entry, listbox_pseudos)).pack(pady=10)
    ttk.Button(fenetre_jeu, text="Supprimer un pseudo", style="Accent.TButton", command=lambda: supprimer_pseudo(listbox_pseudos)).pack(pady=10)

    # Bouton "Commencer la partie"
    btn_commencer = ttk.Button(
        fenetre_jeu,
        text="Commencer la partie",
        style="Green.TButton",
        command=lambda: afficher_reglement(fenetre_jeu) if pseudos else afficher_message_bloquant("Erreur", "Ajoutez au moins un joueur !")
    )
    btn_commencer.pack(pady=10)

    # Bouton "Retour à l'accueil"
    btn_retour = ttk.Button(fenetre_jeu, text="Retour à l'accueil", command=retour_accueil)
    btn_retour.pack(pady=10)

    # Centrer la fenêtre
    fenetre_jeu.update_idletasks()
    width = fenetre_jeu.winfo_width()
    height = fenetre_jeu.winfo_height()
    x = (fenetre_jeu.winfo_screenwidth() // 2) - (width // 2)
    y = (fenetre_jeu.winfo_screenheight() // 2) - (height // 2)
    fenetre_jeu.geometry(f"+{x}+{y}")
