import tkinter as tk
from tkinter import messagebox
import sv_ttk as sv

# Fenêtre principale
fenetre = tk.Tk()
fenetre.title("Jeu EMC")
fenetre.geometry("600x400")
fenetre.configure(bg="#1c1c1c")
fenetre.resizable(False, False)
sv.set_theme("dark")

# Variables globales
score = 0
index_question = 0
score_var = tk.IntVar(value=0)  # Variable Tkinter pour stocker dynamiquement le score

# Questions
questions = [
    {"q": "Capitale de la France ?", "r": ["Paris", "Londres", "Berlin", "Madrid"], "c": "Paris"},
    {"q": "7 x 8 ?", "r": ["54", "56", "49", "63"], "c": "56"},
    {"q": "Peintre de la Joconde ?", "r": ["Van Gogh", "Monet", "Léonard de Vinci", "Picasso"], "c": "Léonard de Vinci"},
    {"q": "Symbole chimique de l'eau ?", "r": ["O2", "H2O", "CO2", "NaCl"], "c": "H2O"},
]

# Widgets
question_label = tk.Label(fenetre, text="", font=("Arial", 14), bg="#1c1c1c", fg="white")
question_label.pack(pady=20)

# Label pour afficher le score
score_label = tk.Label(fenetre, text="Score : 0", font=("Arial", 12), bg="#1c1c1c", fg="white")
score_label.pack()
score_label.config(textvariable=score_var)  # Associer score_var au label

frame_reponses = tk.Frame(fenetre, bg="#1c1c1c")
frame_reponses.pack()

# Fonction pour afficher la question
def afficher_question():
    global index_question
    if index_question < len(questions):
        q = questions[index_question]
        question_label.config(text=q["q"])

        # Supprimer les anciens boutons
        for widget in frame_reponses.winfo_children():
            widget.destroy()

        # Créer de nouveaux boutons pour les réponses
        for r in q["r"]:
            tk.Button(frame_reponses, text=r, font=("Arial", 12),
                      command=lambda rep=r: verifier_reponse(rep)).pack(pady=5, fill="x")
    else:
        question_label.config(text="Le quiz est terminé ! 🎉")  # Message final
        for widget in frame_reponses.winfo_children():
            widget.destroy()
        tk.Label(frame_reponses, text=f"Votre score : {score}/{len(questions)}",
                 font=("Arial", 12), bg="#1c1c1c", fg="white").pack()
        tk.Label(frame_reponses, text="Vous pouvez fermer la fenêtre.",
                 font=("Arial", 10), bg="#1c1c1c", fg="gray").pack()

# Fonction pour vérifier la réponse
def verifier_reponse(reponse):
    global score, index_question, score_var
    if index_question < len(questions):
        if reponse == questions[index_question]["c"]:
            score += 1
            score_var.set(score)  # Mise à jour du score affiché
        index_question += 1
        afficher_question()

# Lancer le jeu
afficher_question()
fenetre.mainloop()
