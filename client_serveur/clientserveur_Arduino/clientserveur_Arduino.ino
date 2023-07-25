// envoi et réception de données par ethernet sans passer par une page web
#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoRS485.h>
#include <ArduinoModbus.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192,168,0,2); 
EthernetServer server(80);
String receivedData;

void setup() {

Serial.begin(9600);

if (!ModbusRTUClient.begin(9600,SERIAL_8N1)) {
Serial.println("Failed to start Modbus RTU Client!");
while (1);
}

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

uint16_t readTempAsservissement(){
uint16_t value = 0;
if (!ModbusRTUClient.requestFrom(1, HOLDING_REGISTERS, 1, 1)) {
Serial.print("Failed to read value! Error: ");
Serial.println(ModbusRTUClient.lastError());
} else {
value = ModbusRTUClient.holdingRegisterRead(1,1);
return value;
}
}


void loop() {
  EthernetClient client = server.available();

  if (client) {
    receivedData = "";

    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        receivedData += c;

        if (receivedData.startsWith("r")) {
          server.println(readTemp());
        }

        if (receivedData.startsWith("t")) {
          server.println(readTempAsservissement());
        }
      }
    }
            if (receivedData.startsWith("s")) {
          String chaineModifiee = receivedData.substring(1);
          int nouvelletempasservissement = chaineModifiee.toInt();
          ModbusRTUClient.holdingRegisterWrite(1, 1, nouvelletempasservissement);
          Serial.print("La nouvelle température d'asservissement est de : ");
          Serial.print(nouvelletempasservissement);
          Serial.println(" °C");
        }
    Serial.println(receivedData);
    client.stop();
  }

  delay(1000);
}