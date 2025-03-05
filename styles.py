import tkinter.ttk as ttk

def configurer_styles():
    style = ttk.Style()
    style.configure("Large.Accent.TButton", padding=(20, 10), font=("Arial", 14))
    style.configure("Green.TButton",
                    background="#4CAF50",  # Couleur verte
                    foreground="white",   # Texte blanc
                    font=("Arial", 14),  # Police
                    padding=(20, 10))    # Padding