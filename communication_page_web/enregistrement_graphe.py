import matplotlib.pyplot as plt

# Demander à l'utilisateur de saisir le nom et l'emplacement du fichier .data
file_path = input("Entrez le chemin et le nom du fichier .data: ")

# Lire les données du fichier .data
timestamps = []
temperatures = []
with open(file_path, "r") as file:
    for line in file:
        timestamp, temperature = line.strip().split(", ")
        timestamps.append(int(timestamp))
        temperatures.append(float(temperature))

# Afficher la courbe de température
plt.plot(timestamps, temperatures)
plt.xlabel("Temps (s)")
plt.ylabel("Température (°C)")
plt.title("Courbe de température")
plt.grid(True)

# Demander à l'utilisateur de saisir le nom et l'emplacement du fichier de sortie
output_path = input("Entrez le chemin et le nom du fichier de sortie (.png): ")

# Enregistrer le graphe au format .png
plt.savefig(output_path)
print("Le graphe a été enregistré avec succès.")

# Afficher le graphe
plt.show()
pytho3