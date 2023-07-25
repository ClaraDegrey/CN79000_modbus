import socket

ip_address = "192.168.0.2"  # Adresse IP de la carte Arduino
port = 80  # Port sur lequel la carte Arduino écoute

variable_value = 123  # Valeur de la variable à envoyer

# Établir la connexion avec la carte Arduino
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip_address, port))

# Envoyer la valeur de la variable à la carte Arduino
sock.send(str(variable_value).encode())
data = sock.recv(1024).decode()
data1=data+3
print("Valeur reçue :", data1)

# Fermer la connexion
sock.close()

