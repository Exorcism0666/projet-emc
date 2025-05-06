import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk as sv
from liste_question import questions
import random
import serial
import threading
import time

# Configuration du port série
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

# Fonction pour lire le résultat du dé depuis l'Arduino
def lire_resultat_de(callback):
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=10)
        line = ser.readline().decode('utf-8').strip()
        ser.close()
        if line.isdigit():
            callback(int(line))
        else:
            print("Valeur invalide reçue :", line)
            callback(None)
    except serial.SerialException as e:
        print("Erreur de communication série:", e)
        callback(None)

def lancer_fenetre_question(pseudos):
    fenetre = tk.Toplevel()
    fenetre.title("Jeu EMC")
    fenetre.geometry("1200x400")
    fenetre.configure(bg="#1c1c1c")
    fenetre.resizable(False, False)
    sv.set_theme("dark")

    index_question = 0
    joueurs = pseudos
    nb_joueurs = len(joueurs)
    scores = {j.strip(): 0 for j in joueurs}
    score_vars = {j.strip(): tk.IntVar(value=0) for j in joueurs}
    questions_posees = {j.strip(): 0 for j in joueurs}
    joueur_actuel_index = 0

    timer_id = None
    temps_restant = 20

    couleurs_fixes = ["#FF3B30", "#007AFF", "#FFD60A", "#34C759"]
    couleurs_joueurs = {j.strip(): couleurs_fixes[i % len(couleurs_fixes)] for i, j in enumerate(joueurs)}
    random.shuffle(questions)

    frame_scoreboard = tk.Frame(fenetre, bg="#2b2b2b", width=200)
    frame_scoreboard.pack(side="left", fill="y")
    tk.Label(frame_scoreboard, text="Scores", font=("Arial", 14, "bold"), bg="#2b2b2b", fg="white").pack(pady=10)
    label_scoreboard = {}

    for j in joueurs:
        pseudo = j.strip()
        couleur = couleurs_joueurs[pseudo]
        line = tk.Frame(frame_scoreboard, bg="#2b2b2b")
        line.pack(anchor="w", padx=10, pady=5)
        label = tk.Label(line, text=pseudo, font=("Arial", 11), bg="#2b2b2b", fg=couleur)
        label.pack(side="left")
        tk.Label(line, textvariable=score_vars[pseudo], font=("Arial", 11), bg="#2b2b2b", fg="white").pack(side="right")
        label_scoreboard[pseudo] = label

    main_frame = tk.Frame(fenetre, bg="#1c1c1c")
    main_frame.pack(fill="both", expand=True)

    label_timer = tk.Label(main_frame, text="", font=("Arial", 14, "bold"), bg="#1c1c1c", fg="white")
    label_timer.pack(pady=(10, 0))

    pseudo_label = tk.Label(main_frame, text="", font=("Arial", 18, "bold"), bg="#1c1c1c", fg="white")
    pseudo_label.pack(pady=(10, 5))

    question_label = tk.Label(main_frame, text="", font=("Arial", 14), bg="#1c1c1c", fg="white", wraplength=600)
    question_label.pack(pady=5)

    frame_reponses = tk.Frame(main_frame, bg="#1c1c1c")
    frame_reponses.pack()

    frame_bas = tk.Frame(main_frame, bg="#1c1c1c")
    frame_bas.pack(side="bottom", fill="x", padx=10, pady=10)

    def mettre_a_jour_scoreboard():
        for j in joueurs:
            pseudo = j.strip()
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
        for widget in frame_reponses.winfo_children():
            widget.destroy()
        joueur = joueurs[joueur_actuel_index].strip()
        couleur = couleurs_joueurs[joueur]
        mettre_a_jour_scoreboard()

        pseudo_label.config(text=joueur, fg=couleur)
        label_timer.config(text="")
        question_label.config(text="Appuie sur le bouton (Arduino) avant de répondre à la question.", fg="white")

        bouton_de = ttk.Button(frame_reponses, text="🎲 Lire le résultat du dé", style="Accent.TButton",
                               command=lire_de_depuis_arduino)
        bouton_de.pack(pady=20)

    def lire_de_depuis_arduino():
        for widget in frame_reponses.winfo_children():
            widget.destroy()
        label_timer.config(text="Attente du résultat de l'Arduino...", fg="gray")
        threading.Thread(target=lire_resultat_de, args=(apres_lancer_de,), daemon=True).start()

    def apres_lancer_de(valeur):
        if valeur is None:
            messagebox.showerror("Erreur", "Impossible de lire le résultat du dé depuis l'Arduino.")
            afficher_intro_question()
        else:
            label_timer.config(text=f"🎲 Résultat du dé : {valeur}", fg="green")
            fenetre.after(2000, afficher_question)

    def afficher_question():
        nonlocal index_question, temps_restant, timer_id
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
                ttk.Button(frame_reponses, text=r, style="Accent.TButton",
                           command=lambda rep=r: verifier_reponse(rep)).pack(pady=5, fill="x")

            lancer_timer()
        else:
            afficher_classement()

    def verifier_reponse(reponse):
        nonlocal joueur_actuel_index, index_question, timer_id
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
        for j in joueurs:
            pseudo = j.strip()
            score = scores[pseudo]
            total = questions_posees[pseudo]
            pct = (score / total) * 100 if total else 0
            classement.append((pseudo, score, total, pct))
        classement.sort(key=lambda x: x[3], reverse=True)
        for nom, pts, total_q, pct in classement:
            couleur = couleurs_joueurs[nom]
            tk.Label(frame_reponses, text=f"{nom} : {pts}/{total_q} ({pct:.1f}%)", font=("Arial", 12), bg="#1c1c1c", fg=couleur).pack()
        ttk.Button(frame_reponses, text="Terminer la partie", command=fenetre.destroy, style="Accent.TButton").pack(pady=10)

    def abandonner_partie():
        def confirmer():
            fenetre.destroy()
        confirmation = tk.Toplevel(fenetre)
        confirmation.title("Abandon")
        confirmation.geometry("400x200")
        confirmation.configure(bg="#1c1c1c")
        sv.set_theme("dark")
        confirmation.protocol("WM_DELETE_WINDOW", lambda: None)
        tk.Label(confirmation, text="Voulez-vous abandonner la partie ?", font=("Arial", 11), bg="#1c1c1c", fg="white").pack(pady=20)
        frame = tk.Frame(confirmation, bg="#1c1c1c")
        frame.pack()
        ttk.Button(frame, text="Revenir", command=confirmation.destroy).pack(side="left", padx=10)
        ttk.Button(frame, text="Abandonner", command=confirmer).pack(side="left", padx=10)

    ttk.Button(frame_bas, text="Abandonner la partie", command=abandonner_partie).pack(side="right")
    afficher_intro_question()
