import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk as sv
from liste_question import questions
import random
import serial
import threading
import time
from utils import centrage_de_fenetre
from serial.tools import list_ports

BAUD_RATE = 9600

def detecter_port_esp32():
    ports = list_ports.comports()
    for port in ports:
        if ("ESP32" in port.description or 
            "Silicon Labs" in str(port.manufacturer) or
            "USB Serial" in port.description or
            "CP210" in port.description or
            "CH340" in port.description):
            print(f"[INFO] ESP32 détecté sur {port.device} ({port.description})")
            return port.device
    return None

def lire_resultat_de(callback):
    try:
        port = detecter_port_esp32()
        if port is None:
            print("❌ Aucun ESP32 détecté. Veuillez connecter l'appareil.")
            callback(None)
            return

        with serial.Serial(port, BAUD_RATE, timeout=30) as ser:
            # Empêche le reset automatique de l'ESP32
            ser.dtr = False
            ser.rts = False
            time.sleep(2.5)  # attendre le boot complet

            ser.reset_input_buffer()
            ser.write(b"start\n")
            print("[Python] → 'start' envoyé, attente bouton utilisateur...")

            ligne = ""
            start_time = time.time()
            while True:
                if ser.in_waiting:
                    ligne = ser.readline().decode('utf-8').strip()
                    print("[Python] ← Reçu :", repr(ligne))
                    if ligne.isdigit():
                        callback(int(ligne))
                        return
                    else:
                        print("⚠️ Réponse invalide reçue :", ligne)
                        break
                if time.time() - start_time > 60:
                    print("⏱ Timeout après 60 secondes sans réponse.")
                    break
                time.sleep(0.1)
            callback(None)
    except serial.SerialException as e:
        print("❌ Erreur de communication série:", e)
        callback(None)

def lancer_fenetre_question(pseudos):
    fenetre = tk.Toplevel()
    fenetre.title("Jeu EMC")
    centrage_de_fenetre(fenetre, 1200, 400)
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
    temps_restant = 60

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
        for widget in frame_reponses.winfo_children():
            widget.destroy()
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
        question_label.config(text="Appuie sur le bouton (ESP32) pour lancer le d\u00e9.", fg="white")

        bouton_de = ttk.Button(frame_reponses, text="🎲 Lire le r\u00e9sultat du d\u00e9", style="Accent.TButton",
                               command=lire_de_depuis_esp32)
        bouton_de.pack(pady=20)

    def lire_de_depuis_esp32():
        for widget in frame_reponses.winfo_children():
            widget.destroy()
        label_timer.config(text="Pr\u00e9paration du d\u00e9...", fg="gray")

        def thread_fonction():
            lire_resultat_de(lambda val: fenetre.after(0, lambda: apres_lancer_de(val)))

        threading.Thread(target=thread_fonction, daemon=True).start()

    def apres_lancer_de(valeur):
        if valeur is None:
            messagebox.showerror("Erreur", "ESP32 non détecté ou problème de lecture.\nVeuillez vérifier la connexion USB.")
            afficher_intro_question()
        else:
            label_timer.config(text=f"🎲 Résultat du dé : {valeur}", fg="green")
            # Affiche le résultat plus longtemps
            fenetre.after(4000, afficher_question)

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
        nonlocal timer_id
        if timer_id:
            fenetre.after_cancel(timer_id)

        for widget in frame_reponses.winfo_children():
            widget.config(state="disabled")

        joueur = joueurs[joueur_actuel_index].strip()
        questions_posees[joueur] += 1
        bonne_reponse = questions[index_question]["c"]
        est_bonne = (reponse == bonne_reponse)

        if est_bonne:
            scores[joueur] += 1
            score_vars[joueur].set(scores[joueur])
            question_label.config(text="✅ Bonne r\u00e9ponse !", fg="green")
        else:
            question_label.config(text=f"❌ Mauvaise r\u00e9ponse.\nLa bonne r\u00e9ponse \u00e9tait : {bonne_reponse}", fg="red")

        ttk.Button(frame_reponses, text="👉 Continuer", style="Accent.TButton",
                   command=passer_joueur_suivant).pack(pady=10)

    def afficher_classement():
        pseudo_label.config(text="")
        label_timer.config(text="")
        question_label.config(text="Le quiz est termin\u00e9 ! 🎉", fg="white")
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
        def confirmer_abandon():
            fenetre.destroy()

        confirmation = tk.Toplevel(fenetre)
        confirmation.title("Confirmer l'abandon")
        centrage_de_fenetre(confirmation, 1200, 400)
        confirmation.configure(bg="#1c1c1c")
        confirmation.resizable(False, False)
        sv.set_theme("dark")
        confirmation.protocol("WM_DELETE_WINDOW", lambda: None)
        tk.Label(confirmation, text="\u00cates-vous certain de vouloir abandonner la partie ?\nVotre progression ne sera pas conserv\u00e9", font=("Arial", 20), bg="#1c1c1c", fg="red", wraplength=500).pack(pady=20)
        bouton_frame = tk.Frame(confirmation, bg="#1c1c1c")
        bouton_frame.pack(pady=10)
        ttk.Button(bouton_frame, text="Revenir au jeu", command=confirmation.destroy, style="Accent.TButton").pack(side="left", padx=30)
        ttk.Button(bouton_frame, text="Abandonner", command=confirmer_abandon, style="TButton").pack(side="left", padx=30)
        confirmation.grab_set()
        confirmation.focus_force()
        confirmation.wait_window()

    ttk.Button(frame_bas, text="Abandonner la partie", command=abandonner_partie, style="TButton").pack(side="right")
    afficher_intro_question()
