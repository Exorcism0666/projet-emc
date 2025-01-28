import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sv_ttk

# Fonction liée aux boutons
def bouton_action_1():
    messagebox.showinfo("Bouton 1", "Action pour le bouton 1")

def bouton_action_2():
    messagebox.showinfo("Bouton 2", "Action pour le bouton 2")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Jeu emc")
fenetre.geometry("500x400")  # Taille de la fenêtre

# Application du thème sv-ttk
sv_ttk.set_theme("dark")  # Vous pouvez changer en "light" pour un thème clair

# Création du style personnalisé pour les boutons
style = ttk.Style()
style.configure("Large.Accent.TButton", padding=(20, 10), font=("Arial", 14), background="#007BFF", foreground="black")
style.map(
    "Large.Blue.TButton",
    background=[("active", "#0056b3"), ("pressed", "#004494")]
)

# Ajout d'un titre
titre = ttk.Label(fenetre, text="La démocratie han", font=("Arial", 18, "bold"), anchor="center")
titre.pack(pady=20)  # Espacement au-dessus et au-dessous du titre

# Création d'un cadre pour les boutons
cadre_boutons = ttk.Frame(fenetre)  # Utilisation de ttk pour compatibilité avec sv-ttk
cadre_boutons.place(relx=0.5, rely=0.5, anchor="center")  # Centrer le cadre

# Ajout des boutons au cadre avec le style "Large.Blue.TButton"
btn_1 = ttk.Button(cadre_boutons, text="Bouton 1", command=bouton_action_1, style="Large.Accent.TButton")
btn_1.pack(pady=15)  # Espacement vertical

btn_2 = ttk.Button(cadre_boutons, text="Bouton 2", command=bouton_action_2, style="Large.Accent.TButton")
btn_2.pack(pady=15)

# Boucle principale de l'application
fenetre.mainloop()
