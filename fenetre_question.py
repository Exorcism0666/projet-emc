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
        {
        "q": "Qu’est-ce qu’une démocratie ? (Niveau 4e)", 
        "r": ["Un système politique où une seule personne détient tous les pouvoirs", "Un système où le pouvoir appartient à une famille royale", "Un système où les citoyens participent aux décisions politiques", "Un système où personne ne vote"], 
        "c": "Un système où les citoyens participent aux décisions politiques"
        },
        {
        "q": "Quel pays est souvent considéré comme le berceau de la démocratie ? (Niveau 4e)",
        "r": ["La France", "L’Italie", "La Grèce", "Les États-Unis"],
        "c": "La Grèce"
        },
        {
        "q": "Quelle est une des caractéristiques principales d’un régime démocratique ? (Niveau 3e)",
        "r": ["La censure de la presse", "L’arrestation des opposants politiques", "L’élection régulière des représentants", "L’obligation de voter pour un seul parti"],
        "c": "L’élection régulière des représentants"
        },
        {
        "q": "En France, qui peut voter aux élections présidentielles ? (Niveau 3e)",
        "r": ["Toute personne vivant en France", "Tout citoyen français majeur", "Uniquement les hommes", "Tous les Européens majeurs"],
        "c": "Tout citoyen français majeur"
        },
        {
        "q": "Quelle institution française veille au respect de la Constitution ? (Niveau 2de)",
        "r": ["Le Conseil économique, social et environnemental", "L’Assemblée nationale", "Le Conseil constitutionnel", "Le Sénat"],
        "c": "Le Conseil constitutionnel"
        },
        {
        "q": "Quel est le rôle principal du suffrage universel ? (Niveau 2de)",
        "r": ["Permettre aux citoyens de rédiger des lois", "Permettre au président de nommer les ministres", "Permettre aux citoyens d’élire leurs représentants", "Supprimer les droits des minorités"],
        "c": "Permettre aux citoyens d’élire leurs représentants"
        },
        {
        "q": "Que garantit la séparation des pouvoirs dans une démocratie ? (Niveau 1re)",
        "r": ["La concentration du pouvoir dans un seul organe", "L’indépendance entre les fonctions exécutives, législatives et judiciaires", "L’armée au pouvoir", "Le président qui cumule tous les pouvoirs"],
        "c": "L’indépendance entre les fonctions exécutives, législatives et judiciaires"
        },
        {
        "q": "Quel philosophe a développé l’idée de séparation des pouvoirs ? (Niveau 1re)",
        "r": ["Platon", "Rousseau", "Montesquieu", "Machiavel"],
        "c": "Montesquieu"
        },
        {
        "q": "Quelle affirmation correspond à une démocratie libérale ? (Niveau Terminale)",
        "r": ["Elle respecte les droits fondamentaux et organise des élections libres", "Elle interdit les partis politiques", "Elle impose une seule idéologie d'État", "Elle supprime les contre-pouvoirs"],
        "c": "Elle respecte les droits fondamentaux et organise des élections libres"
        },
        {
        "q": "Pourquoi peut-on dire que la démocratie est un régime perfectible ? (Niveau Terminale)",
        "r": ["Parce qu’elle ne fonctionne que dans les petits pays", "Parce qu’elle évolue et s’adapte aux sociétés et à leurs revendications", "Parce qu’elle garantit l’autorité absolue du chef d’État", "Parce qu’elle interdit toute critique du système"],
        "c": "Parce qu’elle évolue et s’adapte aux sociétés et à leurs revendications"
        }
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

    def afficher_intro_question():
        nonlocal joueur_actuel_index

        for widget in frame_reponses.winfo_children():
            widget.destroy()

        joueur = joueurs[joueur_actuel_index].strip()
        question_label.config(text=f"{joueur} : Appuie sur le dé avant de répondre à la question.")

        bouton_de = tk.Button(frame_reponses, text="🎲 Lancer le dé", font=("Arial", 12), command=afficher_question)
        bouton_de.pack(pady=20)

    def afficher_question():
        nonlocal index_question, joueur_actuel_index

        if index_question < len(questions):
            joueur = joueurs[joueur_actuel_index].strip()
            q = questions[index_question]
            question_label.config(text=f"{joueur} : {q['q']}")

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
        joueur_actuel_index = (joueur_actuel_index + 1) % nb_joueurs
        index_question += 1
        afficher_intro_question()  # Affiche l'annonce du prochain joueur

    # Commencer par la page d’introduction au lieu de la question directe :
    afficher_intro_question()


    def verifier_reponse(reponse):
        nonlocal index_question, joueur_actuel_index
        joueur = joueurs[joueur_actuel_index].strip()
        questions_posees[joueur] += 1
        if reponse == questions[index_question]["c"]:
            scores[joueur] += 1
            score_vars[joueur].set(scores[joueur])
        joueur_actuel_index = (joueur_actuel_index + 1) % nb_joueurs
        index_question += 1
        afficher_intro_question()


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

    tk.Button(frame_bas, text="Abandonner la parties", command=abandonner_partie).pack(side="right")
    afficher_intro_question()

