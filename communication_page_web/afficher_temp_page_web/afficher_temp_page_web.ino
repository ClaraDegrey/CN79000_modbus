// envoi de la temperature du four sur une page web (Adresse IP 192.168.0.2)
#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {
0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
IPAddress ip(192,168,0,2); //on choisit d'assigner cette adreese ip comme entree (pair pr les entrees et impaire pr les cartes)

// Initialize the Ethernet server library
// with the IP address and port you want to use
// (port 80 is default for HTTP):
EthernetServer server(80);

void setup() {

Serial.begin(9600);
if (!ModbusRTUClient.begin(9600,SERIAL_8N1)) {
Serial.println("Failed to start Modbus RTU Client!");
while (1);
}

Ethernet.init(5); //MKR ETH Shield

// Open serial communications and wait for port to open:
Serial.begin(9600);
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

uint16_t readTemp(){
uint16_t value = 0;
if (!ModbusRTUClient.requestFrom(1, HOLDING_REGISTERS, 0, 1)) {
Serial.print("Failed to read value! Error: ");
Serial.println(ModbusRTUClient.lastError());
} else {
value = ModbusRTUClient.read();
return value;
}
}

void loop() {
uint16_t tempfourbrut=0;
tempfourbrut=readTemp();
float tempfour=tempfourbrut/10.0;
Serial.println(tempfour);
// listen for incoming clients
EthernetClient client = server.available();
if (client) {
Serial.println("new client");
// an http request ends with a blank line
boolean currentLineIsBlank = true;
while (client.connected()) {
if (client.available()) {
char c = client.read();
Serial.write(c);
// if you've gotten to the end of the line (received a newline
// character) and the line is blank, the http request has ended,
// so you can send a reply
if (c == '\n' && currentLineIsBlank) {
// send a standard http response header
client.println("HTTP/1.1 200 OK");
client.println("Content-Type: text/html");
client.println("Connection: close"); // the connection will be closed after completion of the response
client.println("Refresh: 5"); // refresh the page automatically every 5 sec
client.println();
client.println("<!DOCTYPE HTML>");
client.println("<html>");
client.print("La temperature est de ");
client.print(tempfour);
client.print(" degres ");
client.println("<br />");
client.println("</html>");
break;
}
if (c == '\n') {
// you're starting a new line
currentLineIsBlank = true;
} else if (c != '\r') {
// you've gotten a character on the current line
currentLineIsBlank = false;
}
}
}
// give the web browser time to receive the data
delay(1);
// close the connection:
client.stop();
Serial.println("client disconnected");
}
}