import socket
import time

ip_address = "192.168.0.2"  # Adresse IP de la carte Arduino
port = 80  # Port sur lequel la carte Arduino écoute
temperature_consigne_desiree=25.7


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
    print("La température est de :", int(data)/10.0, "°C")
    time.sleep(1)
    sock.close()


def lecture_temperature_consigne(ip_address, port):
    variable_value = 't'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_address, port))
    sock.send(str(variable_value).encode())
    data = sock.recv(1024).decode()
    print("La température de consigne est de :", int(data)/10.0, "°C")
    time.sleep(1)
    sock.close()

def modification_temperature_consigne(ip_address, port, temperature_consigne_desiree):
    variable_value = 's'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_address, port))
    sock.send(str(variable_value).encode())
    sock.send(str(int(temperature_consigne_desiree*10)).encode())
    print("La température de consigne est maintenant à :", temperature_consigne_desiree, "°C")
    time.sleep(1)

while True:
 lecture_temperature(ip_address, port)

lecture_temperature(ip_address, port)
lecture_temperature_consigne(ip_address, port)
modification_temperature_consigne(ip_address, port, temperature_consigne_desiree)
lecture_temperature_consigne(ip_address, port)

