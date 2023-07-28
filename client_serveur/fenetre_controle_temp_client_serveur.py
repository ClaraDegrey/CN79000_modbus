import socket
import time
from tkinter import *
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog

ip_address = "192.168.0.2"  # Adresse IP de la carte Arduino
port = 80  # Port sur lequel la carte Arduino écoute

temperatures = []  # Liste pour stocker les valeurs de température
timestamps = []  # Liste pour stocker les horodatages correspondants


def enregistrer_temperature(ip_address, port):
    variable_value = 'r'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_address, port))
    sock.send(str(variable_value).encode())
    data = sock.recv(1024).decode()
    time.sleep(1)
    sock.close()
    return int(data) / 10.0


def lecture_temperature(ip_address, port):
    variable_value = 'r'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_address, port))
    sock.send(str(variable_value).encode())
    data = sock.recv(1024).decode()
    time.sleep(1)
    sock.close()
    return int(data) / 10.0


def lecture_temperature_consigne(ip_address, port):
    variable_value = 't'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_address, port))
    sock.send(str(variable_value).encode())
    data = sock.recv(1024).decode()
    dataint=int(data)
    time.sleep(1)
    sock.close()
    if dataint >= 1000:
        return dataint / 10.0-6553.6
    else:
        return dataint / 10.0

def modification_temperature_consigne(ip_address, port, temperature_consigne_desiree):
    variable_value = 's'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_address, port))
    sock.send(str(variable_value).encode())
    sock.send(str(int(temperature_consigne_desiree * 10)).encode())
    time.sleep(1)
    sock.close()


def update_temperatures():
    temperature_four = lecture_temperature(ip_address, port)
    temperature_consigne = lecture_temperature_consigne(ip_address, port)
    label_temperature_four.config(text="Température actuelle : {:.1f} °C".format(temperature_four))

    if temperature_consigne >= 0:
        label_temperature_consigne.config(text="Température d'asservissement : {:.1f} °C".format(temperature_consigne))
    else:
        label_temperature_consigne.config(text="Température d'asservissement : -{:.1f} °C".format(abs(temperature_consigne)))


    # Ajouter la valeur actuelle à la liste des températures
    temperatures.append(temperature_four)
    timestamps.append(time.time())

    # Tracer le graphe de température
    ax.clear()
    ax.plot(timestamps, temperatures, '-o')
    ax.set_xlabel('Temps')
    ax.set_ylabel('Température (°C)')
    ax.set_title('Température en direct')
    fig.canvas.draw()

    # Planifier la prochaine mise à jour
    gui.after(1000, update_temperatures)


def validate_entry():
    temp_asservissement_string = myEntry.get()
    try:
        temperature_consigne_desiree = float(temp_asservissement_string)
        if -100 <= temperature_consigne_desiree <= 200:
            modification_temperature_consigne(ip_address, port, temperature_consigne_desiree)
        else:
            messagebox.showerror("Erreur", "Veuillez saisir une température entre -100 et 200.")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez saisir une température valide.")


def check_entry():
    temp_asservissement_string = myEntry.get()
    try:
        temperature_consigne_desiree = float(temp_asservissement_string)
        if -100 <= temperature_consigne_desiree <= 200:
            btn.config(state=tk.NORMAL)
        else:
            btn.config(state=tk.DISABLED)
    except ValueError:
        btn.config(state=tk.DISABLED)
    gui.after(100, check_entry)


def save_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".dat")
    if file_path:
        with open(file_path, "w") as file:
            for t, temp in zip(timestamps, temperatures):
                file.write("{:.2f}, {:.2f}\n".format(t, temp))

gui = tk.Tk()
gui.geometry("800x700")
gui.title("Fenêtre de contrôle de température")

label_temperature_four = tk.Label(gui, text="Température du four :")
label_temperature_four.pack(pady=10)

label_temperature_consigne = tk.Label(gui, text="Température d'asservissement :")
label_temperature_consigne.pack(pady=10)

myEntry = tk.Entry(gui, width=40)
myEntry.pack(pady=10)
btn = tk.Button(gui, height=1, width=10, text="Valider", command=validate_entry, state=tk.DISABLED)
btn.pack()

save_button = tk.Button(gui, height=1, width=10, text="Enregistrer", command=save_data)
save_button.pack()

# Initialiser le graphe
fig = plt.Figure(figsize=(8, 6))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=gui)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

check_entry()
update_temperatures()
gui.mainloop()
