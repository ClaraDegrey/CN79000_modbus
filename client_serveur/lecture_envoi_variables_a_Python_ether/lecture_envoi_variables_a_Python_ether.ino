// envoi de donnees par ethernet sans passer par une page web
// transforme les chaines de caracteres recues en entiers
#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>

byte mac[] = {
0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
IPAddress ip(192,168,0,2); 
EthernetServer server(80);

void setup() {

Serial.begin(9600);
Ethernet.init(5); 
while (!Serial) {
; // wait for serial port to connect. Needed for native USB port only
}
Serial.println("Ethernet WebServer Example");

// start the Ethernet connection and the server:
Ethernet.begin(mac, ip);

// Check for Ethernet hardware present
if (Ethernet.hardwareStatus() == EthernetNoHardware) {
Serial.println("Ethernet shield was not found. Sorry, can't run without hardware. :(");
while (true) {
delay(1); // do nothing, no point running without Ethernet hardware
}
}
if (Ethernet.linkStatus() == LinkOFF) {
Serial.println("Ethernet cable is not connected.");
}

// start the server
server.begin();
Serial.print("server is at ");
Serial.println(Ethernet.localIP());
}

void loop() {

EthernetClient client = server.available();  // Lecture de la variable envoyee par le script Python
  if (client) {
    String receivedData;

    while (client.connected()) {
      if (client.available()) {
          server.print(125);  //envoi de la valeur 123 sur le script Python
        char c = client.read();  // Lit le caractere recu
        receivedData += c;
        // Traitez le caractere ici
        // Par exemple, vous pouvez stocker les valeurs dans des variables
      }
    }
    int receivedValue = receivedData.toInt();  // Convertit la chaine en entier
    Serial.println(receivedValue+3);  // Affiche la valeur entiere
    client.stop();  // Ferme la connexion
  }
 delay(1000);
}