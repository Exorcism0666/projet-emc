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
    popup.grab_set()

    label = ttk.Label(popup, text=message, font=("Arial", 12), background="#1c1c1c", foreground="white", wraplength=280)
    label.pack(pady=20, padx=20)
    ttk.Button(popup, text="OK", command=popup.destroy).pack()

    popup.update_idletasks()
    largeur = popup.winfo_width()
    hauteur = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (largeur // 2)
    y = (popup.winfo_screenheight() // 2) - (hauteur // 2)
    popup.geometry(f"{largeur}x{hauteur}+{x}+{y}")

def effet_fondu(titre, opacity=0):
    if opacity <= 1.0:
        couleur = f"#{int(opacity * 255):02x}{int(opacity * 255):02x}{int(opacity * 255):02x}"
        titre.config(foreground=couleur)
        titre.after(50, effet_fondu, titre, opacity + 0.05)

def afficher_texte(texte_intro, description, index=0):
    if index < len(description):
        texte_intro.config(text=description[:index+1])
        texte_intro.after(50, afficher_texte, texte_intro, description, index+1)