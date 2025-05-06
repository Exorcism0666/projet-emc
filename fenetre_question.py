import tkinter as tk
from tkinter import ttk
import sv_ttk as sv
from tkinter import messagebox
from liste_question import questions
import random
from utils import centrage_de_fenetre

def lancer_fenetre_question(pseudos):
    fenetre = tk.Toplevel()
    fenetre.title("Jeu EMC")
    centrage_de_fenetre(fenetre, 1200, 400)
    fenetre.configure(bg="#1c1c1c")
    fenetre.resizable(False, False)
    sv.set_theme("dark")

    def on_closing():
        pass

    fenetre.protocol("WM_DELETE_WINDOW", on_closing)

    index_question = 0
    joueurs = pseudos
    nb_joueurs = len(joueurs)
    scores = {joueur.strip(): 0 for joueur in joueurs}
    score_vars = {joueur.strip(): tk.IntVar(value=0) for joueur in joueurs}
    questions_posees = {joueur.strip(): 0 for joueur in joueurs}
    joueur_actuel_index = 0

    # Timer variables
    timer_id = None
    temps_restant = 20

    # Couleurs fixes selon l'ordre
    couleurs_fixes = ["#FF3B30", "#007AFF", "#FFD60A", "#34C759"]
    couleurs_joueurs = {}
    for i, joueur in enumerate(joueurs):
        couleurs_joueurs[joueur.strip()] = couleurs_fixes[i % len(couleurs_fixes)]
    random.shuffle(questions)

    # Scoreboard
    frame_scoreboard = tk.Frame(fenetre, bg="#2b2b2b", width=200)
    frame_scoreboard.pack(side="left", fill="y")

    tk.Label(frame_scoreboard, text="Scores", font=("Arial", 14, "bold"), bg="#2b2b2b", fg="white").pack(pady=10)

    label_scoreboard = {}

    for joueur in joueurs:
        pseudo = joueur.strip()
        couleur = couleurs_joueurs[pseudo]
        line = tk.Frame(frame_scoreboard, bg="#2b2b2b")
        line.pack(anchor="w", padx=10, pady=5)
        label = tk.Label(line, text=pseudo, font=("Arial", 11), bg="#2b2b2b", fg=couleur)
        label.pack(side="left")
        tk.Label(line, textvariable=score_vars[pseudo], font=("Arial", 11), bg="#2b2b2b", fg="white").pack(side="right")
        label_scoreboard[pseudo] = label

    # Zone centrale
    main_frame = tk.Frame(fenetre, bg="#1c1c1c")
    main_frame.pack(fill="both", expand=True)

    # Timer label
    label_timer = tk.Label(main_frame, text="", font=("Arial", 14, "bold"), bg="#1c1c1c", fg="white", justify="center")
    label_timer.pack(pady=(10, 0))

    pseudo_label = tk.Label(main_frame, text="", font=("Arial", 18, "bold"), bg="#1c1c1c", fg="white", justify="center")
    pseudo_label.pack(pady=(10, 5))

    question_label = tk.Label(main_frame, text="", font=("Arial", 14), bg="#1c1c1c", fg="white", wraplength=600, justify="center")
    question_label.pack(pady=5)

    frame_reponses = tk.Frame(main_frame, bg="#1c1c1c")
    frame_reponses.pack()

    frame_bas = tk.Frame(main_frame, bg="#1c1c1c")
    frame_bas.pack(side="bottom", fill="x", padx=10, pady=10)

    def mettre_a_jour_scoreboard():
        for joueur in joueurs:
            pseudo = joueur.strip()
            couleur = couleurs_joueurs[pseudo]
            if pseudo == joueurs[joueur_actuel_index].strip():
                label_scoreboard[pseudo].config(font=("Arial", 12, "bold"), fg=couleur)
            else:
                label_scoreboard[pseudo].config(font=("Arial", 11), fg=couleur)

    def passer_joueur_suivant():
        nonlocal joueur_actuel_index, index_question, timer_id
        if timer_id:
            fenetre.after_cancel(timer_id)
        joueur_actuel_index = (joueur_actuel_index + 1) % nb_joueurs
        index_question += 1
        afficher_intro_question()

    def lancer_timer():
        nonlocal temps_restant, timer_id
        if temps_restant > 0:
            label_timer.config(text=f"⏱️ Temps restant : {temps_restant} s", fg="white")
            temps_restant -= 1
            timer_id = fenetre.after(1000, lancer_timer)
        else:
            label_timer.config(text="⏰ TEMPS IMPARTI", font=("Arial", 28, "bold"), fg="red")
            for widget in frame_reponses.winfo_children():
                widget.destroy()
            question_label.config(text="")
            fenetre.after(3000, passer_joueur_suivant)

    def afficher_intro_question():
        nonlocal joueur_actuel_index
        for widget in frame_reponses.winfo_children():
            widget.destroy()
        joueur = joueurs[joueur_actuel_index].strip()
        couleur = couleurs_joueurs[joueur]
        mettre_a_jour_scoreboard()

        pseudo_label.config(text=joueur, fg=couleur)
        label_timer.config(text="")
        question_label.config(
            text="Appuie sur le dé avant de répondre à la question.",
            fg="white"
        )

        bouton_de = ttk.Button(frame_reponses, text="🎲 Lancer le dé", command=afficher_question, style="Accent.TButton")
        bouton_de.pack(pady=20)

    def afficher_question():
        nonlocal index_question, joueur_actuel_index, temps_restant, timer_id
        if timer_id:
            fenetre.after_cancel(timer_id)
        temps_restant = 20

        if index_question < len(questions):
            joueur = joueurs[joueur_actuel_index].strip()
            couleur = couleurs_joueurs[joueur]
            mettre_a_jour_scoreboard()
            q = questions[index_question]

            pseudo_label.config(text=joueur, fg=couleur)
            question_label.config(text=q["q"], fg="white")

            for widget in frame_reponses.winfo_children():
                widget.destroy()
            reponses_melangees = q["r"][:]
            random.shuffle(reponses_melangees)
            for r in reponses_melangees:
                ttk.Button(frame_reponses, style="Accent.TButton", text=r, command=lambda rep=r: verifier_reponse(rep)).pack(pady=5, fill="x")

            lancer_timer()
        else:
            afficher_classement()

    def verifier_reponse(reponse):
        nonlocal index_question, joueur_actuel_index, timer_id
        if timer_id:
            fenetre.after_cancel(timer_id)

        joueur = joueurs[joueur_actuel_index].strip()
        questions_posees[joueur] += 1
        if reponse == questions[index_question]["c"]:
            scores[joueur] += 1
            score_vars[joueur].set(scores[joueur])
        joueur_actuel_index = (joueur_actuel_index + 1) % nb_joueurs
        index_question += 1
        afficher_intro_question()

    def afficher_classement():
        pseudo_label.config(text="")
        label_timer.config(text="")
        question_label.config(text="Le quiz est terminé ! 🎉", fg="white")
        for widget in frame_reponses.winfo_children():
            widget.destroy()

        classement = []
        for joueur in joueurs:
            j = joueur.strip()
            score = scores[j]
            total = questions_posees[j]
            pourcentage = (score / total) * 100 if total else 0
            classement.append((j, score, total, pourcentage))

        classement.sort(key=lambda x: x[3], reverse=True)

        for nom, pts, total_q, pct in classement:
            couleur = couleurs_joueurs[nom]
            tk.Label(frame_reponses, text=f"{nom} : {pts}/{total_q} ({pct:.1f}%)", font=("Arial", 12), bg="#1c1c1c", fg=couleur).pack()

        tk.Label(frame_reponses, text="Vous pouvez fermer la fenêtre.", font=("Arial", 10), bg="#1c1c1c", fg="gray").pack()
        ttk.Button(frame_reponses, text="Terminer la partie", style="Accent.TButton", command=fenetre.destroy).pack(pady=10)

    def abandonner_partie():
        def confirmer_abandon():
            fenetre.destroy()

        confirmation = tk.Toplevel(fenetre)
        confirmation.title("Confirmer l'abandon")
        centrage_de_fenetre(confirmation, 1200, 400)
        confirmation.configure(bg="#1c1c1c")
        confirmation.resizable(False, False)
        sv.set_theme("dark")
        confirmation.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(confirmation, text="Êtes-vous certain de vouloir abandonner la partie ?\nVotre progression ne sera pas conservé", font=("Arial", 20), bg="#1c1c1c", fg="red", wraplength=500).pack(pady=20)

        bouton_frame = tk.Frame(confirmation, bg="#1c1c1c")
        bouton_frame.pack(pady=10)

        ttk.Button(bouton_frame, text="Revenir au jeu", command=confirmation.destroy, style="Accent.TButton").pack(side="left", padx=30)
        ttk.Button(bouton_frame, text="Abandonner", command=confirmer_abandon, style="TButton").pack(side="left", padx=30)
        confirmation.grab_set()
        confirmation.focus_force()
        confirmation.wait_window()
        parent=lancer_fenetre_question


    ttk.Button(frame_bas, text="Abandonner la partie", command=abandonner_partie, style="TButton").pack(side="right")
    afficher_intro_question()

