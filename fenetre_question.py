import tkinter as tk
from tkinter import ttk
import sv_ttk as sv
from tkinter import messagebox


def lancer_fenetre_question(pseudos):
    # Fenêtre principale
    fenetre = tk.Toplevel()
    fenetre.title("Jeu EMC")
    fenetre.geometry("800x400")
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

    # Questions
    questions = [
        {"q": "Capitale de la France ?", "r": ["Paris", "Londres", "Berlin", "Madrid"], "c": "Paris"},
        {"q": "7 x 8 ?", "r": ["54", "56", "49", "63"], "c": "56"},
        {"q": "Peintre de la Joconde ?", "r": ["Van Gogh", "Monet", "Léonard de Vinci", "Picasso"], "c": "Léonard de Vinci"},
        {"q": "Symbole chimique de l'eau ?", "r": ["O2", "H2O", "CO2", "NaCl"], "c": "H2O"},
    ]

    # Scoreboard à gauche
    frame_scoreboard = tk.Frame(fenetre, bg="#2b2b2b", width=160)
    frame_scoreboard.pack(side="left", fill="y")

    tk.Label(frame_scoreboard, text="Scores", font=("Arial", 14, "bold"), bg="#2b2b2b", fg="white").pack(pady=10)
    for joueur in joueurs:
        pseudo = joueur.strip()
        line = tk.Frame(frame_scoreboard, bg="#2b2b2b")
        line.pack(anchor="w", padx=10, pady=5)
        tk.Label(line, text=pseudo, font=("Arial", 11), bg="#2b2b2b", fg="white").pack(side="left")
        tk.Label(line, textvariable=score_vars[pseudo], font=("Arial", 11), bg="#2b2b2b", fg="white").pack(side="right")

    # Zone centrale
    main_frame = tk.Frame(fenetre, bg="#1c1c1c")
    main_frame.pack(fill="both", expand=True)

    question_label = tk.Label(main_frame, text="", font=("Arial", 14), bg="#1c1c1c", fg="white")
    question_label.pack(pady=20)

    score_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="#1c1c1c", fg="white")
    score_label.pack()

    frame_reponses = tk.Frame(main_frame, bg="#1c1c1c")
    frame_reponses.pack()

    frame_bas = tk.Frame(main_frame, bg="#1c1c1c")
    frame_bas.pack(side="bottom", fill="x", padx=10, pady=10)

    def afficher_question():
        nonlocal index_question, joueur_actuel_index
        if index_question < len(questions):
            joueur = joueurs[joueur_actuel_index].strip()
            q = questions[index_question]
            question_label.config(text=f"{joueur}, à vous de jouer !\n\n{q['q']}")

            for widget in frame_reponses.winfo_children():
                widget.destroy()

            for r in q["r"]:
                tk.Button(frame_reponses, text=r, font=("Arial", 12), command=lambda rep=r: verifier_reponse(rep)).pack(pady=5, fill="x")
        else:
            afficher_classement()

    def verifier_reponse(reponse):
        nonlocal index_question, joueur_actuel_index
        joueur = joueurs[joueur_actuel_index].strip()
        questions_posees[joueur] += 1
        if reponse == questions[index_question]["c"]:
            scores[joueur] += 1
            score_vars[joueur].set(scores[joueur])
        joueur_actuel_index = (joueur_actuel_index + 1) % nb_joueurs
        index_question += 1
        afficher_question()

    def afficher_classement():
        question_label.config(text="Le quiz est terminé ! 🎉")
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
            tk.Label(frame_reponses, text=f"{nom} : {pts}/{total_q} ({pct:.1f}%)", font=("Arial", 12), bg="#1c1c1c", fg="white").pack()

        tk.Label(frame_reponses, text="Vous pouvez fermer la fenêtre.", font=("Arial", 10), bg="#1c1c1c", fg="gray").pack()
        tk.Button(frame_reponses, text="Terminer la partie", font=("Arial", 11), command=fenetre.destroy).pack(pady=10)

    def abandonner_partie():
        def confirmer_abandon():
            fenetre.destroy()

        confirmation = tk.Toplevel(fenetre)
        confirmation.title("Confirmer l'abandon")
        confirmation.geometry("400x200")
        confirmation.configure(bg="#1c1c1c")
        confirmation.resizable(False, False)
        sv.set_theme("dark")
        confirmation.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(confirmation, text="Êtes-vous certain de vouloir abandonner la partie ?\nVotre score sera de 0 et vous devrez reprendre de 0.", font=("Arial", 11), bg="#1c1c1c", fg="white", wraplength=380).pack(pady=20)

        bouton_frame = tk.Frame(confirmation, bg="#1c1c1c")
        bouton_frame.pack(pady=10)

        tk.Button(bouton_frame, text="Revenir au jeu", command=confirmation.destroy).pack(side="left", padx=10)
        tk.Button(bouton_frame, text="Abandonner", command=confirmer_abandon).pack(side="left", padx=10)

    tk.Button(frame_bas, text="Abandonner la partie", command=abandonner_partie).pack(side="right")
    afficher_question()
