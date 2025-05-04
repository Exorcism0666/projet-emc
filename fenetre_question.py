import tkinter as tk
from tkinter import ttk
import sv_ttk as sv
from tkinter import messagebox
import random


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
    questions = questions = [
  {
    "q": "Quel est le principe fondamental d'une démocratie représentative ?",
    "r": [
      "Les citoyens élisent des représentants pour prendre les décisions en leur nom",
      "Le pouvoir est exercé directement par le peuple sans intermédiaire",
      "Les décisions sont prises par les militaires",
      "Les lois sont imposées par une religion d'État"
    ],
    "c": "Les citoyens élisent des représentants pour prendre les décisions en leur nom"
  },
  {
    "q": "Quelle est la principale différence entre démocratie directe et démocratie représentative ?",
    "r": [
      "La démocratie directe implique une participation directe des citoyens aux décisions",
      "La démocratie représentative n’a pas de Constitution",
      "La démocratie directe repose sur le pouvoir militaire",
      "La démocratie représentative supprime les élections"
    ],
    "c": "La démocratie directe implique une participation directe des citoyens aux décisions"
  },
  {
    "q": "Quel texte fondateur français affirme les principes de la démocratie ?",
    "r": [
      "La Déclaration des droits de l'homme et du citoyen de 1789",
      "Le Code Napoléon",
      "La loi sur la laïcité de 1905",
      "Le traité de Versailles"
    ],
    "c": "La Déclaration des droits de l'homme et du citoyen de 1789"
  },
  {
    "q": "Dans une démocratie, quel est le rôle des partis politiques ?",
    "r": [
      "Organiser la représentation des opinions dans les institutions",
      "Imposer une seule idéologie à tous les citoyens",
      "Contrôler les médias publics",
      "Nommer les juges constitutionnels"
    ],
    "c": "Organiser la représentation des opinions dans les institutions"
  },
  {
    "q": "Qu’est-ce qu’un référendum ?",
    "r": [
      "Un vote par lequel les citoyens approuvent ou rejettent directement une proposition",
      "Un discours présidentiel exceptionnel",
      "Un rapport secret du Parlement",
      "Une conférence de presse du gouvernement"
    ],
    "c": "Un vote par lequel les citoyens approuvent ou rejettent directement une proposition"
  },
  {
    "q": "Qu’est-ce qu’une démocratie ? (Niveau 4e)",
    "r": [
      "Un système où les citoyens participent aux décisions politiques",
      "Un régime où le pouvoir est détenu par une seule personne",
      "Un régime basé sur l’hérédité du pouvoir",
      "Un système où seuls les riches votent"
    ],
    "c": "Un système où les citoyens participent aux décisions politiques"
  },
  {
    "q": "Quel pays est souvent considéré comme le berceau de la démocratie ? (Niveau 4e)",
    "r": [
      "La Grèce",
      "La Rome antique",
      "Les États-Unis",
      "L’Angleterre médiévale"
    ],
    "c": "La Grèce"
  },
  {
    "q": "Quelle est une caractéristique essentielle d’un régime démocratique ? (Niveau 3e)",
    "r": [
      "L’élection régulière des représentants",
      "La centralisation absolue des pouvoirs",
      "Le pouvoir militaire prioritaire",
      "La censure des médias"
    ],
    "c": "L’élection régulière des représentants"
  },
  {
    "q": "Qui peut voter aux élections présidentielles en France ? (Niveau 3e)",
    "r": [
      "Tout citoyen français majeur",
      "Toute personne résidant en France depuis 5 ans",
      "Tout citoyen européen résidant en France",
      "Uniquement les fonctionnaires"
    ],
    "c": "Tout citoyen français majeur"
  },
  {
    "q": "Quelle institution française veille au respect de la Constitution ? (Niveau 2de)",
    "r": [
      "Le Conseil constitutionnel",
      "Le Sénat",
      "Le Conseil d’État",
      "L’Assemblée nationale"
    ],
    "c": "Le Conseil constitutionnel"
  },
  {
    "q": "Quel est le rôle principal du suffrage universel ? (Niveau 2de)",
    "r": [
      "Permettre aux citoyens d’élire leurs représentants",
      "Permettre aux partis politiques de se financer",
      "Contrôler les décisions du gouvernement",
      "Exprimer l’opinion publique sans effet contraignant"
    ],
    "c": "Permettre aux citoyens d’élire leurs représentants"
  },
  {
    "q": "Que garantit la séparation des pouvoirs ? (Niveau 1re)",
    "r": [
      "L’indépendance entre les fonctions exécutives, législatives et judiciaires",
      "Le contrôle du pouvoir judiciaire par l’exécutif",
      "L’élection directe des juges par les citoyens",
      "La concentration du pouvoir dans un seul organe"
    ],
    "c": "L’indépendance entre les fonctions exécutives, législatives et judiciaires"
  },
  {
    "q": "Quel philosophe a proposé l’idée de séparation des pouvoirs ? (Niveau 1re)",
    "r": [
      "Montesquieu",
      "Rousseau",
      "Platon",
      "Hobbes"
    ],
    "c": "Montesquieu"
  },
  {
    "q": "Qu’est-ce qu’une démocratie libérale ? (Niveau Terminale)",
    "r": [
      "Elle respecte les droits fondamentaux et organise des élections libres",
      "Elle interdit toute forme de contestation politique",
      "Elle limite la liberté d’expression pour maintenir l’ordre",
      "Elle réserve le pouvoir aux élites économiques"
    ],
    "c": "Elle respecte les droits fondamentaux et organise des élections libres"
  },
  {
    "q": "Pourquoi dit-on que la démocratie est perfectible ? (Niveau Terminale)",
    "r": [
      "Parce qu’elle évolue et s’adapte aux sociétés",
      "Parce qu’elle est par définition instable",
      "Parce qu’elle dépend du bon vouloir du chef de l’État",
      "Parce qu’elle limite la participation populaire"
    ],
    "c": "Parce qu’elle évolue et s’adapte aux sociétés"
  },
  {
    "q": "Quelle liberté fondamentale est garantie dans une démocratie ? (Niveau 2de)",
    "r": [
      "La liberté d'expression",
      "Le droit à une justice privée",
      "Le droit de refuser toute loi",
      "La liberté de censurer les élus"
    ],
    "c": "La liberté d'expression"
  },
  {
    "q": "Quel document fixe les règles principales d’une démocratie ? (Niveau 1re)",
    "r": [
      "La Constitution",
      "Le Code civil",
      "La Déclaration des droits de l’homme uniquement",
      "Le règlement intérieur du gouvernement"
    ],
    "c": "La Constitution"
  },
  {
    "q": "Quelle est la différence majeure entre démocratie directe et démocratie représentative ? (Niveau HGGSP)",
    "r": [
      "La démocratie directe implique un vote des citoyens sur chaque décision, contrairement à la démocratie représentative où les citoyens élisent des représentants.",
      "La démocratie représentative interdit les référendums.",
      "La démocratie directe fonctionne uniquement en monarchie.",
      "La démocratie représentative exclut les élections législatives."
    ],
    "c": "La démocratie directe implique un vote des citoyens sur chaque décision, contrairement à la démocratie représentative où les citoyens élisent des représentants."
  },
  {
    "q": "Quel est l’apport principal de Tocqueville dans sa réflexion sur la démocratie ? (Niveau HGGSP)",
    "r": [
      "Il critique la tyrannie de la majorité dans les régimes démocratiques.",
      "Il propose l’instauration d’un pouvoir héréditaire tempéré.",
      "Il défend une monarchie parlementaire.",
      "Il souhaite une démocratie sans libertés individuelles."
    ],
    "c": "Il critique la tyrannie de la majorité dans les régimes démocratiques."
  },
  {
    "q": "Pourquoi peut-on dire que la démocratie libérale repose sur des contre-pouvoirs ? (Niveau HGGSP)",
    "r": [
      "Parce que l'État y détient tous les pouvoirs.",
      "Car les libertés fondamentales peuvent être suspendues.",
      "Parce que les pouvoirs exécutif, législatif et judiciaire sont séparés et se contrôlent mutuellement.",
      "Car seule l’armée peut contester le président."
    ],
    "c": "Parce que les pouvoirs exécutif, législatif et judiciaire sont séparés et se contrôlent mutuellement."
  },
  {
    "q": "Quel est l’objectif du constitutionnalisme dans les démocraties modernes ? (Niveau HGGSP)",
    "r": [
      "Limiter l’arbitraire du pouvoir en le soumettant à un cadre juridique stable.",
      "Permettre au pouvoir exécutif de s’imposer sans contrôle.",
      "Rendre la Constitution révisable à volonté par l’exécutif.",
      "Supprimer les droits fondamentaux au nom de l’unité nationale."
    ],
    "c": "Limiter l’arbitraire du pouvoir en le soumettant à un cadre juridique stable."
  },
  {
    "q": "Pourquoi l’Union européenne est-elle parfois critiquée en matière de démocratie ? (Niveau HGGSP)",
    "r": [
      "Car elle impose un président à chaque pays.",
      "À cause du déficit démocratique perçu dans le fonctionnement de ses institutions.",
      "Parce qu’elle interdit les élections nationales.",
      "Car elle applique uniquement le droit américain."
    ],
    "c": "À cause du déficit démocratique perçu dans le fonctionnement de ses institutions."
  },
  {
    "q": "Quel est le rôle d’un régime de séparation souple des pouvoirs ? (Niveau HGGSP)",
    "r": [
      "Favoriser une collaboration entre exécutif et législatif tout en maintenant des mécanismes de contrôle mutuel.",
      "Supprimer la distinction entre exécutif et judiciaire.",
      "Garantir une absence totale de contrôle entre les pouvoirs.",
      "Fusionner les rôles de parlement et de cour constitutionnelle."
    ],
    "c": "Favoriser une collaboration entre exécutif et législatif tout en maintenant des mécanismes de contrôle mutuel."
  },
  {
    "q": "Quel événement marque le début du processus de démocratisation en Europe de l’Est après la guerre froide ? (Niveau HGGSP)",
    "r": [
      "La chute du mur de Berlin (1989).",
      "La fondation de l’ONU.",
      "La révolution industrielle.",
      "Le traité de Maastricht."
    ],
    "c": "La chute du mur de Berlin (1989)."
  },
  {
    "q": "Qu’est-ce qu’une démocratie illibérale ? (Niveau HGGSP)",
    "r": [
      "Un régime qui conserve des élections mais affaiblit les libertés fondamentales et l’État de droit.",
      "Une démocratie où les citoyens votent deux fois par an.",
      "Une monarchie constitutionnelle déguisée.",
      "Une démocratie dirigée par des multinationales."
    ],
    "c": "Un régime qui conserve des élections mais affaiblit les libertés fondamentales et l’État de droit."
  },
  {
    "q": "Quel est l’impact du numérique sur la démocratie contemporaine ? (Niveau HGGSP)",
    "r": [
      "Il peut à la fois renforcer la participation citoyenne et faciliter la manipulation de l’opinion publique.",
      "Il interdit la liberté d’expression.",
      "Il supprime les élections locales.",
      "Il garantit la vérité absolue dans les débats politiques."
    ],
    "c": "Il peut à la fois renforcer la participation citoyenne et faciliter la manipulation de l’opinion publique."
  },
  {
    "q": "Quel est l’objectif du référendum d’initiative citoyenne (RIC) ? (Niveau HGGSP)",
    "r": [
      "Permettre aux citoyens de proposer ou d’abroger une loi sans passer par le Parlement.",
      "Permettre au président de nommer les juges.",
      "Autoriser l’armée à intervenir dans la vie politique.",
      "Rendre le vote obligatoire pour les moins de 18 ans."
    ],
    "c": "Permettre aux citoyens de proposer ou d’abroger une loi sans passer par le Parlement."
  }
]




    # Permet d'avoir les questions pas dans le même ordre que prévue
    random.shuffle(questions)

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

        bouton_de = ttk.Button(frame_reponses, text="🎲 Lancer le dé", command=afficher_question, style="Accent.TButton")
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
                ttk.Button(frame_reponses, style="Accent.TButton", text=r, command=lambda rep=r: verifier_reponse(rep)).pack(pady=5, fill="x")
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
        ttk.Button(frame_reponses, text="Terminer la partie", style="Accent.TButton", command=fenetre.destroy).pack(pady=10)

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

        ttk.Button(bouton_frame, text="Revenir au jeu", command=confirmation.destroy, style="Accent.TButton").pack(side="left", padx=10)
        ttk.Button(bouton_frame, text="Abandonner", command=confirmer_abandon, style="TButton").pack(side="left", padx=10)

    ttk.Button(frame_bas, text="Abandonner la partie", command=abandonner_partie, style="TButton").pack(side="right")
    afficher_intro_question()
