import tkinter as tk
from tkinter import ttk
import sv_ttk as sv

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Jeu EMC")
fenetre.geometry("600x500")
fenetre.configure(bg="#1c1c1c")
fenetre.resizable(False, False)
sv.set_theme("dark")

# Scores des joueurs
scores = [0, 0, 0, 0]

# Liste de questions et réponses (dans l'ordre)
questions_reponses = [
    {"question": "Quelle est la capitale de la France ?", "reponses": ["Paris", "Londres", "Berlin", "Madrid"], "correcte": "Paris"},
    {"question": "Combien font 7 x 8 ?", "reponses": ["54", "56", "49", "63"], "correcte": "56"},
    {"question": "Qui a peint la Joconde ?", "reponses": ["Van Gogh", "Monet", "Léonard de Vinci", "Picasso"], "correcte": "Léonard de Vinci"},
    {"question": "Quel est le symbole chimique de l'eau ?", "reponses": ["O2", "H2O", "CO2", "NaCl"], "correcte": "H2O"},
]

# Indices pour suivre l'état du jeu
index_question = 0
joueur_actuel = 0  # Le premier joueur commence

# Fonction pour mettre à jour le score
def augmenter_score(joueur):
    scores[joueur] += 1
    labels_score[joueur].config(text=f"Joueur {joueur+1}: {scores[joueur]}")

# Fonction pour afficher la prochaine question
def prochaine_question():
    global index_question, joueur_actuel

    if index_question < len(questions_reponses):
        question_actuelle = questions_reponses[index_question]
        question_label.config(text=question_actuelle["question"])
        tour_label.config(text=f"Tour du Joueur {joueur_actuel+1}", foreground=["red", "blue", "green", "yellow"][joueur_actuel])

        for i in range(4):
            boutons_reponse[i].config(
                text=question_actuelle["reponses"][i],
                state="normal",
                command=lambda i=i: verifier_reponse(joueur_actuel, boutons_reponse[i].cget("text"))
            )

    else:
        question_label.config(text="Fin du quiz ! 🎉")
        tour_label.config(text="Merci d'avoir joué !", foreground="white")
        for bouton in boutons_reponse:
            bouton.config(state="disabled")

# Fonction pour vérifier la réponse et passer au joueur suivant
def verifier_reponse(joueur, reponse):
    global index_question, joueur_actuel
    question_actuelle = questions_reponses[index_question]

    if reponse == question_actuelle["correcte"]:
        augmenter_score(joueur)

    for bouton in boutons_reponse:
        bouton.config(state="disabled")  # Désactive les boutons après réponse

    # Passer au joueur suivant
    joueur_actuel = (joueur_actuel + 1) % 4  # Tourne entre 0 et 3
    index_question += 1

    fenetre.after(2000, prochaine_question)  # Passe à la prochaine question après 2 secondes

# Cadre des scores (en haut à gauche)
frame_scores = tk.Frame(fenetre, bg="#1c1c1c")
frame_scores.place(x=10, y=10)

labels_score = []
for i in range(4):
    label = ttk.Label(frame_scores, text=f"Joueur {i+1}: {scores[i]}", font=("Arial", 12, "bold"), foreground="white", background="#1c1c1c")
    label.pack(anchor="w", pady=2)
    labels_score.append(label)

# Indicateur du tour actuel (au-dessus de la question)
tour_label = ttk.Label(fenetre, text="Tour du Joueur 1", font=("Arial", 14, "bold"), foreground="red", background="#1c1c1c")
tour_label.place(relx=0.5, rely=0.3, anchor="center")

# Affichage de la question (au centre)
question_label = ttk.Label(fenetre, text="", font=("Arial", 16, "bold"), foreground="white", background="#1c1c1c", wraplength=500, justify="center")
question_label.place(relx=0.5, rely=0.4, anchor="center")

# Cadre pour les boutons de réponse
frame_reponses = tk.Frame(fenetre, bg="#1c1c1c")
frame_reponses.place(relx=0.5, rely=0.6, anchor="center")

boutons_reponse = []
for i in range(4):
    bouton = ttk.Button(frame_reponses, text="", state="disabled")
    bouton.pack(fill="x", padx=20, pady=5)
    boutons_reponse.append(bouton)


# Lancement du jeu avec la première question
prochaine_question()

fenetre.mainloop()
