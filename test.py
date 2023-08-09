import tkinter as tk

def confirmer():
    print("Action confirmée!")

def annuler():
    print("Action annulée!")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Exemple de Boutons")

# Créer une frame pour contenir les boutons
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Créer le bouton "Confirmer"
bouton_confirmer = tk.Button(frame, text="Confirmer", command=confirmer)
bouton_confirmer.pack(side=tk.LEFT, padx=10)

# Créer le bouton "Annuler"
bouton_annuler = tk.Button(frame, text="Annuler", command=annuler)
bouton_annuler.pack(side=tk.LEFT, padx=10)

# Lancer la boucle principale
root.mainloop()