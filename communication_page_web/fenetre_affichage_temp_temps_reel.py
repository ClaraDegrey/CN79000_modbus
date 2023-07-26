import tkinter as tk
from tkinter import messagebox
import requests
import re


def fetch_temperature():
    response = requests.get(url)
    html_content = response.text

    temperature_regex = r"La temperature est de ([\d.]+) degres"
    match = re.search(temperature_regex, html_content)
    if match:
        return float(match.group(1))
    else:
        return None



def valider_temperature():
    global temperature_souhaitee

    try:
        temperature_souhaitee = float(temperature_entry.get())
        if -500 <= temperature_souhaitee <= 1000:
            temperature_actuelle.set(temperature_souhaitee)
            messagebox.showinfo("Succès", "Température enregistrée : {:.2f}°C".format(temperature_souhaitee))
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez saisir une température valide (-500 à 1000)")
        temperature_entry.delete(0, tk.END)

url = "http://192.168.0.2/"

fenetre = tk.Tk()
fenetre.title("Réglage de la température du four")

# Définition de la taille en pixels pour une taille de 10 cm
largeur_pixels = int(fenetre.winfo_fpixels("10c"))

# Calcul des coordonnées pour centrer la fenêtre sur l'écran
largeur_ecran = fenetre.winfo_screenwidth()
hauteur_ecran = fenetre.winfo_screenheight()
x_pos = int((largeur_ecran - largeur_pixels) / 2)
y_pos = int((hauteur_ecran - largeur_pixels) / 2)

fenetre.geometry(f"{largeur_pixels}x200+{x_pos}+{y_pos}")

temperature_actuelle = tk.DoubleVar()
temperature_actuelle.set(fetch_temperature())

temperature_label = tk.Label(fenetre, text="Température souhaitée (°C):")
temperature_label.pack()

temperature_entry = tk.Entry(fenetre)
temperature_entry.pack()

temperature_actuelle_label = tk.Label(fenetre, text="Température actuelle : {:.2f}°C".format(temperature_actuelle.get()))
temperature_actuelle_label.pack()

valider_button = tk.Button(fenetre, text="Valider", command=valider_temperature)
valider_button.pack()



fenetre.mainloop()

while True:
    temperature=fetch_temperature()
    print(temperature)
