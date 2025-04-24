import tkinter as tk
from tkinter import messagebox
import sv_ttk as sv

def lancer_fenetre_question():
    # Fenêtre principale
    fenetre = tk.Toplevel()
    fenetre.title("Jeu EMC")
    fenetre.geometry("600x400")
    fenetre.configure(bg="#1c1c1c")
    fenetre.resizable(False, False)
    sv.set_theme("dark")

    # Empêche la fermeture avec la croix
    def on_closing():
        pass  # Ne fait rien

    fenetre.protocol("WM_DELETE_WINDOW", on_closing)

    # Variables globales locales à la fonction
    score = 0
    index_question = 0
    score_var = tk.IntVar(value=0)

    questions = [
        {"q": "Capitale de la France ?", "r": ["Paris", "Londres", "Berlin", "Madrid"], "c": "Paris"},
        {"q": "7 x 8 ?", "r": ["54", "56", "49", "63"], "c": "56"},
        {"q": "Peintre de la Joconde ?", "r": ["Van Gogh", "Monet", "Léonard de Vinci", "Picasso"], "c": "Léonard de Vinci"},
        {"q": "Symbole chimique de l'eau ?", "r": ["O2", "H2O", "CO2", "NaCl"], "c": "H2O"},
    ]

    # Widgets
    question_label = tk.Label(fenetre, text="", font=("Arial", 14), bg="#1c1c1c", fg="white")
    question_label.pack(pady=20)

    score_label = tk.Label(fenetre, text="Score : 0", font=("Arial", 12), bg="#1c1c1c", fg="white")
    score_label.pack()
    score_label.config(textvariable=score_var)

    frame_reponses = tk.Frame(fenetre, bg="#1c1c1c")
    frame_reponses.pack()

    frame_bas = tk.Frame(fenetre, bg="#1c1c1c")
    frame_bas.pack(side="bottom", fill="x", padx=10, pady=10)

    def afficher_question():
        nonlocal index_question, score
        if index_question < len(questions):
            q = questions[index_question]
            question_label.config(text=q["q"])

            for widget in frame_reponses.winfo_children():
                widget.destroy()

            for r in q["r"]:
                tk.Button(frame_reponses, text=r, font=("Arial", 12),
                          command=lambda rep=r: verifier_reponse(rep)).pack(pady=5, fill="x")
        else:
            question_label.config(text="Le quiz est terminé ! 🎉")
            for widget in frame_reponses.winfo_children():
                widget.destroy()
            tk.Label(frame_reponses, text=f"Votre score : {score}/{len(questions)}",
                     font=("Arial", 12), bg="#1c1c1c", fg="white").pack()
            tk.Label(frame_reponses, text="Vous pouvez fermer la fenêtre.",
                     font=("Arial", 10), bg="#1c1c1c", fg="gray").pack()
            tk.Button(frame_reponses, text="Terminer la partie", font=("Arial", 11),
                      command=fenetre.destroy).pack(pady=10)

    def verifier_reponse(reponse):
        nonlocal index_question, score
        if index_question < len(questions):
            if reponse == questions[index_question]["c"]:
                score += 1
                score_var.set(score)
            index_question += 1
            afficher_question()

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

        tk.Label(confirmation, text="Êtes-vous certain de vouloir abandonner la partie ?\nVotre score sera de 0 et vous devrez reprendre de 0.",
                 font=("Arial", 11), bg="#1c1c1c", fg="white", wraplength=380).pack(pady=20)

        bouton_frame = tk.Frame(confirmation, bg="#1c1c1c")
        bouton_frame.pack(pady=10)

        tk.Button(bouton_frame, text="Revenir au jeu", command=confirmation.destroy).pack(side="left", padx=10)
        tk.Button(bouton_frame, text="Abandonner", command=confirmer_abandon).pack(side="left", padx=10)

    tk.Button(frame_bas, text="Abandonner la partie", command=abandonner_partie).pack(side="right")

    afficher_question()
