import tkinter as tk
from tkinter import ttk
import webbrowser

def ouvrir_lien_mit():
    webbrowser.open("https://github.com/Exorcism0666/projet-emc/blob/main/LICENSE")

def afficher_message_bloquant(titre, message):
    popup = tk.Toplevel()
    popup.title(titre)
    popup.configure(bg="#1c1c1c")
    popup.resizable(False, False)
    popup.transient(parent)
    label = ttk.Label(popup, text=message, font=("Arial", 12), background="#1c1c1c", foreground="white", wraplength=280)
    label.pack(pady=20, padx=20)
    ttk.Button(popup, text="OK", command=popup.destroy).pack()

    popup.update_idletasks()
    largeur = popup.winfo_width()
    hauteur = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (largeur // 2)
    y = (popup.winfo_screenheight() // 2) - (hauteur // 2)
    popup.geometry(f"{largeur}x{hauteur}+{x}+{y}")

    popup.grab_set()           # Empêche toute interaction avec les autres fenêtres
    popup.focus_force()        # Donne le focus à la fenêtre popup
    popup.wait_window()        # Attend que le popup soit fermé avant de poursuivre

def effet_fondu(titre, opacity=0):
    if opacity <= 1.0:
        couleur = f"#{int(opacity * 255):02x}{int(opacity * 255):02x}{int(opacity * 255):02x}"
        titre.config(foreground=couleur)
        titre.after(50, effet_fondu, titre, opacity + 0.05)

def afficher_texte(texte_intro, description, index=0):
    if index < len(description):
        texte_intro.config(text=description[:index+1])
        texte_intro.after(50, afficher_texte, texte_intro, description, index+1)

def centrage_de_fenetre(window, width=400, height=300):
    """Centre une fenêtre Tkinter sur l'écran."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{x}+{y}")
